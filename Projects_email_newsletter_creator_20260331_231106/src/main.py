import os
from anthropic import Anthropic

SAMPLE_CONTENT = {
    "topic": "Technology Updates",
    "articles": [
        "AI breakthrough in medical diagnosis",
        "New smartphone with 200MP camera released",  
        "Quantum computing milestone achieved"
    ],
    "audience": "Tech enthusiasts",
    "tone": "professional yet engaging"
}

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def create_newsletter(content_data):
    client = get_client()
    articles_list = "\n".join([f"- {article}" for article in content_data['articles']])
    
    prompt = f"""Create an engaging email newsletter:

Topic: {content_data['topic']}
Target audience: {content_data['audience']}
Tone: {content_data['tone']}

Content to include:
{articles_list}

Generate:
1. Compelling subject line
2. Newsletter header/intro
3. Article summaries with engaging headlines
4. Call-to-action sections
5. Footer with unsubscribe info"""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=400,
        temperature=0.4,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Email Newsletter Creator ===\n")
    print(create_newsletter(SAMPLE_CONTENT))

if __name__ == "__main__":
    main()
