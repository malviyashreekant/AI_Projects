import os
from anthropic import Anthropic

SAMPLE_QUERIES = [
    "How do I reset my password?",
    "Analyze sales trends from Q3 data in attached spreadsheet",
    "What's your refund policy?",
    "Calculate compound interest for $10000 at 5% over 10 years",
]

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def classify_and_route(query):
    client = get_client()
    prompt = f"""Classify this query and route to the appropriate handler.

Handlers:
- FAQ: Simple policy/process questions
- SUPPORT: Technical issues requiring human help
- ANALYTICS: Data analysis requests
- CALCULATOR: Math/computation tasks

Query: {query}

Respond with: Handler name, Confidence (high/medium/low), Brief reasoning"""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=150,
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Intelligent Query Router ===\n")
    for i, query in enumerate(SAMPLE_QUERIES, 1):
        print(f"Query {i}: {query}")
        print(f"Routing: {classify_and_route(query)}\n")

if __name__ == "__main__":
    main()
