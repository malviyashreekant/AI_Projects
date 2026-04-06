import os
from anthropic import Anthropic

SAMPLE_PROJECT = {
    "name": "Mobile App Development",
    "milestones": [
        {"name": "UI Design", "due": "2026-04-10", "status": "Completed", "progress": 100},
        {"name": "Backend API", "due": "2026-04-20", "status": "In Progress", "progress": 75},
        {"name": "Testing", "due": "2026-04-30", "status": "Not Started", "progress": 0},
        {"name": "Deployment", "due": "2026-05-05", "status": "Not Started", "progress": 0},
    ],
    "team_size": 5,
    "budget_used": 60
}

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def track_progress(project_data):
    client = get_client()
    milestones_list = "\n".join([f"- {ms['name']}: {ms['status']} ({ms['progress']}%) - Due: {ms['due']}" 
                                 for ms in project_data['milestones']])
    
    prompt = f"""Analyze project progress and provide insights:

Project: {project_data['name']}
Team Size: {project_data['team_size']}
Budget Used: {project_data['budget_used']}%

Milestones:
{milestones_list}

Analysis:
1. Overall project health assessment
2. Risk factors and potential delays
3. Resource allocation recommendations
4. Next steps and priorities
5. Timeline optimization suggestions"""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=350,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Project Progress Tracker ===\n")
    print(track_progress(SAMPLE_PROJECT))

if __name__ == "__main__":
    main()
