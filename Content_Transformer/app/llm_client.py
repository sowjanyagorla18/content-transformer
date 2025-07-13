import requests
from config import API_URL, API_KEY

def call_llm(prompt: str) -> str:
    headers = {"x-api-key": API_KEY}
    data = {
        "model": "usf1-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "web_search": True,
        "stream": False,
        "max_tokens": 1000,
    }
    response = requests.post(API_URL, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]
