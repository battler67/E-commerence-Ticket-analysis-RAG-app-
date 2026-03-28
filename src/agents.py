import os
import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from src.models import (
    AgentState, 
    TriageOutput, 
    PolicyQuery, 
    ResolutionDraftOutput, 
    ComplianceOutput
)
from src.rag import get_chroma_vectorstore, format_citations

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Instantiate vectorstore once
vectorstore = get_chroma_vectorstore()

def triage_node(state: AgentState):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert E-Commerce Support Triage Agent. Your job is to classify the support ticket and identify if critical information is missing based on the order context. If essential information (like what item is broken, or what outcome they want) is missing, or the request is ambiguous, you MUST formulate up to 3 clarifying questions. Otherwise, leave clarifying questions empty."),
        ("human", "Ticket: {ticket}\n\nOrder Context: {order_context}\n\nChat History:\n{chat_history}")
    ])
    
    chain = prompt | llm.with_structured_output(TriageOutput)
    
    # Format chat history
    history_str = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in state.get("chat_history", [])])
    
    result = chain.invoke({
        "ticket": state["ticket"],
        "order_context": json.dumps(state["order_context"], indent=2),
        "chat_history": history_str if history_str else "None"
    })
    
    return {
        "issue_type": result.issue_type,
        "confidence": result.confidence,
        "clarifying_questions": result.clarifying_questions
    }

def retriever_node(state: AgentState):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a Policy Retrieval Formulator. Based on the ticket, order context, and issue type, generate 1-3 targeted search queries to find the exact policies needed to resolve this issue in our vector database."),
        ("human", "Issue Type: {issue_type}\nTicket: {ticket}\nOrder Context: {order_context}")
    ])
    
    chain = prompt | llm.with_structured_output(PolicyQuery)
    result = chain.invoke({
        "issue_type": state["issue_type"],
        "ticket": state["ticket"],
        "order_context": json.dumps(state["order_context"], indent=2)
    })
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    all_docs = []
    
    for query in result.queries:
        docs = retriever.invoke(query)
        all_docs.extend(docs)
    
    # Deduplicate based on chunk_id
    seen = set()
    unique_docs = []
    for doc in all_docs:
        chunk_id = doc.metadata.get("chunk_id")
        if chunk_id not in seen:
            seen.add(chunk_id)
            unique_docs.append(doc)
            
    formatted_citations, citations_metadata = format_citations(unique_docs)
    
    return {"citations": citations_metadata}

def writer_node(state: AgentState):
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a Resolution Writer for Purple Merit Technologies. 
Your task is to draft a customer-ready response resolving their ticket.
EVIDENCE-ONLY RULE: You must answer ONLY on the basis of the retrieved Top-K documents. Do not invent details or assume company procedures.
REFUSAL RULE: If the provided citations do not contain sufficient evidence to thoroughly answer the user's query, you MUST refuse. You must state exactly: 'I am unable to provide a solution as the policies do not cover this issue.' in the customer draft, and set decision to 'needs escalation'.
HARD RULE: If a customer requests something "Not in policy", you must abstain or escalate; no guessing.
HARD RULE: You must compulsorily evaluate and write out every possibility of policy conflict considered (e.g., Regional laws vs General policy). Exceptions (like Final Sale, Hygiene) override general rules.
Provide your conflicts_considered, rationale, decision, customer draft, and next_steps.
CRITICAL: You MUST provide concrete next steps for the human support agent or system. Do not leave next_steps empty under any circumstances."""),
        ("human", """Ticket: {ticket}
Order Context: {order_context}
Issue Type: {issue_type}

Chat History:
{chat_history}

--- RETRIEVED POLICIES ---
{citations}
--------------------------

Feedback from Compliance (if any): {compliance_feedback}""")
    ])
    
    chain = prompt | llm.with_structured_output(ResolutionDraftOutput)
    
    # Format citations for the prompt
    citations_str = ""
    for c in state.get("citations", []):
        citations_str += f"- Doc: {c['doc']} (ID: {c['chunk_id']})\n  Content: {c['content']}\n\n"
        
    history_str = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in state.get("chat_history", [])])
        
    result = chain.invoke({
        "ticket": state["ticket"],
        "order_context": json.dumps(state["order_context"], indent=2),
        "issue_type": state["issue_type"],
        "chat_history": history_str if history_str else "None",
        "citations": citations_str,
        "compliance_feedback": state.get("compliance_feedback", "None")
    })
    
    return {
        "conflicts_considered": result.conflicts_considered,
        "decision": result.decision,
        "rationale": result.rationale,
        "customer_response": result.customer_response,
        "next_steps": result.next_steps,
        "rewrite_count": state.get("rewrite_count", 0) + 1
    }

def compliance_node(state: AgentState):
    # Hard-coded citation checker mapping directly to user requirements
    if not state.get("citations") or len(state["citations"]) == 0:
        return {
            "is_compliant": False,
            "compliance_feedback": "CRITICAL FAILURE: No citations retrieved. Run explicitly failed due to zero evidence.",
            "needs_escalation": True,
            "escalation_reason": "No policy evidence found. Missing citations."
        }
        
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a strict Compliance & Safety Verifier Agent.
Your job is to review the drafted customer response against the cited Top-K documents.
VERIFIER AGENT RULE: You MUST manually block any claim not explicitly supported by the citations. If citations are missing for a specific claim made by the writer, FAIL the run (set needs_hard_escalation=True).
Check for:
1. Unsupported statements (hallucinations): Any policy claim MUST be backed by citations.
2. Giving a refund/replacement when policy strictly forbids it (e.g., Exception-heavy categories).
3. Failing to handle "Not in policy" requests properly.
4. Abusive customer behavior or legal threats requiring escalation.

If the draft violates policy or invents rules, mark compliant=False.
If the customer is threatening legal action, or the writer invented a massive policy, set needs_hard_escalation=True."""),
        ("human", """Customer Ticket: {ticket}

--- RETRIEVED POLICIES (Ground Truth) ---
{citations}
-----------------------------------------

--- DRAFTED RESPONSE ---
Decision: {decision}
Rationale: {rationale}
Message: {customer_response}
Next Steps: {next_steps}""")
    ])
    
    chain = prompt | llm.with_structured_output(ComplianceOutput)
    
    citations_str = ""
    for c in state.get("citations", []):
        citations_str += f"- Doc: {c['doc']} (ID: {c['chunk_id']})\n  Content: {c['content']}\n\n"
        
    result = chain.invoke({
        "ticket": state["ticket"],
        "citations": citations_str,
        "decision": state["decision"],
        "rationale": state["rationale"],
        "customer_response": state["customer_response"],
        "next_steps": state["next_steps"]
    })
    
    return {
        "is_compliant": result.is_compliant,
        "compliance_feedback": result.feedback,
        "needs_escalation": result.needs_hard_escalation,
        "escalation_reason": result.feedback if result.needs_hard_escalation else ""
    }
