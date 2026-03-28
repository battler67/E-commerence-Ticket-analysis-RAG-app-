import os
import sys

# Ensure project root is in sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from dotenv import load_dotenv
load_dotenv()

from src.graph import build_graph

def generate_explanation(state, query):
    report = f"# Explanation for Query\n**User Query:** {query}\n\n"
    
    # Extract decision and rationale
    decision = state.get('decision', 'N/A')
    rationale = state.get('rationale', 'N/A')
    customer_response = state.get('customer_response', 'N/A')
    
    report += f"## Resolution\n- **Decision:** {decision}\n- **Rationale:** {rationale}\n\n"
    
    # Conflict handling / Escalation
    if state.get('needs_escalation'):
        report += "### Conflict Handling (Escalated)\n"
        report += f"The agent determined the issue requires escalation. Reason: {state.get('escalation_reason', 'N/A')}\n\n"
    elif state.get('rewrite_count', 0) > 0:
        report += "### Conflict Handling (Compliance Retries)\n"
        report += f"The agent's initial draft violated policies and was sent back for {state.get('rewrite_count')} rewrite(s). "
        if state.get('compliance_feedback'):
            report += f"Latest feedback: {state.get('compliance_feedback')}\n\n"
    else:
        report += "### Conflict Handling\n"
        report += "No major conflicts. The customer request was handled directly based on policy.\n\n"
        
    # Top-K Documents
    report += "## Top-K Documents Visited\n"
    citations = state.get('citations', [])
    if citations:
        for i, c in enumerate(citations):
            report += f"{i+1}. **{c.get('doc')}** (Chunk: {c.get('chunk_id')})\n"
            content = c.get('content', '').replace('\n', ' ')
            report += f"   > {content[:200]}...\n"
    else:
        report += "No policy documents were cited for this query.\n"
        
    report += f"\n## Final Response Draft\n```\n{customer_response}\n```\n"

    with open("explanation.md", "w", encoding="utf-8") as f:
        f.write(report)
        
    print(f"\n[System] Detailed explanation saved to 'explanation.md'")

def main():
    print("=========================================")
    print(" E-Commerce Support Agent - CLI Mode")
    print("=========================================\n")
    
    print("[System] Initializing Agent & Loading Vector Database...")
    graph = build_graph()
    print("[System] Ready!\n")
    
    print("--- LangGraph Architecture ---")
    try:
        graph.get_graph().print_ascii()
    except Exception as e:
        print(f"[Could not render graph natively: {e}]")
    print("------------------------------\n")
    
    print("\n--- Order Context Configuration (Press Enter to skip any field) ---")
    order_context = {}
    
    def prompt_choice(field_name, options):
        print(f"\n{field_name}:")
        for i, opt in enumerate(options, 1):
            print(f"  {i}. {opt}")
        val = input(f"Choose a number for {field_name} (1-{len(options)}) [Skip]: ").strip()
        if val.isdigit() and 1 <= int(val) <= len(options):
            return options[int(val)-1]
        return None
        
    status = prompt_choice("order_status", ['placed', 'shipped', 'delivered', 'lost'])
    if status: order_context["order_status"] = status
    
    fulfillment = prompt_choice("fulfillment_type", ['first-party', 'marketplace seller'])
    if fulfillment: order_context["fulfillment_type"] = fulfillment
    
    category = prompt_choice("item_category", ['Apparel', 'Electronics', 'Home', 'Perishable', 'Accessories'])
    if category: order_context["item_category"] = category
    
    region = prompt_choice("shipping_region", ['California', 'UK', 'Texas', 'New York', 'Other'])
    if region:
        if region == "Other":
            region = input("Enter custom shipping region: ").strip() or "Unknown"
        order_context["shipping_region"] = region
        
    tag = prompt_choice("item_tags", ['Final Sale', 'Personalized', 'None'])
    if tag and tag != 'None':
        order_context["item_tags"] = [tag]
    
    print(f"\nContext Captured: {order_context}")
    
    while True:
        print("-" * 50)
        try:
            user_input = input("Enter your support query (or type 'exit' to quit): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            break
            
        if user_input.lower() in ['exit', 'quit']:
            break
            
        if not user_input:
            continue
                
        ticket_text = user_input
        clarification_count = 0
        chat_history = []
        
        while True:
            current_ticket = ticket_text
            if clarification_count >= 3:
                current_ticket += "\n\n[SYSTEM DIRECTIVE: Maximum clarifying questions (3) reached. You MUST NOT ask any further questions. You MUST classify the issue and draw a final conclusion based on policy.]"
                
            from typing import Any
            initial_state: dict[str, Any] = {
                "ticket": current_ticket,
                "order_context": order_context,
                "rewrite_count": 0,
                "clarification_count": clarification_count,
                "chat_history": chat_history
            }
            
            if clarification_count > 0:
                print(f"\n[System] Starting Agents (Follow-up Turn {clarification_count})...\n")
            else:
                print("\n[System] Starting Agents...\n")
                
            current_state: dict[str, Any] = dict(initial_state)
            
            # Stream the graph execution to print node status
            for event in graph.stream(initial_state):
                # event is a dict mapping node_name to its output
                for node_name, original_updates in event.items():
                    print(f"--> [Agent Working: {node_name.upper()}] <--")
                    
                    if not isinstance(original_updates, dict):
                        continue
                        
                    node_updates: dict = original_updates
                    
                    # Update our tracking state with the latest updates from the node
                    current_state.update(node_updates)
                    
                    # Print descriptive highlights based on the node
                    if node_name == "triage":
                        print(f"    Issue Type Identified: {node_updates.get('issue_type', 'N/A')}")
                        if node_updates.get('clarifying_questions'):
                            print("    Needs Clarification: Yes")
                    elif node_name == "retriever":
                        citations = node_updates.get('citations', [])
                        print(f"    Retrieved {len(citations)} policy chunks from ChromaDB.")
                    elif node_name == "writer":
                        print(f"    Drafting Response (Rewrite Attempt: {node_updates.get('rewrite_count', current_state.get('rewrite_count', 0))})...")
                    elif node_name == "compliance":
                        is_compliant = node_updates.get('is_compliant')
                        print(f"    Compliance Check passed: {is_compliant}")
                        if not is_compliant:
                            print(f"    Feedback: {node_updates.get('compliance_feedback')}")
                    elif node_name in ["clarification_end", "escalation_end", "approved_end"]:
                        print(f"    Workflow reached terminal state: {node_name}")
                        
                    print()  # empty line for readability

            c_qs = current_state.get('clarifying_questions', [])
            
            # If clarifying questions exist and we haven't hit the 3-limit, follow up interactively
            if c_qs and clarification_count < 3:
                import random
                selected_q = random.choice(c_qs)
                print("-" * 50)
                print(f"1. Classification: {current_state.get('issue_type')} (Confidence: {current_state.get('confidence')})")
                print(f"2. Clarifying Question: {selected_q}")
                print("-" * 50)
                
                user_reply = input("--> Please answer the clarification question (or 'exit' to cancel): ").strip()
                if user_reply.lower() in ['exit', 'quit']:
                    print("Exiting conversation thread.")
                    break
                
                # Append to chat history
                chat_history.append({"role": "assistant", "content": selected_q})
                chat_history.append({"role": "human", "content": user_reply})
                
                clarification_count += 1
                continue  # Loop again and re-feed to the graph
                
            # If we reach here, it concluded successfully or hit the max 3 limit
            print("-" * 50)
            print(f"1. Classification: {current_state.get('issue_type')} (Confidence: {current_state.get('confidence')})")
            
            if c_qs and clarification_count >= 3:
                print("2. Clarifying Questions: None (Max 3 follow-ups reached, forced policy conclusion)")
            else:
                print("2. Clarifying Questions: None")
                
            print(f"3. Conflicts Analyzed: {current_state.get('conflicts_considered', 'N/A')}")
            print(f"4. Decision: {current_state.get('decision')}")
            print(f"5. Rationale: {current_state.get('rationale')}")
            print("6. Citations & Sources:")
            import os
            for c in current_state.get('citations', []):
                doc_name = c.get('doc', 'Unknown')
                abs_path = os.path.abspath(os.path.join("data", "policies", doc_name)).replace('\\', '/')
                url = f"file:///{abs_path}"
                print(f"   - {doc_name} (ID: {c.get('chunk_id')})")
                print(f"     URL: {url}")
                print(f"     Date Accessed: 28/3/2026")
            resp = str(current_state.get('customer_response', 'N/A'))
            print(f"7. Customer Response Draft: {resp[:100]}...")
            print(f"8. Next Steps / Internal Notes: {current_state.get('next_steps')}\n")
            
            # Generate the explanation file
            generate_explanation(current_state, ticket_text)
            break

if __name__ == "__main__":
    main()
