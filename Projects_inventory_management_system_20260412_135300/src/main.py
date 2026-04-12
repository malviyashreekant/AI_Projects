import os
from anthropic import Anthropic

SAMPLE_INVENTORY = [
    {"item": "Widget A", "current_stock": 45, "reorder_point": 20, "monthly_usage": 15},
    {"item": "Component B", "current_stock": 8, "reorder_point": 25, "monthly_usage": 30},
    {"item": "Tool C", "current_stock": 120, "reorder_point": 50, "monthly_usage": 10},
]

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def analyze_inventory(inventory_data):
    client = get_client()
    inventory_list = "\n".join([f"- {item['item']}: Stock={item['current_stock']}, Reorder={item['reorder_point']}, Usage={item['monthly_usage']}/mo" 
                               for item in inventory_data])
    
    prompt = f"""Analyze inventory levels and provide recommendations:

Current Inventory:
{inventory_list}

Analysis:
1. Stock status alerts (low/overstocked items)
2. Reorder recommendations with quantities
3. Usage trend analysis
4. Inventory optimization suggestions
5. Cost reduction opportunities"""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=300,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Inventory Management System ===\n")
    print(analyze_inventory(SAMPLE_INVENTORY))

if __name__ == "__main__":
    main()
