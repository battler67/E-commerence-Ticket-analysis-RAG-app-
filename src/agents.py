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
        ("system", "You are an expert E-Commerce Support Triage Agent. Your job is to classify the support ticket and identify if critical information is missing based on the order context. If essential information (like what item is broken, or what outcome they want) is missing, formulate up to 3 clarifying questions. Otherwise, leave clarifying questions empty."),
        ("human", "Ticket: {ticket}\n\nOrder Context: {order_context}")
    ])
    
    chain = prompt | llm.with_structured_output(TriageOutput)
    result = chain.invoke({
        "ticket": state["ticket"],
        "order_context": json.dumps(state["order_context"], indent=2)
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
HARD RULE: You must ONLY use the provided policy citations. Do NOT invent policies.
HARD RULE: If a customer requests something outside of the cited policies, you must deny it or state that you cannot fulfill it based on the policy.
Provide your rationale and the customer draft."""),
        ("human", """Ticket: {ticket}
Order Context: {order_context}
Issue Type: {issue_type}

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
        
    result = chain.invoke({
        "ticket": state["ticket"],
        "order_context": json.dumps(state["order_context"], indent=2),
        "issue_type": state["issue_type"],
        "citations": citations_str,
        "compliance_feedback": state.get("compliance_feedback", "None")
    })
    
    return {
        "decision": result.decision,
        "rationale": result.rationale,
        "customer_response": result.customer_response,
        "next_steps": result.next_steps,
        "rewrite_count": state.get("rewrite_count", 0) + 1
    }

def compliance_node(state: AgentState):
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a strict Compliance & Safety Support Agent.
Your job is to review the drafted customer response against the cited policies and the customer's request.
Check for:
1. Unsupported statements (hallucinations).
2. Missing or weak citations for any claims made.
3. Giving a refund/replacement when policy strictly forbids it (e.g. Final Sale, out of timeframe).
4. Abusive customer behavior or legal threats that require immediate escalation.

If the draft violates policy, invents rules, or if the customer is abusive/threatening, mark compliant=False.
If it's a minor error that the writer can fix, provide feedback and needs_hard_escalation=False.
If the customer is threatening legal action or extreme policy abuses, set needs_hard_escalation=True."""),
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
