import os
from anthropic import Anthropic

SAMPLE_PROCESS = {
    "name": "Customer Onboarding",
    "current_steps": [
        "Manual email verification",
        "PDF document collection", 
        "Manual data entry",
        "Manager approval via email",
        "Account setup in multiple systems"
    ],
    "pain_points": ["Time consuming", "Error prone", "Manual bottlenecks"]
}

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def design_workflow_automation(process_data):
    client = get_client()
    steps_list = "\n".join([f"- {step}" for step in process_data['current_steps']])
    issues_list = ", ".join(process_data['pain_points'])
    
    prompt = f"""Design an automated workflow for this business process:

Process: {process_data['name']}

Current Steps:
{steps_list}

Pain Points: {issues_list}

Design:
1. Optimized workflow with automation opportunities
2. Technology recommendations
3. Integration points
4. Time/cost savings estimation
5. Implementation roadmap"""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=400,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Workflow Automation Designer ===\n")
    print(design_workflow_automation(SAMPLE_PROCESS))

if __name__ == "__main__":
    main()
