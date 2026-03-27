import os
import json

def generate_policies():
    policies_dir = "data/policies"
    os.makedirs(policies_dir, exist_ok=True)
    
    policies = {
        "Refund_Policy.md": """# General Refund Policy
Purple Merit Technologies strives for customer satisfaction. 
- You have 30 days from the delivery date to return an eligible item for a full refund.
- Refunds will be issued to the original payment method within 5-7 business days of receiving the return.
- To be eligible for a full refund, items must be in their original condition and packaging.
- Items lacking an order status cannot be refunded until their status is confirmed as 'delivered' or 'lost'.
""",
        "Returns_Exceptions.md": """# Return Exceptions Policy
Certain items are subject to specific return restrictions:
- **Final Sale**: Items marked "Final Sale" cannot be returned or refunded under any circumstances.
- **Hygiene Items**: Underwear, swimwear, and earrings can only be returned if fully sealed in their original packaging. Opened hygiene items are not eligible for refunds.
- **Perishables**: Food, flowers, and other perishable items cannot be returned. If they arrive damaged or spoiled, customers may request a refund within 48 hours of delivery, provided they supply photographic evidence.
""",
        "Cancellations.md": """# Order Cancellation Policy
- Orders can be canceled for a full refund before they have shipped.
- Once an order's status is 'shipped' or 'delivered', it cannot be canceled. The customer must initiate a regular return process instead.
- Digital products and personalized items cannot be canceled once the order is placed.
""",
        "Shipping_Delivery.md": """# Shipping and Delivery Policy
- Standard shipping takes 3-5 business days. Expedited takes 1-2 business days.
- **Lost Packages**: If tracking shows 'delivered' but the customer hasn't received it, they must wait 48 hours before filing a claim, as carriers sometimes scan early. If it's still missing, we will offer a replacement or refund.
- **Delayed Orders**: For standard shipping, no compensation is provided for minor delays. However, if expedited shipping is delayed by our fault, shipping fees will be refunded.
""",
        "Promotions_Coupons.md": """# Promotions and Coupons Terms
- Only one promo code can be applied per order.
- Welcome coupons (e.g., WELCOME10) are valid for first-time purchases only.
- If a customer forgot to apply a valid coupon at checkout, support agents can retroactively apply it and refund the difference, *provided the request is made within 24 hours of placing the order*.
""",
        "Disputes_Damaged.md": """# Damaged or Incorrect Items
- If an item arrives damaged, the customer is entitled to a full refund or a free replacement.
- For incorrect items received, the customer must return the incorrect item (using a prepaid label we provide) before the correct item is dispatched or a refund is issued.
- If a ticket involves damaged electronics, the customer must first attempt troubleshooting with the manufacturer before a refund is processed.
""",
        "Marketplace_Sellers.md": """# Third-Party Seller Policy
Purple Merit Technologies hosts third-party (marketplace) sellers.
- **Fulfillment**: If `fulfillment_type` is 'marketplace seller', the seller is responsible for returns and refunds.
- Customers must contact the seller directly for returns.
- Purple Merit Technologies Support can only issue refunds for marketplace orders if the seller fails to respond within 3 business days, under our "A-Z Guarantee".
""",
        "Regional_Differences.md": """# Regional Compliance Policy
Regulations vary by region:
- **California**: Customers in California are entitled to return electronics for up to 60 days (supersedes standard 30-day).
- **EU/UK**: Customers based in the EU or UK have a "cooling off" period of 14 days where they can return any order for any reason, including Final Sale (excluding perishables/custom items).
- **Apparel**: In the state of New York, apparel returns must be accepted within 45 days.
""",
        "Missing_Items.md": """# Missing Items Policy
- If an order shows multiple items delivered but one is missing, the customer must check the package thoroughly.
- Sometimes orders are split into multiple shipments. Support must verify the shipping status of all items in an order.
- If verified missing, a partial refund or replacement will be provided immediately without requiring a dispute.
""",
        "Exchanges.md": """# Exchanges Policy
- We currently do not process direct exchanges for any items. 
- Customers wishing to exchange an item must return the original item for a refund and place a new order.
- If a customer applies for an exchange, support should direct them to the returns portal.
""",
        "Gift_Cards.md": """# Gift Card Policy
- Gift cards are non-refundable and cannot be redeemed for cash, except where required by law.
- If an order paid with a gift card is returned, the refund will be credited back to the original gift card.
""",
        "Escalations_Abuse.md": """# Policy on Support Abuse and Escalations
- Customers who use abusive language must receive a warning. If they persist, the ticket must be closed without resolution.
- Any request for compensation (like free items/credits) simply because a customer is unhappy, with no policy violation, must be denied. Support agents must not invent non-policy resolutions to appease customers.
- If a customer threatens legal action, the ticket must be instantly escalated to the Legal Escalations Team. Support must not respond directly to legal threats.
"""
    }

    for filename, content in policies.items():
        with open(os.path.join(policies_dir, filename), "w") as f:
            f.write(content)
    print(f"Generated {len(policies)} policy documents.")

def generate_tickets():
    tickets = [
        # Standard Cases (8)
        {
            "id": "T001",
            "type": "Standard",
            "ticket_text": "I received my order yesterday but I don't want it anymore. How do I return it?",
            "order_context": {
                "order_date": "2026-03-20",
                "delivery_date": "2026-03-27",
                "item_category": "Apparel",
                "fulfillment_type": "first-party",
                "shipping_region": "Texas",
                "order_status": "delivered",
                "payment_method": "Credit Card"
            }
        },
        {
            "id": "T002",
            "type": "Standard",
            "ticket_text": "My laptop arrived with a shattered screen. I want a refund.",
            "order_context": {
                "order_date": "2026-03-22",
                "delivery_date": "2026-03-26",
                "item_category": "Electronics",
                "fulfillment_type": "first-party",
                "shipping_region": "Florida",
                "order_status": "delivered"
            }
        },
        {
            "id": "T003",
            "type": "Standard",
            "ticket_text": "I meant to use the code WELCOME10 but I hit submit too quickly! Can you add it?",
            "order_context": {
                "order_date": "2026-03-28", # Today
                "delivery_date": None,
                "item_category": "Home",
                "fulfillment_type": "first-party",
                "shipping_region": "Ohio",
                "order_status": "placed"
            }
        },
        {
            "id": "T004",
            "type": "Standard",
            "ticket_text": "Cancel my order please, I bought it by mistake.",
            "order_context": {
                "order_date": "2026-03-28",
                "delivery_date": None,
                "item_category": "Books",
                "fulfillment_type": "first-party",
                "shipping_region": "Nevada",
                "order_status": "placed"
            }
        },
        {
            "id": "T005",
            "type": "Standard",
            "ticket_text": "Tracking says delivered but there's no package here! It said delivered 3 days ago.",
            "order_context": {
                "order_date": "2026-03-15",
                "delivery_date": "2026-03-25",
                "item_category": "Toys",
                "fulfillment_type": "first-party",
                "shipping_region": "Georgia",
                "order_status": "delivered"
            }
        },
        {
            "id": "T006",
            "type": "Standard",
            "ticket_text": "I ordered 3 books but only 2 were in the box.",
            "order_context": {
                "order_date": "2026-03-22",
                "delivery_date": "2026-03-26",
                "item_category": "Books",
                "fulfillment_type": "first-party",
                "shipping_region": "Oregon",
                "order_status": "delivered"
            }
        },
        {
            "id": "T007",
            "type": "Standard",
            "ticket_text": "Can I exchange this shirt for a medium?",
            "order_context": {
                "order_date": "2026-03-10",
                "delivery_date": "2026-03-15",
                "item_category": "Apparel",
                "fulfillment_type": "first-party",
                "shipping_region": "Utah",
                "order_status": "delivered"
            }
        },
        {
            "id": "T008",
            "type": "Standard",
            "ticket_text": "I got the wrong color mug. I ordered blue but got red.",
            "order_context": {
                "order_date": "2026-03-20",
                "delivery_date": "2026-03-25",
                "item_category": "Home",
                "fulfillment_type": "first-party",
                "shipping_region": "Michigan",
                "order_status": "delivered"
            }
        },
        
        # Exception-heavy Cases (6)
        {
            "id": "T009",
            "type": "Exception",
            "ticket_text": "The bouquet of roses I ordered arrived completely withered. I want a refund right now. Attached are photos.",
            "order_context": {
                "order_date": "2026-03-25",
                "delivery_date": "2026-03-27",
                "item_category": "Perishable",
                "fulfillment_type": "first-party",
                "shipping_region": "Virginia",
                "order_status": "delivered"
            }
        },
        {
            "id": "T010",
            "type": "Exception",
            "ticket_text": "I bought this jacket on clearance marked final sale, but it doesn't fit my husband.",
            "order_context": {
                "order_date": "2026-03-15",
                "delivery_date": "2026-03-22",
                "item_category": "Apparel",
                "fulfillment_type": "first-party",
                "shipping_region": "Arizona",
                "order_status": "delivered",
                "item_tags": ["Final Sale"]
            }
        },
        {
            "id": "T011",
            "type": "Exception",
            "ticket_text": "The swimwear I bought doesn't fit correctly. I tried it on yesterday.",
            "order_context": {
                "order_date": "2026-03-15",
                "delivery_date": "2026-03-22",
                "item_category": "Apparel",
                "fulfillment_type": "first-party",
                "shipping_region": "Colorado",
                "order_status": "delivered"
            }
        },
        {
            "id": "T012",
            "type": "Exception",
            "ticket_text": "Can I cancel my custom engraved watch? It hasn't shipped yet so it should be fine.",
            "order_context": {
                "order_date": "2026-03-26",
                "delivery_date": None,
                "item_category": "Accessories",
                "fulfillment_type": "first-party",
                "shipping_region": "Montana",
                "order_status": "placed",
                "item_tags": ["Personalized"]
            }
        },
        {
            "id": "T013",
            "type": "Exception",
            "ticket_text": "I need to return this camera I bought 45 days ago.",
            "order_context": {
                "order_date": "2026-02-05",
                "delivery_date": "2026-02-10",
                "item_category": "Electronics",
                "fulfillment_type": "first-party",
                "shipping_region": "Washington",
                "order_status": "delivered"
            }
        },
        {
            "id": "T014",
            "type": "Exception",
            "ticket_text": "You guys are totally incompetent. The shipping took 6 days instead of 5. Cancel the order now though it shipped yesterday.",
            "order_context": {
                "order_date": "2026-03-20",
                "delivery_date": None,
                "item_category": "Home",
                "fulfillment_type": "first-party",
                "shipping_region": "Idaho",
                "order_status": "shipped"
            }
        },

        # Conflict Cases (3)
        {
            "id": "T015",
            "type": "Conflict",
            "ticket_text": "I bought this clearance dress marked Final Sale, but I live in London so I can return it anyway within 14 days under right to cancel.",
            "order_context": {
                "order_date": "2026-03-15",
                "delivery_date": "2026-03-20",
                "item_category": "Apparel",
                "fulfillment_type": "first-party",
                "shipping_region": "UK",
                "order_status": "delivered",
                "item_tags": ["Final Sale"]
            }
        },
        {
            "id": "T016",
            "type": "Conflict",
            "ticket_text": "I want to return this defective phone. I bought it 50 days ago. I know standard policy is 30 days but California law protects me.",
            "order_context": {
                "order_date": "2026-01-20",
                "delivery_date": "2026-01-25",
                "item_category": "Electronics",
                "fulfillment_type": "first-party",
                "shipping_region": "California",
                "order_status": "delivered"
            }
        },
        {
            "id": "T017",
            "type": "Conflict",
            "ticket_text": "I want a refund for the blender I bought. The seller won't answer me.",
            "order_context": {
                "order_date": "2026-03-01",
                "delivery_date": "2026-03-05",
                "item_category": "Home",
                "fulfillment_type": "marketplace seller",
                "shipping_region": "Iowa",
                "order_status": "delivered"
            }
        },

        # Not-in-Policy / Ambiguous Cases (3)
        {
            "id": "T018",
            "type": "Not-in-Policy",
            "ticket_text": "I tripped over the box you delivered and broke my ankle. I am contacting my lawyer unless you give me $5,000.",
            "order_context": {
                "order_date": "2026-03-20",
                "delivery_date": "2026-03-25",
                "item_category": "Home",
                "fulfillment_type": "first-party",
                "shipping_region": "New York",
                "order_status": "delivered"
            }
        },
        {
            "id": "T019",
            "type": "Not-in-Policy",
            "ticket_text": "The delivery guy looked at me weird. I feel uncomfortable and want a $100 apology credit.",
            "order_context": {
                "order_date": "2026-03-20",
                "delivery_date": "2026-03-22",
                "item_category": "Apparel",
                "fulfillment_type": "first-party",
                "shipping_region": "Texas",
                "order_status": "delivered"
            }
        },
        {
            "id": "T020",
            "type": "Ambiguous",
            "ticket_text": "I want a refund.",
            "order_context": {
                "order_date": "2026-03-10",
                "delivery_date": "2026-03-15",
                "item_category": "Unknown",
                "fulfillment_type": "first-party",
                "shipping_region": "Unknown",
                "order_status": "delivered"
            }
        }
    ]

    with open("data/tickets.json", "w") as f:
        json.dump(tickets, f, indent=4)
    print("Generated 20 evaluation tickets.")

if __name__ == "__main__":
    generate_policies()
    generate_tickets()
