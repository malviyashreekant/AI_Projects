import os
from anthropic import Anthropic

SAMPLE_CODE = """
def calculate_total(items):
    total = 0
    for item in items:
        if item['price'] > 0:
            total = total + item['price']
    return total

class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        
    def get_info(self):
        return self.name + " (" + self.email + ")"
"""

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def check_code_quality(code):
    client = get_client()
    prompt = f"""Analyze this code for quality, best practices, and potential issues:

{code}

Provide:
1. Code style and formatting issues
2. Performance optimizations
3. Security vulnerabilities  
4. Best practice violations
5. Refactoring suggestions
6. Overall quality score (1-10)"""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=400,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Code Quality Checker ===\n")
    print(check_code_quality(SAMPLE_CODE))

if __name__ == "__main__":
    main()
