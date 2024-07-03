import requests
import os
from dotenv import load_dotenv
def yandexgpt_answer(prompt: str):
    """
    Генерирует ответ с использованием модели Yandexgpt-lite на основе заданного промпта.
    
    Аргументы:
    prompt (str): Текст промпта для генерации ответа.

    Возвращает:
    result (str): Сгенерированный ответ на основе промпта в виде строки.
    """
    load_dotenv()
    question = {
    "modelUri": f"gpt://{os.getenv('YANDEX_DIRECTORY_ID')}/yandexgpt/latest",
    "completionOptions": {
        "stream": False,
        "temperature": 0.7,
        "maxTokens": "2000"
    },
    "messages": [
        {
        "role": "system",
        "text": "Ты — рассказчик историй."
        },
        {
        "role": "user",
        "text": prompt
        }
    ]
    }
    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {os.getenv('YANDEX_AUTHORIATION')}"
    }
    
    try:
        response = requests.post(url, headers=headers, json=question)
        response_json = response.json()
        result = response_json['result']['alternatives'][0]['message']['text']
        return result
    except Exception as e:
        result = str(e)
        return result
