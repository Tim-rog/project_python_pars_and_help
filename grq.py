from groq import Groq
import os

client = Groq(api_key="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")

syst = """
Ты фильтр сообщений из рабочих чатов.
Ответь строго одним словом: IMPORTANT или SKIP.

IMPORTANT — если сообщение про смену, срочность, поломку, деньги, жалобу клиента, дедлайн, просьбу к человеку, расписание, обсуждение важных вопросов.
SKIP — флуд, мемы, ок, привет, стикеры, пустая болтовня.
"""
for m in client.models.list().data:
    print(m.id)
async def classify(text: str) -> str:
    r = client.chat.completions.create(
        model="openai/gpt-oss-safeguard-20b",
        messages=[
            {"role": "system", "content": syst},
            {"role": "user", "content": text},
        ],
        temperature=0,
    )
    return r.choices[0].message.content.strip().upper()