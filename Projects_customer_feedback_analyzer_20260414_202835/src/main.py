import os
from anthropic import Anthropic

SAMPLE_FEEDBACK = [
    {"source": "Survey", "rating": 4, "comment": "Great product but delivery was slow"},
    {"source": "Support Chat", "rating": 5, "comment": "Excellent customer service, very helpful"},
    {"source": "App Review", "rating": 2, "comment": "App crashes frequently, needs bug fixes"},
    {"source": "Email", "rating": 4, "comment": "Love the features but UI could be more intuitive"}
]

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def analyze_feedback(feedback_data):
    client = get_client()
    feedback_list = "\n".join([f"- {fb['source']} ({fb['rating']}/5): {fb['comment']}" for fb in feedback_data])
    avg_rating = sum(fb['rating'] for fb in feedback_data) / len(feedback_data)
    
    prompt = f"""Analyze customer feedback for insights and action items:

Feedback (Avg Rating: {avg_rating:.1f}/5):
{feedback_list}

Analysis:
1. Key themes and sentiment patterns
2. Critical issues requiring immediate attention
3. Positive feedback to leverage
4. Improvement recommendations
5. Customer satisfaction trends"""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=350,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Customer Feedback Analyzer ===\n")
    print(analyze_feedback(SAMPLE_FEEDBACK))

if __name__ == "__main__":
    main()
