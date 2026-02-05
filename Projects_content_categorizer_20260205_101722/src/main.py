import os
from anthropic import Anthropic

CATEGORIES = ["Technology", "Business", "Health", "Education", "Entertainment"]

SAMPLE_ARTICLES = [
    "New AI model achieves breakthrough in natural language understanding, outperforming previous benchmarks.",
    "Market analysis shows tech stocks rising amid strong Q4 earnings reports from major companies.",
    "Study reveals regular exercise reduces risk of chronic diseases by up to 40 percent.",
]

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def categorize_content(text):
    client = get_client()
    prompt = f"""Categorize this content into one or more categories: {', '.join(CATEGORIES)}

Content: {text}

Respond with categories (comma-separated) and confidence (high/medium/low)."""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=100,
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Content Categorizer ===\n")
    for i, article in enumerate(SAMPLE_ARTICLES, 1):
        print(f"Article {i}: {article[:60]}...")
        print(f"Categories: {categorize_content(article)}\n")

if __name__ == "__main__":
    main()
