import os
from anthropic import Anthropic

SAMPLE_CODE = """
def calculate_discount(price, customer_tier, quantity):
    base_discount = 0.0
    if customer_tier == "gold":
        base_discount = 0.15
    elif customer_tier == "silver":
        base_discount = 0.10
    elif customer_tier == "bronze":
        base_discount = 0.05
    
    bulk_discount = min(quantity * 0.01, 0.20)
    total_discount = min(base_discount + bulk_discount, 0.30)
    return price * (1 - total_discount)
"""

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def generate_docs(code):
    client = get_client()
    prompt = f"""Generate comprehensive documentation for this function.

Include:
1. Clear docstring
2. Parameter descriptions
3. Return value description
4. Example usage

Code:
{code}"""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=400,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Code Documentation Generator ===\n")
    print(generate_docs(SAMPLE_CODE))

if __name__ == "__main__":
    main()
