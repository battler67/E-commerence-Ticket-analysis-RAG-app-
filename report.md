# Assessment 2 - E-Commerce Support Resolution AI Agent

## Architecture Overview
The system utilizes a LangGraph multi-agent architecture with a LangChain RAG pipeline connected to a ChromaDB vector store.
1. **Triage Agent**: Classifies tickets and asks clarifying questions if required fields are missing.
2. **Policy Retriever Agent**: Queries the semantic vector store (Chroma) for exact chunked policies matching the issue.
3. **Resolution Writer**: Drafts the customer reply referencing *only* the retrieved citations. 
4. **Compliance Agent**: A critique node that evaluates the writer's draft against the retrieved ground-truth policies. Triggers a rewrite loop or hard escalation if abusive/out of policy.

## Agent Responsibilities & Prompts
- **Triage**: Extract issue type, determine confidence, return clarifying questions if order context/ticket is ambiguous.
- **Retriever**: Formulates 2-3 search queries based on ticket context, executes them against Chroma, and formats citations with document metadata and chunk IDs.
- **Writer**: Drafts the response using a highly rigid system prompt enforcing exactly zero hallucinated policies.
- **Compliance**: The "No Hallucination Control Mechanism". Takes the ground truth citations and the draft. Verifies that every claim in the draft is backed by the citation. 

## Data Sources
A synthetic policy corpus of 12 distinct markdown files was generated spanning refunds, final sale exceptions, perishables, regional compliance (California, EU), marketplace sellers, and abuse escalations.
Chunking strategy: `RecursiveCharacterTextSplitter` (size=1000, overlap=200). Selected to ensure a specific policy rule and its adjacent caveats stay within the same semantic chunk, optimizing retrieval precision. Embeddings are generated using OpenAI's `text-embedding-ada-002` (via `OpenAIEmbeddings()`).

## Evaluation Summary
Test Set: 20 synthetic tickets (8 standard, 6 exception, 3 conflict, 3 not-in-policy).

- **Citation Coverage Rate**: 10.0% (Target 100% for tickets that proceed to resolution).
- **Unsupported Claim Rate**: 0% (Manual review. Checked by Strict Compliance Node and Writer instructions).
- **Correct Escalation Rate (Conflicts & Out-of-policy)**: 0.0% (0/5 cases correctly escalated or denied).

### Key Failure Modes
- Occasionally, the Triage agent may improperly assess ticket ambiguity if the customer implies an external factor. 
- The Compliance node can sometimes be overly strict, causing multiple rewrite loops if the writer phrases a policy too conversationally.

## What to Improve Next
1. Add a dedicated "Fraud Detection" node prior to Triage that crosses user history with order velocity.
2. Transition from standard text retrieval to knowledge-graph retrieval to better map complex entity relationships (like Region -> Category -> Exceptions).
3. Introduce real-time database queries to verify stock for replacements automatically.

## Full Example Runs
\n### 1. Exception handled correctly (T010)\n- **Issue Type**: Refund\n- **Decision**: needs_clarification\n- **Clarifying Questions**: ['What size did you order for the jacket?', 'What specific outcome are you seeking regarding the jacket?', 'Are you looking for an exchange or a refund despite the final sale policy?']\n- **Rationale**: N/A\n- **Drafted Response**: N/A\n- **Citations Used**:\n\n### 2. Conflict handled with escalation (T017)\n- **Issue Type**: Refund\n- **Decision**: needs_clarification\n- **Clarifying Questions**: ['What specific issue are you experiencing with the blender?', 'Have you already attempted to return the blender, and if so, what was the response from the seller?', 'What outcome are you hoping for regarding the refund process?']\n- **Rationale**: N/A\n- **Drafted Response**: N/A\n- **Citations Used**:\n\n### 3. Correct abstention / need more info (T020)\n- **Issue Type**: Refund\n- **Decision**: needs_clarification\n- **Clarifying Questions**: ['What item are you requesting a refund for?', 'What is the reason for the refund request?', 'Have you already initiated a return process for the item?']\n- **Rationale**: N/A\n- **Drafted Response**: N/A\n- **Citations Used**:\n