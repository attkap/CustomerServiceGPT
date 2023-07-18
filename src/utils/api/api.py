import os
import logging
import openai

import tiktoken
from typing import List, Dict, Any
from dotenv import find_dotenv, load_dotenv

# Load OPENAI_API_KEY from .env
load_dotenv(find_dotenv())
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def num_tokens_from_messages(messages: List[Dict[str, str]], model: str="gpt-4") -> int:
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
        
    # Assuming it works with gpt-4 by default
    tokens_per_message = 3
    tokens_per_name = 1

    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with assistant
    return num_tokens

def call_llm(system_message: str, user_message: str) -> Dict[str, Any]:
    """
    Call the OpenAI API with a system message and a user message.

    Parameters:
    system_message (str): The system message.
    user_message (str): The user message.

    Returns:
    dict: The dictionary containing the response from the OpenAI API.
    """
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]

    # Calculate the number of input tokens
    num_input_tokens = num_tokens_from_messages(messages)
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4", temperature=0.0, messages=messages
        )
    except Exception as e:
        logger.error(f"Failed to call OpenAI API: {e}")
        raise

    # Extract the number of output tokens from the response
    num_output_tokens = response['usage']['completion_tokens']

    # Calculate cost
    input_cost_per_1K = 0.03
    output_cost_per_1K = 0.06
    total_cost = (num_input_tokens / 1000 * input_cost_per_1K) + (num_output_tokens / 1000 * output_cost_per_1K)

    # Log token and cost information in one message
    logger.info(f"API call token usage and cost: input tokens={num_input_tokens}, output tokens={num_output_tokens}, total cost={total_cost}")

    return response


