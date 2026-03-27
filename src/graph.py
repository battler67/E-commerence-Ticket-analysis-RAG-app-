from langgraph.graph import StateGraph, END
from src.models import AgentState
from src.agents import triage_node, retriever_node, writer_node, compliance_node

def route_triage(state: AgentState):
    # If the triage node found that clarifying questions are needed, or if confidence is very low.
    if state.get("clarifying_questions") and len(state["clarifying_questions"]) > 0:
        return "needs_clarification"
    return "retrieve_policies"

def route_compliance(state: AgentState):
    if state.get("needs_escalation"):
        return "escalated"
    if state.get("is_compliant"):
        return "approved"
    
    # If not compliant, rewrite up to 3 times
    if state.get("rewrite_count", 0) >= 3:
        return "escalated"
    
    return "rewrite"

def build_graph():
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("triage", triage_node)
    workflow.add_node("retriever", retriever_node)
    workflow.add_node("writer", writer_node)
    workflow.add_node("compliance", compliance_node)
    
    # Add dummy node for clarification/escalation ends
    workflow.add_node("clarification_end", lambda x: {"decision": "needs_clarification"})
    workflow.add_node("escalation_end", lambda x: {"decision": "escalate"})
    workflow.add_node("approved_end", lambda x: x)
    
    # Edges
    workflow.set_entry_point("triage")
    
    workflow.add_conditional_edges(
        "triage",
        route_triage,
        {
            "needs_clarification": "clarification_end",
            "retrieve_policies": "retriever"
        }
    )
    
    workflow.add_edge("retriever", "writer")
    workflow.add_edge("writer", "compliance")
    
    workflow.add_conditional_edges(
        "compliance",
        route_compliance,
        {
            "approved": "approved_end",
            "rewrite": "writer",
            "escalated": "escalation_end"
        }
    )
    
    workflow.add_edge("clarification_end", END)
    workflow.add_edge("escalation_end", END)
    workflow.add_edge("approved_end", END)
    
    return workflow.compile()
