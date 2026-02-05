import os
from anthropic import Anthropic

SAMPLE_REVIEWS = [
    "Love this product! Setup was easy and support team was super helpful. 5 stars!",
    "Good overall but the mobile app crashes frequently. Desktop version works fine.",
    "Disappointed. Features promised in marketing don't work as expected. Refund requested.",
    "Been using for 3 months. Solid tool, fair price. Wish it had better integrations.",
]

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def analyze_review(review):
    client = get_client()
    prompt = f"""Analyze this customer review and extract:
1. Sentiment (positive/negative/mixed)
2. Key themes (comma-separated)
3. Action items (if any)

Review: {review}

Format:
Sentiment: 
Themes: 
Action:"""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=150,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Customer Review Analyzer ===\n")
    for i, review in enumerate(SAMPLE_REVIEWS, 1):
        print(f"Review {i}: {review}")
        print(f"{analyze_review(review)}\n")

if __name__ == "__main__":
    main()
