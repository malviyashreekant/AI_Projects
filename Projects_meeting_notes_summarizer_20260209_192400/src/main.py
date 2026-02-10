import os
from anthropic import Anthropic

SAMPLE_TRANSCRIPT = """
John: Let's discuss Q1 roadmap. Top priority is mobile app launch.
Sarah: Agree. We need design mockups by Feb 15. I'll coordinate with design team.
Mike: Backend APIs are 80% done. Should finish by Feb 10.
John: Great. Sarah, can you also schedule user testing for March 1?
Sarah: Will do. I'll send calendar invites this week.
Mike: One blocker - we need final sign-off on data schema.
John: I'll get that approved by Friday. Any other concerns?
Sarah: All good. Let's sync again next Monday.
"""

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def summarize_meeting(transcript):
    client = get_client()
    prompt = f"""Summarize this meeting transcript.

Extract:
1. Key decisions
2. Action items (who, what, when)
3. Next steps

Transcript:
{transcript}"""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=300,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Meeting Notes Summarizer ===\n")
    print(summarize_meeting(SAMPLE_TRANSCRIPT))

if __name__ == "__main__":
    main()
