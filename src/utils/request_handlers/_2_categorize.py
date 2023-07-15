from typing import Dict
from src.utils.api.api import call_llm
from src.constants.system_message_constants import CATEGORIZATION_SYSTEM_MESSAGE

class CategorizationError(Exception):
    """Custom exception for errors during categorization."""
    pass

def get_parent_category_and_child_category(translated_request: str) -> str:
    """
    Categorize the customer request into one of the predefined categories.

    This function makes a call to OpenAI API to classify the customer request.

    Parameters:
    translated_request (str): The translated customer request text.

    Returns:
    str: A string in the format "parent_category_child_category".
    """
    system_message = CATEGORIZATION_SYSTEM_MESSAGE
    user_message = translated_request

    try:
        llm_result: Dict = call_llm(system_message, user_message)
        categories_result: str = llm_result.choices[0].message.content

        if categories_result is None:
            raise CategorizationError("No result from call_llm.")

    except Exception as e:
        raise CategorizationError(f"Error categorizing request: {e}") from e

    return categories_result
