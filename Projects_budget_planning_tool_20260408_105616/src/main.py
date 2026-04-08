import os
from anthropic import Anthropic

SAMPLE_BUDGET_DATA = {
    "categories": [
        {"name": "Marketing", "allocated": 50000, "spent": 35000, "remaining_months": 8},
        {"name": "R&D", "allocated": 100000, "spent": 60000, "remaining_months": 8},
        {"name": "Operations", "allocated": 75000, "spent": 55000, "remaining_months": 8},
    ],
    "total_budget": 300000,
    "year_progress": 33  # 4 months into 12-month budget
}

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def plan_budget(budget_data):
    client = get_client()
    categories_list = "\n".join([f"- {cat['name']}: ${cat['spent']:,} / ${cat['allocated']:,} spent" 
                                for cat in budget_data['categories']])
    total_spent = sum(cat['spent'] for cat in budget_data['categories'])
    
    prompt = f"""Analyze budget performance and create forecast:

Budget Status ({budget_data['year_progress']}% through the year):
Total Budget: ${budget_data['total_budget']:,}
Total Spent: ${total_spent:,}

Categories:
{categories_list}

Analysis:
1. Spending pace vs. timeline assessment
2. Over/under budget categories
3. Forecast for remaining period
4. Reallocation recommendations
5. Risk factors and mitigation"""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=350,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Budget Planning Tool ===\n")
    print(plan_budget(SAMPLE_BUDGET_DATA))

if __name__ == "__main__":
    main()
