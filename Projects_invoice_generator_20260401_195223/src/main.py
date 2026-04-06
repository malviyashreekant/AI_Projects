import os
from anthropic import Anthropic

SAMPLE_WORK_DATA = {
    "client": "ABC Corporation",
    "project": "Website Development", 
    "work_items": [
        {"description": "Frontend development", "hours": 40, "rate": 75},
        {"description": "Backend API development", "hours": 32, "rate": 85},
        {"description": "Database setup", "hours": 16, "rate": 80},
        {"description": "Testing and deployment", "hours": 12, "rate": 70},
    ],
    "invoice_date": "2026-03-31",
    "due_date": "2026-04-30"
}

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def generate_invoice(work_data):
    client = get_client()
    work_items = "\n".join([f"- {item['description']}: {item['hours']} hrs @ ${item['rate']}/hr = ${item['hours'] * item['rate']}" 
                            for item in work_data['work_items']])
    total = sum(item['hours'] * item['rate'] for item in work_data['work_items'])
    
    prompt = f"""Generate a professional invoice:

Client: {work_data['client']}
Project: {work_data['project']}
Invoice Date: {work_data['invoice_date']}
Due Date: {work_data['due_date']}

Work Items:
{work_items}

Total: ${total}

Create formatted invoice with:
1. Professional header
2. Itemized work breakdown  
3. Subtotal, tax (if applicable), total
4. Payment terms and instructions"""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=350,
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Invoice Generator ===\n")
    print(generate_invoice(SAMPLE_WORK_DATA))

if __name__ == "__main__":
    main()
