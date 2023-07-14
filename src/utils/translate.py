from typing import Dict
from src.utils.api import call_llm
from src.constants.system_message_constants import LANGUAGE_DETECTION_SYSTEM_MESSAGE, TRANSLATION_SYSTEM_MESSAGE

def translate_request(customer_request: str) -> Dict[str, str]:
    """
    Translates a customer request into English and detects the original language.

    Parameters:
    customer_request (str): The customer request to be translated.

    Returns:
    dict: A dictionary containing the detected language and the translated request.

    Raises:
    Exception: If there's an error during the API call.
    """
    try:
        # Language detection
        language_detection = call_llm(LANGUAGE_DETECTION_SYSTEM_MESSAGE, customer_request)
        detected_language = language_detection.choices[0].message.content
    except Exception as e:
        print(f"Error detecting language: {e}")
        raise

    try:
        # Translation to English
        translation = call_llm(TRANSLATION_SYSTEM_MESSAGE, customer_request)
        translated_request = translation.choices[0].message.content
    except Exception as e:
        print(f"Error translating request: {e}")
        raise

    # Return the results in a structured dictionary
    return {"detected_language": detected_language, "translated_request": translated_request}
