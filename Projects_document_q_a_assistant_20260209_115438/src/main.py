import os
from anthropic import Anthropic

COMPANY_HANDBOOK = """
Vacation Policy: Employees accrue 15 days PTO per year. Must request 2 weeks in advance.
Remote Work: Hybrid schedule - 3 days in office, 2 days remote. Full remote requires manager approval.
Health Benefits: Medical, dental, vision coverage starts after 30 days. Company pays 80% of premiums.
Performance Reviews: Conducted quarterly. Raises based on performance and market data.
"""

SAMPLE_QUESTIONS = [
    "How many vacation days do I get?",
    "When does health insurance start?",
    "What's the remote work policy?",
]

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def answer_from_document(question):
    client = get_client()
    prompt = f"""Answer the question using only information from the document.

Document:
{COMPANY_HANDBOOK}

Question: {question}

Answer:"""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=150,
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Document Q&A Assistant ===\n")
    for q in SAMPLE_QUESTIONS:
        print(f"Q: {q}")
        print(f"A: {answer_from_document(q)}\n")

if __name__ == "__main__":
    main()
