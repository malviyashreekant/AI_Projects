import os
from anthropic import Anthropic

SAMPLE_RISKS = [
    {"risk": "Data breach", "probability": "Medium", "impact": "High", "mitigation": "Enhanced security protocols"},
    {"risk": "Market downturn", "probability": "High", "impact": "Medium", "mitigation": "Diversified revenue streams"},
    {"risk": "Key employee departure", "probability": "Low", "impact": "High", "mitigation": "Knowledge documentation"},
]

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def assess_risks(risk_data):
    client = get_client()
    risks_list = "\n".join([f"- {risk['risk']}: P={risk['probability']}, I={risk['impact']}, Mitigation={risk['mitigation']}" 
                           for risk in risk_data])
    
    prompt = f"""Assess business risks and provide recommendations:

Identified Risks:
{risks_list}

Assessment:
1. Risk priority matrix (probability vs impact)
2. Critical risks requiring immediate attention
3. Risk mitigation strategy evaluation
4. Additional risk factors to consider
5. Risk monitoring recommendations"""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=350,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Risk Assessment Engine ===\n")
    print(assess_risks(SAMPLE_RISKS))

if __name__ == "__main__":
    main()
