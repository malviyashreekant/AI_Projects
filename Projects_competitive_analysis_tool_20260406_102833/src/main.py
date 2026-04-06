import os
from anthropic import Anthropic

SAMPLE_COMPETITORS = [
    {"name": "CompetitorA", "price": "$49/mo", "features": "Basic CRM, Email marketing, 1000 contacts"},
    {"name": "CompetitorB", "price": "$99/mo", "features": "Advanced CRM, Automation, Unlimited contacts, Analytics"},
    {"name": "CompetitorC", "price": "$29/mo", "features": "Simple CRM, Email templates, 500 contacts"}
]

OUR_PRODUCT = {
    "name": "Our Solution",
    "price": "$79/mo", 
    "features": "Full CRM, AI automation, 5000 contacts, Advanced analytics"
}

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def analyze_competition(competitors, our_product):
    client = get_client()
    comp_list = "\n".join([f"- {comp['name']}: {comp['price']} | {comp['features']}" for comp in competitors])
    
    prompt = f"""Perform competitive analysis:

Our Product: {our_product['name']} - {our_product['price']}
Features: {our_product['features']}

Competitors:
{comp_list}

Analysis:
1. Pricing comparison and positioning
2. Feature gap analysis
3. Competitive advantages/disadvantages
4. Market positioning recommendations
5. Strategic opportunities"""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=350,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Competitive Analysis Tool ===\n")
    print(analyze_competition(SAMPLE_COMPETITORS, OUR_PRODUCT))

if __name__ == "__main__":
    main()
