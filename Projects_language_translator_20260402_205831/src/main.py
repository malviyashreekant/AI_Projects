import os
from anthropic import Anthropic

SAMPLE_TEXTS = [
    {"text": "Hello, how are you today?", "target_language": "Spanish"},
    {"text": "The meeting is scheduled for tomorrow at 3 PM.", "target_language": "French"},
    {"text": "Please send me the report by Friday.", "target_language": "German"},
]

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def translate_text(text, target_language):
    client = get_client()
    prompt = f"""Translate the following text to {target_language}, preserving tone and context:

Original text: "{text}"

Provide:
1. Direct translation
2. Cultural context notes (if relevant)
3. Alternative phrasings for different formality levels"""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=200,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Language Translator ===\n")
    for i, item in enumerate(SAMPLE_TEXTS, 1):
        print(f"Translation {i} ({item['target_language']}):")
        print(f"Original: {item['text']}")
        print(f"Result:\n{translate_text(item['text'], item['target_language'])}\n")

if __name__ == "__main__":
    main()
