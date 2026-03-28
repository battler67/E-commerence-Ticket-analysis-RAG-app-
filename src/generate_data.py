import os
import json

def generate_policies():
    policies_dir = "data/policies"
    os.makedirs(policies_dir, exist_ok=True)
    
    policies = {
        "Refund_Policy.md": """# General Refund Policy
Purple Merit Technologies strives to ensure complete customer satisfaction through a structured and comprehensive refund process. 
- **Standard Return Window:** You have 30 days from the confirmed delivery date to return an eligible item for a full refund. This timeframe is strictly enforced based on carrier tracking data.
- **Condition of Returned Items:** To be eligible for a full refund, items must be in their original, unused condition. All tags must be attached, and the item must be returned in its original packaging. Items that show signs of wear, alteration, or damage caused by the customer will incur a restocking fee of up to 50% or may be rejected outright.
- **Refund Processing Time:** Refunds will be issued strictly to the original payment method utilized during checkout. Processing typically occurs within 5-7 business days from the date our warehouse receives and inspects the return.
- **Lost or Undelivered Items:** Items lacking an official 'delivered' order status cannot be refunded until their status is explicitly confirmed as 'lost' by the carrier. 
- **Restocking Fees:** Certain high-value electronics and heavy home goods are subject to a 15% restocking fee unless the item is verified as defective upon arrival.
""",
        "Returns_Exceptions.md": """# Return Exceptions Policy
To maintain health standards and honor vendor agreements, certain items are subject to stringent return restrictions:
- **Final Sale & Clearance**: Any items explicitly marked "Final Sale," "Clearance," or discounted by 50% or more at the time of purchase cannot be returned, exchanged, or refunded under any circumstances. This policy overrides all standard return windows.
- **Hygiene & Intimate Items**: Underwear, swimwear, earrings, and personal grooming devices can only be returned if they remain fully sealed in their original, tamper-proof packaging. Opened hygiene items present a biological hazard and are strictly non-refundable. If such items are mailed back, they will be destroyed without compensation.
- **Perishables**: Food, flowers, live plants, and other temperature-sensitive or perishable items cannot be returned due to spoilage risks. However, if they arrive damaged, wilted, or spoiled, customers may request a full refund within 48 hours of delivery. This request MUST be accompanied by clear photographic evidence of the damage and the shipping box.
- **Customized Items**: Personalized or custom-engraved items are crafted specifically to user specifications and are strictly non-refundable and non-cancellable once production has begun.
""",
        "Cancellations.md": """# Order Cancellation Policy
Purple Merit Technologies processes orders rapidly to ensure fast delivery.
- **Pre-Shipment Cancellation:** Orders can be freely canceled for a full refund only while the order status is 'placed' or 'processing'.
- **Post-Shipment Restrictions:** Once an order's status transitions to 'shipped' or 'delivered' or a tracking number is generated, the order is locked and cannot be canceled under any circumstances. The customer must wait for delivery and initiate a standard return.
- **Digital Products:** Software keys, downloadable media, and digital gift cards are delivered instantly upon purchase and are absolutely excluded from cancellations and refunds.
""",
        "Shipping_Delivery.md": """# Shipping and Delivery Policy
We offer various shipping tiers to meet customer needs.
- **Timeframes:** Standard shipping generally takes 3-5 business days. Expedited shipping guarantees delivery within 1-2 business days.
- **Lost Packages & Carrier Scans:** If a carrier tracking system indicates a package is 'delivered' but the customer denies receipt, support must instruct the customer to wait exactly 48 hours before filing a formal claim. Carriers frequently pre-scan packages as delivered up to two days before actual drop-off. If the package remains missing after 48 hours, support will cross-reference GPS drop-off data and, if appropriate, offer a free replacement or refund.
- **Delayed Expedited Orders:** We do not compensate for minor delays on standard shipping. However, if a customer paid a premium for expedited shipping and the delivery is delayed due to our failure or carrier failure, the expedited shipping fees must be fully refunded to the customer.
""",
        "Promotions_Coupons.md": """# Promotions, Coupons, and Price Adjustments
- **Stacking Restrictions:** Our system allows only one (1) promotional code, coupon, or discount to be applied per single order. Stacking codes is prohibited.
- **Welcome Bonuses:** Welcome coupons (e.g., WELCOME10, NEWBIE20) are strictly valid for first-time purchasers only. If a user creates multiple accounts to abuse Welcome promos, they will be flagged for fraud.
- **Retroactive Application:** If a customer forgets to apply a valid, active coupon code during checkout, our support agents are authorized to retroactively apply the code and issue a partial refund for the difference. However, this exception is ONLY valid if the customer submits the request within 24 hours of placing the order.
- **Price Matching:** We do not offer post-purchase price matching if an item goes on sale after a customer has purchased it.
""",
        "Disputes_Damaged.md": """# Damaged, Defective, or Incorrect Items
We take quality control seriously and have specific dispute workflows.
- **Damaged on Arrival:** If an item arrives physically damaged, the customer is entitled to a full refund or a free replacement without needing to return the shattered/broken item. Photographic proof is required for items over $50.
- **Incorrect Item Received:** If the warehouse ships the wrong color, size, or explicit item (e.g. blue instead of red), the order is considered 'incorrect'. The customer must return the incorrect item using a prepaid label we provide. A refund or the correct replacement dispatch will only be authorized AFTER the tracking number on the return label shows movement.
- **Electronics Troubleshooting:** Before any refund or replacement is authorized for an electronic device claiming a "technical defect," the customer must undergo basic troubleshooting steps or verify they contacted the manufacturer's warranty department.
""",
        "Marketplace_Sellers.md": """# Third-Party Marketplace Seller Policy
Purple Merit Technologies acts as a platform host for various independent third-party sellers.
- **Fulfillment Distinction:** Support agents MUST verify the `fulfillment_type`. If it is 'marketplace seller', Purple Merit's standard return policies do NOT apply. The third-party seller sets their own return and refund rules.
- **Direct Contact Required:** Customers must initiate returns and disputes by contacting the marketplace seller directly through our messaging portal.
- **A-Z Guarantee Escalation:** Purple Merit Technologies Support is strictly prohibited from issuing refunds for marketplace orders directly, EXCEPT under our "A-Z Guarantee". The A-Z Guarantee is triggered ONLY if the customer proves they messaged the seller and the seller failed to respond within 3 full business days. If this condition is met, Purple Merit will force a refund.
""",
        "Regional_Differences.md": """# Regional Compliance Policy
Local and international commerce laws supersede standard corporate policies. Agents must verify the `shipping_region`.
- **California Electronics Law:** Customers residing in California are legally entitled to return electronic devices for up to 60 days from purchase. This directly supersedes our standard 30-day corporate return window for electronics.
- **EU/UK Right to Cancel:** Customers based in the European Union or the United Kingdom are protected by distance selling laws. They retain a strict "cooling-off" period of 14 days, during which they can return ANY order for ANY reason. This regional law overrides our "Final Sale" and "Clearance" restrictions. Note: Perishables and custom personalized items remain exempt from the cooling-off period.
- **New York Apparel Regulations:** In the state of New York, apparel and clothing returns must be accepted for up to 45 days.
""",
        "Missing_Items.md": """# Missing Items from Multi-Item Orders
- **Split Shipments:** It is common for large orders containing multiple categories to be split into separate shipments from different fulfillment centers. Before assuming an item is missing, support must verify the individual shipping status of all items in an order.
- **Verification:** If an order shows multiple items consolidated and delivered in one box, but the customer claims one item is entirely missing, the customer must check the packaging thoroughly. 
- **Resolution:** If verified that the warehouse failed to pack the item, a partial refund or expedited replacement for the exact missing item must be provided immediately. No formal dispute process is required.
""",
        "Exchanges.md": """# Product Exchanges Workflow
- **No Direct Exchanges:** Due to the complexities of inventory management, we currently do not process direct exchanges for any single item (e.g., swapping a size Medium for a size Large).
- **Required Protocol:** Customers wishing to exchange a product must first return the original item for a standard refund, and subsequently place an entirely new order for the desired size or color.
- **Support Action:** If a customer opens a ticket explicitly asking for an exchange, support agents should politely decline the direct exchange and provide them a link to the self-service returns portal, instructing them to re-order the correct item.
""",
        "Gift_Cards.md": """# Gift Card and Store Credit Policy
- **Non-Refundable:** Both Physical and Digital Gift Cards are strictly non-refundable and cannot be redeemed for cash, except in states or regions where explicitly required by law.
- **Return Credits:** If a customer returns a physical item that was originally paid for using a gift card, the refunded amount will be credited directly back to the original gift card balance or issued as digital store credit. It cannot be converted to a credit card refund.
""",
        "Escalations_Abuse.md": """# Policy on Support Abuse, Harassment, and Legal Escalations
Purple Merit Technologies maintains a zero-tolerance policy against employee abuse and fraudulent extortion.
- **Abusive Language:** Customers who utilize profanity, derogatory language, or personal attacks against support agents must receive precisely one formal warning. If the abuse persists in subsequent messages, the ticket must be immediately closed without resolution and the user's account flagged.
- **Extortion & Unwarranted Compensation:** Any demand for arbitrary compensation, free items, or apology credits simply because a customer is mildly dissatisfied or "felt uncomfortable"—with no actual underlying policy violation or physical damage—MUST be categorically denied. Support agents must never invent ad-hoc non-policy resolutions to appease demanding customers.
- **Legal Action Threats:** If a customer threatens lawsuits, involves lawyers, mentions contacting the Better Business Bureau (BBB), or threatens physical harm, support agents are strictly prohibited from attempting to resolve the issue directly. The ticket must be instantly escalated to the Legal Escalations Team.
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
