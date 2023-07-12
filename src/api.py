# api/api.py
import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def call_openai_api(model, messages):
    return openai.ChatCompletion.create(
        model=model,
        temperature=0.0,
        messages=messages
    )
