from src.utils.api.api import call_llm
from src.constants.system_message_constants import RESPONSE_SYSTEM_MESSAGE

class ResponseError(Exception):
    """Custom exception for errors during response generation."""
    pass

def get_response(translated_request: str, categories_result: str, category_context: str) -> str:
    """
    Generate a response to a customer request using the OpenAI API.

    This function prepares a system message containing the response system message, 
    the categories result, and the category context. It then sends this system message 
    along with the translated customer request to the OpenAI API and extracts the 
    assistant's response from the API's response.

    Parameters:
    translated_request (str): The customer request translated into English.
    categories_result (str): The result of categorizing the customer request.
    category_context (str): The context for the category.

    Returns:
    str: The assistant's response.
    """
    # Prepare the messages to send to OpenAI
    system_message = RESPONSE_SYSTEM_MESSAGE + f"""
        {categories_result}
        Here is some additional context:
        {category_context}
        """
    user_message = translated_request

    try:
        # Make an API call to OpenAI with the translated request and the context
        response = call_llm(system_message, user_message)

        # Extract the assistant's response
        assistant_response = response.choices[0].message.content

    except Exception as e:
        raise ResponseError(f"Error generating response: {e}") from e

    return assistant_response
