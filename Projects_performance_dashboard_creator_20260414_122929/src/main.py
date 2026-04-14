import os
from anthropic import Anthropic

SAMPLE_METRICS = {
    "sales": {"current": 150000, "target": 200000, "last_month": 140000},
    "conversion_rate": {"current": 2.5, "target": 3.0, "last_month": 2.3},
    "customer_satisfaction": {"current": 8.2, "target": 9.0, "last_month": 8.0},
    "website_traffic": {"current": 50000, "target": 60000, "last_month": 45000}
}

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def create_dashboard_insights(metrics_data):
    client = get_client()
    metrics_list = "\n".join([f"- {name}: Current={data['current']}, Target={data['target']}, Last Month={data['last_month']}" 
                             for name, data in metrics_data.items()])
    
    prompt = f"""Create dashboard insights and visualizations:

Key Metrics:
{metrics_list}

Dashboard Design:
1. KPI summary with status indicators
2. Trend analysis and performance insights  
3. Goal achievement tracking
4. Alert recommendations for metrics
5. Suggested chart types for visualization"""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=300,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Performance Dashboard Creator ===\n")
    print(create_dashboard_insights(SAMPLE_METRICS))

if __name__ == "__main__":
    main()
