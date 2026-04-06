import os
from anthropic import Anthropic

SAMPLE_ARTICLES = [
    "Tech stocks surged 5% today as investors showed renewed confidence in AI companies. Major players like NVIDIA and Microsoft led the gains...",
    "Climate summit reaches historic agreement on carbon reduction targets. 195 countries committed to net-zero emissions by 2050...",
    "New study reveals breakthrough in quantum computing. Researchers achieved 99% error correction in quantum processors...",
]

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def summarize_news(articles):
    client = get_client()
    articles_text = "\n\n".join([f"Article {i+1}: {article}" for i, article in enumerate(articles)])
    
    prompt = f"""Summarize these news articles into key insights:

{articles_text}

Provide:
1. Main headlines and key points
2. Common themes across articles
3. Impact analysis
4. Brief summary for each article
5. Overall trends or implications"""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=350,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== News Summarizer ===\n")
    print(summarize_news(SAMPLE_ARTICLES))

if __name__ == "__main__":
    main()
