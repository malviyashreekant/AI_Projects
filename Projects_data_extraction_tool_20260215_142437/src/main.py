import os
from anthropic import Anthropic

SAMPLE_EMAIL = """
From: orders@webstore.com
Subject: Order Confirmation #ORD-2024-5678

Thank you for your order!

Customer: Jane Smith
Email: jane.smith@email.com
Order Total: $234.99
Payment Method: Visa ending in 4242

Items:
- Laptop Stand (x1) - $89.99
- USB-C Cable (x2) - $24.99 each
- Wireless Mouse (x1) - $69.99

Estimated Delivery: February 10, 2024
Tracking: 1Z999AA10123456784
"""

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def extract_order_data(text):
    client = get_client()
    prompt = f"""Extract structured data from this order confirmation email.

Email:
{text}

Output JSON with fields: order_id, customer_name, customer_email, total, delivery_date, tracking_number, items (array)"""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=300,
        temperature=0.1,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Data Extraction Tool ===\n")
    print(extract_order_data(SAMPLE_EMAIL))

if __name__ == "__main__":
    main()
