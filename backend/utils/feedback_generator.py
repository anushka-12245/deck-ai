import os
import requests

FIREWORKS_API_KEY = os.getenv("FIREWORKS_API_KEY")

def get_feedback(text: str) -> str:
    url = "https://api.fireworks.ai/inference/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {FIREWORKS_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "accounts/fireworks/models/llama-v3p1-70b-instruct",  # pick one Fireworks supports
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
        "model": "accounts/fireworks/models/llama-v3p1-70b-instruct",
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
