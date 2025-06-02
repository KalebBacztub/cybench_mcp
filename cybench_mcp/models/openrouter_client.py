import requests
from config.config import OPENROUTER_API_KEY

class OpenRouterClient:
    def __init__(self, api_key=OPENROUTER_API_KEY):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def query(self, messages, model="deepseek/deepseek-r1-0528:free", temperature=0.0, max_tokens=1024):
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        response = requests.post(self.base_url, headers=self.headers, json=payload, timeout=100)

        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content']
        else:
            raise Exception(f"OpenRouter API error {response.status_code}: {response.text}")