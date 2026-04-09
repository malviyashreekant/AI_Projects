import os
from anthropic import Anthropic

SAMPLE_COMPLIANCE_ITEMS = [
    {"requirement": "GDPR Data Protection", "status": "Compliant", "last_audit": "2026-02-15"},
    {"requirement": "SOX Financial Controls", "status": "Needs Review", "last_audit": "2025-12-01"},
    {"requirement": "ISO 27001 Security", "status": "Non-compliant", "last_audit": "2026-01-20"},
    {"requirement": "HIPAA Privacy Rules", "status": "Compliant", "last_audit": "2026-03-01"},
]

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def monitor_compliance(compliance_data):
    client = get_client()
    items_list = "\n".join([f"- {item['requirement']}: {item['status']} (Last audit: {item['last_audit']})" 
                           for item in compliance_data])
    
    prompt = f"""Monitor compliance status and generate recommendations:

Compliance Items:
{items_list}

Report:
1. Compliance status summary
2. Critical non-compliance issues
3. Upcoming audit requirements
4. Risk assessment and mitigation
5. Action plan for improvements"""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=300,
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Compliance Monitor ===\n")
    print(monitor_compliance(SAMPLE_COMPLIANCE_ITEMS))

if __name__ == "__main__":
    main()
