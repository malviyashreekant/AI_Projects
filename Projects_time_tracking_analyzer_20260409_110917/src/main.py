import os
from anthropic import Anthropic

SAMPLE_TIME_DATA = [
    {"task": "Code Development", "hours": 32, "productivity": "High"},
    {"task": "Meetings", "hours": 12, "productivity": "Medium"},
    {"task": "Email/Admin", "hours": 8, "productivity": "Low"},
    {"task": "Learning/Research", "hours": 6, "productivity": "High"},
    {"task": "Bug Fixes", "hours": 10, "productivity": "Medium"},
]

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def analyze_time_tracking(time_data):
    client = get_client()
    time_list = "\n".join([f"- {task['task']}: {task['hours']} hours ({task['productivity']} productivity)" 
                          for task in time_data])
    total_hours = sum(task['hours'] for task in time_data)
    
    prompt = f"""Analyze time allocation and productivity patterns:

Weekly Time Breakdown ({total_hours} total hours):
{time_list}

Analysis:
1. Productivity assessment by activity
2. Time allocation optimization suggestions
3. Bottleneck identification
4. Efficiency improvement recommendations
5. Work-life balance insights"""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=300,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Time Tracking Analyzer ===\n")
    print(analyze_time_tracking(SAMPLE_TIME_DATA))

if __name__ == "__main__":
    main()
