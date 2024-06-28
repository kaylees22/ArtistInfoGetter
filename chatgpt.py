import requests
import openai
from config import CHATGPT_KEY

class ChatGPT:
    def __init__(self):
        self.api = openai.OpenAI(api_key = CHATGPT_KEY)
        
        
    def ask_chat(self, message):
        MODEL = "gpt-3.5-turbo"
        response = self.api.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": message},
        ],
        temperature=0,
        )
        
        reply = response.choices[0].message.content
        return reply



