import os
from anthropic import Anthropic

SAMPLE_RESUME = """
John Smith
Software Engineer
Email: john.smith@email.com
Phone: (555) 123-4567

EXPERIENCE:
Senior Developer at Tech Corp (2020-2024)
- Led team of 5 developers on web applications
- Implemented microservices architecture
- Technologies: Python, React, AWS

Junior Developer at StartupXYZ (2018-2020)  
- Built REST APIs and database systems
- Collaborated on mobile app development

EDUCATION:
BS Computer Science, State University (2016-2018)

SKILLS:
Python, JavaScript, React, Node.js, AWS, Docker, SQL
"""

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def parse_resume(resume_text):
    client = get_client()
    prompt = f"""Parse this resume and extract structured information:

{resume_text}

Extract:
1. Personal information (name, contact)
2. Work experience with dates and responsibilities  
3. Education background
4. Technical skills
5. Years of experience
6. Seniority level assessment"""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=350,
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Resume Parser ===\n")
    print(parse_resume(SAMPLE_RESUME))

if __name__ == "__main__":
    main()
