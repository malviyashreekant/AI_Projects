import os
from anthropic import Anthropic

SAMPLE_ARTICLE = """
Breaking: Tech Giant Announces Record Quarterly Earnings

XYZ Corp reported Q4 revenue of $52 billion, exceeding analyst expectations by 12%. 
CEO stated AI investments driving growth. Stock jumped 8% in after-hours trading.
Company also announced 1000 new AI researcher hires for 2024.
"""

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def extract_facts(text):
    client = get_client()
    prompt = f"Extract key facts as bullet points from:\n{text}"
    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=150, temperature=0.2,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def summarize(text):
    client = get_client()
    prompt = f"Summarize in one sentence:\n{text}"
    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=100, temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def categorize(text):
    client = get_client()
    prompt = f"Categorize (Business/Tech/Finance/Other):\n{text}"
    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=50, temperature=0.1,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Multi-Step Content Pipeline ===\n")
    print("Step 1 - Extract Facts:")
    facts = extract_facts(SAMPLE_ARTICLE)
    print(facts)
    
    print("\nStep 2 - Summarize:")
    summary = summarize(facts)
    print(summary)
    
    print("\nStep 3 - Categorize:")
    category = categorize(summary)
    print(category)

if __name__ == "__main__":
    main()
