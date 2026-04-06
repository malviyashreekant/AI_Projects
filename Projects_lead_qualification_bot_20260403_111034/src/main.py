import os
from anthropic import Anthropic

SAMPLE_LEADS = [
    {"name": "John Corp", "company_size": "500 employees", "budget": "$50k", "timeline": "Q2 2026", "pain_points": "Manual processes, data silos"},
    {"name": "Small Biz", "company_size": "10 employees", "budget": "$5k", "timeline": "Next year", "pain_points": "Cost management"},
    {"name": "Enterprise Ltd", "company_size": "2000 employees", "budget": "$200k", "timeline": "ASAP", "pain_points": "Scalability issues"}
]

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def qualify_leads(leads):
    client = get_client()
    leads_list = "\n".join([f"- {lead['name']}: {lead['company_size']}, Budget: {lead['budget']}, Timeline: {lead['timeline']}, Issues: {lead['pain_points']}" 
                           for lead in leads])
    
    prompt = f"""Qualify these leads and prioritize for sales outreach:

Leads:
{leads_list}

For each lead provide:
1. Qualification score (1-10)
2. Buying signals strength
3. Sales priority (High/Medium/Low)
4. Recommended approach/messaging
5. Next steps for engagement"""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=400,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Lead Qualification Bot ===\n")
    print(qualify_leads(SAMPLE_LEADS))

if __name__ == "__main__":
    main()
