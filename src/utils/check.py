from typing import Dict
from src.utils.api import call_llm
from constants.system_message_constants import CHECK_RESPONSE_SYSTEM_MESSAGE
import openai

class CheckError(Exception):
    """
    Custom exception for errors during the response checking process.
    """
    pass

def check_response(translated_request: str, category_context: str, assistant_response: str) -> Dict[str, str]:
    """
    Checks a customer response for harm and correctness.

    Parameters:
    translated_request (str): The customer request translated into English.
    category_context (str): The relevant context given to generate the assistant response.
    assistant_response (str): The generated assistant response to the customer.

    Returns:
    dict: A dictionary containing the moderation result and the correctness check result.
    """
    # Moderation check
    try:
        moderation_response = openai.Moderation.create(input=assistant_response)
        moderation_result = moderation_response["results"][0]
    except Exception as e:
        raise CheckError(f"Error during moderation check: {e}") from e

    # Correctness check
    system_message = CHECK_RESPONSE_SYSTEM_MESSAGE
    user_message = f"""
    Customer Request: {translated_request} 
    ###
    Category Context: {category_context}
    ###
    Assistant Response: {assistant_response}"""

    try:
        check_response = call_llm(system_message, user_message)
        correctness_result = check_response.choices[0].message.content
    except Exception as e:
        raise CheckError(f"Error during correctness check: {e}") from e

    return {"moderation_result": moderation_result, "correctness_result": correctness_result}
