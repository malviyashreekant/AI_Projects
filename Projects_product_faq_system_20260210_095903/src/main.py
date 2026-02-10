import os
from anthropic import Anthropic

# Sample product knowledge base
KNOWLEDGE_BASE = [
    "Our Pro plan costs $49/month and includes unlimited users, 100GB storage, and priority support.",
    "Free trial lasts 14 days with full access to Pro features. No credit card required.",
    "You can upgrade or downgrade your plan anytime from the billing section.",
    "We accept Visa, Mastercard, American Express, and PayPal.",
    "Data is encrypted at rest and in transit. We're SOC 2 Type II certified.",
    "API rate limits: Free tier 100 req/hour, Pro tier 1000 req/hour.",
]

SAMPLE_QUESTIONS = [
    "How much does the Pro plan cost?",
    "Do I need a credit card for the trial?",
    "What payment methods do you accept?",
]

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def retrieve_relevant_docs(question, docs, top_k=3):
    """Simple keyword-based retrieval"""
    question_words = set(question.lower().split())
    scored = []
    for doc in docs:
        doc_words = set(doc.lower().split())
        score = len(question_words & doc_words)
        scored.append((score, doc))
    scored.sort(reverse=True, key=lambda x: x[0])
    return [doc for _, doc in scored[:top_k]]

def answer_question(question):
    context = retrieve_relevant_docs(question, KNOWLEDGE_BASE)
    client = get_client()
    
    prompt = f"""Answer the question using only the provided context.

Context:
{chr(10).join(f"- {doc}" for doc in context)}

Question: {question}

Answer concisely and accurately."""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=150,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Product FAQ System ===\n")
    for q in SAMPLE_QUESTIONS:
        print(f"Q: {q}")
        print(f"A: {answer_question(q)}\n")

if __name__ == "__main__":
    main()
