import os
from anthropic import Anthropic

SAMPLE_FILES = [
    {"name": "report_q1.pdf", "size": "2.3MB", "date": "2026-03-15"},
    {"name": "vacation_photos.zip", "size": "45MB", "date": "2026-02-20"},
    {"name": "budget_2026.xlsx", "size": "1.2MB", "date": "2026-01-10"},
    {"name": "meeting_notes.docx", "size": "500KB", "date": "2026-03-25"},
    {"name": "project_code.zip", "size": "15MB", "date": "2026-03-20"},
]

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def organize_files(files):
    client = get_client()
    files_list = "\n".join([f"- {file['name']} ({file['size']}, {file['date']})" for file in files])
    
    prompt = f"""Analyze these files and suggest an organization structure:

Files:
{files_list}

Provide:
1. Suggested folder structure
2. File categorization rules
3. Naming conventions
4. Archive/cleanup recommendations
5. Organization rationale"""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=300,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== File Organizer ===\n")
    print(organize_files(SAMPLE_FILES))

if __name__ == "__main__":
    main()
