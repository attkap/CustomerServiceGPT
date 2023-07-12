import os
from typing import Any, Dict, List

import openai
from dotenv import find_dotenv, load_dotenv

# Load OPENAI_API_KEY from .env
load_dotenv(find_dotenv())
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def call_llm(system_message, user_message):
    messages = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": user_message},
]

    return openai.ChatCompletion.create(
        model="gpt-4", temperature=0.0, messages=messages
    )
