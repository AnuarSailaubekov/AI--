import os
from groq import Groq
import concurrent.futures

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_groq(prompt):
    """Вспомогательная функция для отправки запроса в Groq"""
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def get_recommendations(emotion):
    if "Ошибка" in emotion or "Не удалось" in emotion:
        return "Не удалось получить совет.", "Не удалось получить песню."

    try:
        advice_prompt = f"Дай короткий совет человеку, который испытывает {emotion}. Ответь кратко и ясно"
        music_prompt = f"Посоветуй песню для человека, который испытывает {emotion}. Ответь кратко и ясно"

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_advice = executor.submit(ask_groq, advice_prompt)
            future_music = executor.submit(ask_groq, music_prompt)

            advice_response = future_advice.result()
            music_response = future_music.result()

        return advice_response, music_response

    except Exception as e:
        print(f"❌ Ошибка Groq (get_recommendations): {e}")
        return "Ошибка при получении совета.", "Ошибка при получении музыки."