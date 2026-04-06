import os
from anthropic import Anthropic

SAMPLE_INGREDIENTS = [
    "chicken breast", "broccoli", "rice", "garlic", "soy sauce", "ginger"
]

DIETARY_PREFERENCES = {
    "restrictions": ["gluten-free"],
    "cuisine": "Asian",
    "cooking_time": "30 minutes",
    "skill_level": "beginner"
}

def get_client():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")
    return Anthropic(api_key=api_key)

def recommend_recipe(ingredients, preferences):
    client = get_client()
    ingredients_list = ", ".join(ingredients)
    
    prompt = f"""Recommend recipes using these ingredients: {ingredients_list}

Preferences:
- Dietary restrictions: {preferences.get('restrictions', 'None')}
- Preferred cuisine: {preferences.get('cuisine', 'Any')}
- Cooking time: {preferences.get('cooking_time', 'Any')}
- Skill level: {preferences.get('skill_level', 'Any')}

Provide:
1. Recipe name and description
2. Complete ingredients list (including what's missing)
3. Step-by-step cooking instructions
4. Prep/cook time and servings
5. Alternative ingredient suggestions"""

    response = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=400,
        temperature=0.4,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text

def main():
    print("=== Recipe Recommender ===\n")
    print(recommend_recipe(SAMPLE_INGREDIENTS, DIETARY_PREFERENCES))

if __name__ == "__main__":
    main()
