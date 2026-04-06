import os
from anthropic import Anthropic

SAMPLE_EXPENSES = [
    {"date": "2026-03-15", "category": "Travel", "amount": 245.50, "description": "Flight to conference"},
    {"date": "2026-03-16", "category": "Meals", "amount": 89.20, "description": "Client dinner"},
    {"date": "2026-03-17", "category": "Office Supplies", "amount": 156.75, "description": "Equipment purchase"},
    {"date": "2026-03-18", "category": "Travel", "amount": 45.00, "description": "Taxi fare"},
]

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def analyze_expenses(expenses):
    client = get_client()
    expense_list = "\n".join([f"- {exp['date']}: {exp['category']} - ${exp['amount']} ({exp['description']})" for exp in expenses])
    total = sum(exp['amount'] for exp in expenses)
    
    prompt = f"""Analyze this expense report for policy compliance and optimization:

Expenses:
{expense_list}
Total: ${total:.2f}

Provide:
1. Category breakdown and spending patterns
2. Policy compliance check (reasonable amounts, proper categories)
3. Cost optimization suggestions
4. Any red flags or anomalies"""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=300,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Expense Report Analyzer ===\n")
    print(analyze_expenses(SAMPLE_EXPENSES))

if __name__ == "__main__":
    main()
