from typing import TypedDict, List, Optional
from pydantic import BaseModel, Field

# Pydantic Output Models for Structured LLM Responses

class TriageOutput(BaseModel):
    issue_type: str = Field(description="Classification of the ticket (e.g., Refund, Shipping, Payment, Promo, Fraud, Other, Ambiguous)")
    confidence: float = Field(description="Confidence in classification (0.0 to 1.0)")
    clarifying_questions: List[str] = Field(description="Up to 3 optional clarifying questions if critical info is missing")

class PolicyQuery(BaseModel):
    queries: List[str] = Field(description="List of targeted search queries to fetch relevant policies")

class ResolutionDraftOutput(BaseModel):
    decision: str = Field(description="Decision made: approve, deny, partial, or needs escalation")
    rationale: str = Field(description="Policy-based rationale for the decision")
    customer_response: str = Field(description="Customer-ready message addressing the issue")
    next_steps: str = Field(description="Internal notes or recommendations on what support does next")

class ComplianceOutput(BaseModel):
    is_compliant: bool = Field(description="Whether the drafted response is 100% supported by citations and policy")
    feedback: str = Field(description="Feedback for the Resolution Writer if not compliant")
    needs_hard_escalation: bool = Field(description="True if request is out of scope or abusive and must be escalated")

# LangGraph State Definition
class AgentState(TypedDict):
    ticket: str
    order_context: dict
    # Populated by Triage
    issue_type: str
    confidence: float
    clarifying_questions: List[str]
    # Populated by Retriever
    citations: List[dict]
    # Populated by Resolution Writer
    decision: str
    rationale: str
    customer_response: str
    next_steps: str
    # Populated by Compliance
    compliance_feedback: str
    is_compliant: bool
    needs_escalation: bool
    escalation_reason: str
    # Loop counters
    rewrite_count: int
