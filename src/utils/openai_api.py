import os
import logging
import openai
import tiktoken
from typing import List, Dict, Any
from dotenv import find_dotenv, load_dotenv

INPUT_COST_PER_1K = 0.03
OUTPUT_COST_PER_1K = 0.06
MODEL_NAME = "gpt-4"

class OpenAI_API:
    def __init__(self) -> None:
        """Initialize an OpenAI_API instance."""
        # Load OPENAI_API_KEY from .env
        load_dotenv(find_dotenv())
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key is None:
            raise ValueError("Missing OPENAI_API_KEY in environment")

        # Get a logger instance
        self.logger = logging.getLogger(__name__)

        # Initialize total cost
        self.total_cost = 0.0

    def num_tokens_from_messages(self, messages: List[Dict[str, str]], model: str = MODEL_NAME) -> int:
        """
        Calculate the number of tokens in a list of messages.

        :param messages: List of messages, where each message is a dictionary with keys 'role' and 'content'.
        :param model: Name of the model to use for encoding.
        :return: Number of tokens.
        """
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            self.logger.warning("Model not found. Using cl100k_base encoding.")
            encoding = tiktoken.get_encoding("cl100k_base")

        tokens_per_message = 3
        tokens_per_name = 1

        num_tokens = sum(
            tokens_per_message + len(encoding.encode(value)) + (tokens_per_name if key == "name" else 0)
            for message in messages
            for key, value in message.items()
        )
        num_tokens += 3
        return num_tokens

    def call_llm(self, system_message: str, user_message: str) -> Dict[str, Any]:
        """
        Call the OpenAI ChatCompletion API with system and user messages.

        :param system_message: System message.
        :param user_message: User message.
        :return: API response.
        """
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ]

        num_input_tokens = self.num_tokens_from_messages(messages)

        try:
            response = openai.ChatCompletion.create(
                model=MODEL_NAME, temperature=0.0, messages=messages
            )
        except Exception as e:
            self.logger.error(f"Failed to call OpenAI API: {e}")
            raise

        num_output_tokens = response['usage']['completion_tokens']
        total_cost = (num_input_tokens / 1000 * INPUT_COST_PER_1K) + (num_output_tokens / 1000 * OUTPUT_COST_PER_1K)
        self.total_cost += total_cost
        self.logger.info(f"input tokens={num_input_tokens}, output tokens={num_output_tokens}, cost={total_cost}")

        return response

    def log_total_cost(self) -> None:
        """Log the total cost of all API calls."""
        self.logger.info(f"Total cost of all API calls: {self.total_cost}")
