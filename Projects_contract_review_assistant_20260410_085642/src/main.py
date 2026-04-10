import os
from anthropic import Anthropic

SAMPLE_CONTRACT = """
Service Agreement between Company A and Vendor B
- Term: 24 months starting January 1, 2026
- Payment: $10,000 monthly, net 30 days
- Termination: Either party with 90 days notice
- No liability limitation clause
- Vendor owns all IP created during engagement
- Auto-renewal unless canceled 60 days prior
- Exclusive supplier arrangement
"""

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def review_contract(contract_text):
    client = get_client()
    prompt = f"""Review this contract for risks and key terms:

{contract_text}

Analysis:
1. Key terms and obligations summary
2. Risk factors and red flags
3. Missing or problematic clauses
4. Negotiation recommendations
5. Legal/compliance considerations"""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=350,
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Contract Review Assistant ===\n")
    print(review_contract(SAMPLE_CONTRACT))

if __name__ == "__main__":
    main()
