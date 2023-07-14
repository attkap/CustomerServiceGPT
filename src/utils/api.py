import os
import logging
import openai

from typing import Any, Dict
from dotenv import find_dotenv, load_dotenv

# Load OPENAI_API_KEY from .env
load_dotenv(find_dotenv())
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def call_llm(system_message: str, user_message: str) -> Dict[str, Any]:
    """
    Call the OpenAI API with a system message and a user message.

    Parameters:
    system_message (str): The system message.
    user_message (str): The user message.

    Returns:
    dict: The response from the OpenAI API.
    """
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]

    try:
        return openai.ChatCompletion.create(
            model="gpt-4", temperature=0.0, messages=messages
        )
    except Exception as e:
        logger.error(f"Failed to call OpenAI API: {e}")
        raise

