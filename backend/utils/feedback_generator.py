import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

FIREWORKS_API_KEY = os.getenv("FIREWORKS_API_KEY")

print(FIREWORKS_API_KEY)

def clean_response(content: str) -> str:
    return re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()

def get_feedback(text: str) -> str:
    url = "https://api.fireworks.ai/inference/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {FIREWORKS_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "accounts/fireworks/models/deepseek-r1",  # pick one Fireworks supports
        "messages": [
            {"role": "system", "content": "You are a critical case competition deck evaluator."},
            {"role": "user", "content": f"Please evaluate this deck content:\n\n{text}"}
        ],
        "max_tokens": 500,
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"]

def chat_with_ai(query: str) -> str:
    url = "https://api.fireworks.ai/inference/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {FIREWORKS_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "accounts/fireworks/models/deepseek-r1",
        "messages": [
            {"role": "system", "content": "You are a helpful consultant for case competitions."},
            {"role": "user", "content": query},
        ],
        "max_tokens": 500,
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"]
