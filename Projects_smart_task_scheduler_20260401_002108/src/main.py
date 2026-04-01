import os
from anthropic import Anthropic

SAMPLE_TASKS = [
    {"name": "Submit quarterly report", "priority": "High", "deadline": "2026-04-15", "estimated_hours": 8},
    {"name": "Team meeting prep", "priority": "Medium", "deadline": "2026-04-05", "estimated_hours": 2},
    {"name": "Code review for Project X", "priority": "High", "deadline": "2026-04-03", "estimated_hours": 4},
    {"name": "Update documentation", "priority": "Low", "deadline": "2026-04-20", "estimated_hours": 6},
]

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def schedule_tasks(tasks):
    client = get_client()
    task_list = "\n".join([f"- {task['name']} (Priority: {task['priority']}, Deadline: {task['deadline']}, Est. {task['estimated_hours']}h)" for task in tasks])
    
    prompt = f"""Analyze these tasks and create an optimal schedule.

Tasks:
{task_list}

Generate a prioritized schedule considering:
1. Deadlines and urgency
2. Task priority levels
3. Estimated effort
4. Resource allocation

Format: Priority order with recommended start dates."""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=300,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Smart Task Scheduler ===\n")
    print(schedule_tasks(SAMPLE_TASKS))

if __name__ == "__main__":
    main()
