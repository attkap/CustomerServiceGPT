# api/api.py
import openai
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def call_openai_api(model, messages):
    return openai.ChatCompletion.create(
        model=model,
        temperature=0.0,
        messages=messages
    )
