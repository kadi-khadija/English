from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def format_conversation(messages: list[dict]) -> str:
    """
    Converts conversation messages into a readable text block.
    """
    formatted = []
    for msg in messages:
        speaker = "User" if msg["role"] == "user" else "Tutor"
        formatted.append(f"{speaker}: {msg['content']}")
    return "\n".join(formatted)


def generate_feedback(conversation: list[dict]) -> dict:
    """
    Generates structured feedback in Arabic (فصحى).
    """
    conversation_text = format_conversation(conversation)

    prompt = f"""
أنت مدرس لغة إنجليزية محترف.
قم بتحليل المحادثة التالية بين متعلم عربي ومدرس لغة إنجليزية.

المطلوب:
1. ملخص قصير للمحادثة (بالإنجليزية).
2. استخراج الأخطاء النحوية المهمة فقط.
   - الجملة الخاطئة
   - التصحيح الصحيح
   - شرح الخطأ باللغة العربية الفصحى
3. تحديد نمط الأخطاء الشائعة إن وُجد.
4. تقديم نصائح واضحة لتحسين مستوى اللغة (بالعربية الفصحى).

المحادثة:
{conversation_text}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}],
        temperature=0.3
    )

    return {"feedback": response.choices[0].message.content}
