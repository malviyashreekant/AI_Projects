import os
from anthropic import Anthropic

# Sample emails for demonstration
SAMPLE_EMAILS = [
    {"from": "customer@example.com", "subject": "Order Status", "body": "Hi, I ordered product #12345 last week. Can you check the delivery status?"},
    {"from": "support@vendor.com", "subject": "Meeting Request", "body": "Would you be available for a call on Friday at 2 PM to discuss the integration?"},
    {"from": "info@newsletter.com", "subject": "Unsubscribe", "body": "Please remove me from your marketing list."},
]

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def generate_response(email):
    client = get_client()
    prompt = f"""Generate a professional email response.

From: {email['from']}
Subject: {email['subject']}
Body: {email['body']}

Write a helpful, concise response (2-3 sentences)."""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=200,
        temperature=0.7,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Email Auto-Responder ===\n")
    for i, email in enumerate(SAMPLE_EMAILS, 1):
        print(f"Email {i}: {email['subject']}")
        print(f"Response:\n{generate_response(email)}\n")

if __name__ == "__main__":
    main()
