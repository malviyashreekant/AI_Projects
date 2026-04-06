import os
from anthropic import Anthropic

SAMPLE_LEARNING_OBJECTIVES = [
    "Understand Python fundamentals and syntax",
    "Learn object-oriented programming concepts", 
    "Master data structures and algorithms",
    "Build web applications with Flask/Django",
]

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def create_training_content(objectives):
    client = get_client()
    objectives_list = "\n".join([f"- {obj}" for obj in objectives])
    
    prompt = f"""Create comprehensive training content for these learning objectives:

{objectives_list}

Include:
1. Structured lesson outline
2. Key concepts to cover
3. Practical exercises
4. Assessment questions
5. Resources and next steps"""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=400,
        temperature=0.4,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Training Content Creator ===\n")
    print(create_training_content(SAMPLE_LEARNING_OBJECTIVES))

if __name__ == "__main__":
    main()
