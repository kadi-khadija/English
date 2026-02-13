from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


LEVEL_RULES = {
    "beginner": """
Use very simple and common English words.
Short sentences.
Ask clear and direct questions.
Avoid idioms and complex grammar.
""",
    "intermediate": """
Use normal daily English.
Medium-length sentences.
Encourage explanations and opinions.
Correct mistakes politely.
""",
    "advanced": """
Use rich vocabulary and complex sentence structures.
Encourage arguments, justifications, and detailed opinions.
Point out subtle grammar mistakes.
"""
}


TOPIC_RULES = {
    "introductions": "Introductions & Personal Information",
    "daily_routine": "Daily Routine & Time",
    "describing_people": "Describing People & Personality",
    "family": "Family & Relationships",
    "studies": "Studies & University",
    "work": "Work & Career",
    "food": "Food, Restaurants & Cafés",
    "technology": "Technology & Social Media",
    "future_plans": "Future Plans & Goals",
    "opinions": "Opinions & Arguments"
}


def build_system_prompt(level: str, topic_key: str) -> str:
    topic = TOPIC_RULES[topic_key]
    level_rule = LEVEL_RULES[level]

    return f"""
You are an English language tutor.
Use Neutral / International English only.

Conversation topic: {topic}

Rules:
{level_rule}

Important:
- Speak ONLY in English.
- Do NOT translate.
- Keep the conversation natural.
- Encourage the user to speak more.
- Do not switch topics unless the user asks.
"""


def get_ai_reply(
    conversation_history: list[dict],
    level: str,
    topic_key: str
) -> str:
    system_prompt = build_system_prompt(level, topic_key)

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(conversation_history)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7
    )

    return response.choices[0].message.content
