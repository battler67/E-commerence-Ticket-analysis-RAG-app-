# E-Commerce Support Ticket Analysis RAG Agent


This project is a multi-agent retrieval-augmented generation (RAG) system built with **LangGraph**, **LangChain**, and **ChromaDB**. It autonomously resolves customer support tickets based exclusively on corporate policy, with strict guardrails against LLM hallucinations.

<p align="center">
  <a href="https://www.youtube.com/watch?v=MISOjLwmuV4">
    <img src="https://img.youtube.com/vi/MISOjLwmuV4/maxresdefault.jpg" width="700">
  </a>
</p>

## Architecture
The system employs a 4-Agent architecture mapping to the LangGraph state machine:
1. **Triage Agent**: Takes the raw ticket and order context, categorizing the issue and optionally generating up to 3 clarifying questions if context is ambiguous or missing.
2. **Policy Retriever Agent**: Translates the customer issue into highly targeted semantic queries. Connects to the Chroma vector database to retrieve specific policy chunks with metadata citations.
3. **Resolution Writer Agent**: Drafts a structured internal/customer-facing resolution document applying the customer's issue only against the exact retrieved policy citations.
4. **Compliance & Safety Agent**: Validates that every claim made by the writer is explicitly justified by the citations, intercepting non-compliant or abusive behaviors via escalation triggers or forced rewrite loops.

## Input Format
The system strictly accepts the following payload structures:

### A) Ticket Text
Free-form `string`. Examples: `"My order arrived late and the cookies are melted. I want a full refund."`

### B) Order Context (Structured JSON)
```json
{
  "order_date": "YYYY-MM-DD",
  "delivery_date": "YYYY-MM-DD",
  "item_category": "string",
  "fulfillment_type": "first-party | marketplace seller",
  "shipping_region": "string",
  "order_status": "placed | shipped | delivered | returned",
  "payment_method": "string (optional)",
  "item_tags": ["string (optional)"]
}
```

## Setup & Running the Project

### Prerequisites
- Python 3.10+
- OpenAI API Key

### Installation

1. Create and activate a Virtual Environment:
```bash
python -m venv venv
# On Windows
.\venv\Scripts\Activate.ps1
# On MacOS/Linux
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Export your API Key:
Create a `.env` file containing your OpenAI key:
```env
OPENAI_API_KEY=sk-xxxxxx
```

### Usage

1. **Generate Data & Test Cases**
```bash
python src/generate_data.py
```
*This populates `data/policies/` with 12 distinct markdown policy documents covering all assessment edge cases, and creates `data/tickets.json` containing 20 evaluated test cases.*

2. **Run Evaluation & Report Generator**
```bash
python src/evaluate.py
```
*This executes all 20 test cases through the complete multi-agent LangGraph workflow. It reports real-time traces via the console and ultimately emits `report.md`, evaluating correct escalation and citation rates.*
