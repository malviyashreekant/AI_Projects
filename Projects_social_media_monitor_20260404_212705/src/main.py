import os
from anthropic import Anthropic

SAMPLE_MENTIONS = [
    {"platform": "Twitter", "content": "Love the new features in @YourBrand app! Great update!", "sentiment": "positive"},
    {"platform": "Facebook", "content": "Had issues with customer service today. Not impressed.", "sentiment": "negative"}, 
    {"platform": "Instagram", "content": "Their product quality has really improved lately", "sentiment": "positive"},
    {"platform": "LinkedIn", "content": "Excited to partner with @YourBrand on our next project", "sentiment": "positive"},
]

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def analyze_social_mentions(mentions):
    client = get_client()
    mention_list = "\n".join([f"- {mention['platform']}: '{mention['content']}'" for mention in mentions])
    
    prompt = f"""Analyze these social media mentions:

{mention_list}

Provide:
1. Overall sentiment analysis
2. Key themes and topics
3. Engagement opportunities
4. Brand perception insights
5. Recommended responses or actions"""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=300,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Social Media Monitor ===\n")
    print(analyze_social_mentions(SAMPLE_MENTIONS))

if __name__ == "__main__":
    main()
