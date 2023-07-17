import os
import logging
from typing import Dict

from src.utils.request_handlers._2_categorize import get_parent_category_and_child_category
from src.utils.data_processing.load_data import load_text_file
from src.utils.request_handlers._3_respond import get_response
from src.utils.request_handlers._1_translate import translate_request
from src.utils.request_handlers._4_check import check_response

logger = logging.getLogger(__name__)

def translate_and_log(customer_request: str) -> Dict[str, str]:
    """
    Translates a customer request and logs the results.

    Args:
        customer_request: A string containing the customer request to be translated.

    Returns:
        A dictionary containing the detected language and the translated request.
    """
    logger.info("Sending request to detect language and translate...")
    translation_result = translate_request(customer_request)
    logger.info(f"Detected language: {translation_result['detected_language']}")
    logger.info(f"Translated request: {translation_result['translated_request']}")
    return translation_result

def categorize_and_log(translated_request: str) -> str:
    """
    Categorizes a customer request and logs the result.

    Args:
        translated_request: A string containing the customer request to be categorized.

    Returns:
        A string containing the category of the request.
    """
    categories_result = get_parent_category_and_child_category(translated_request)
    logger.info(f"Categories Result: {categories_result}")
    return categories_result

def formulate_response_and_log(translated_request: str, categories_result: str, base_path: str) -> Dict[str, str]:
    """
    Formulates a response based on the translated request and its category, and logs the result.

    Args:
        translated_request: A string containing the customer request translated into English.
        categories_result: A string containing the category of the request.
        base_path: The base path for data files.

    Returns:
        A dictionary containing the formulated response and the category context.
    """
    category_context_file = f"{categories_result}.txt"
    category_context_dir = os.path.join(base_path, "category_contexts")

    # Construct the full file path
    full_file_path = os.path.join(category_context_dir, category_context_file)

    # Load category context
    category_context = load_text_file(full_file_path)
    logger.info(f"Category Context: {category_context}")
    assistant_response = get_response(translated_request, categories_result, category_context)
    logger.info(f"Assistant Response: {assistant_response}")
    
    return {"assistant_response": assistant_response, "category_context": category_context}


def check_and_log(translated_request: str, category_context: str, assistant_response: str) -> Dict[str, str]:
    """
    Checks a customer response for harm and correctness and logs the results.

    Args:
        translated_request: A string containing the translated customer request.
        category_context: A string containing the relevant context to generate the assistant response.
        assistant_response: A string containing the generated assistant response.

    Returns:
        A dictionary containing the moderation result and the check result.
    """
    logger.info("Sending response to check...")
    check_result = check_response(translated_request, category_context, assistant_response)
    logger.info(f"Moderation Result: {check_result['moderation_result']}")
    logger.info(f"Check Result: {check_result['correctness_result']}")
    return check_result

def process_request(full_file_path: str, base_path: str) -> Dict[str, str]:
    """
    Processes a single request file.

    This function reads the customer request from the file, translates it, categorizes it,
    formulates a response, and returns the results in a dictionary.

    Args:
        full_file_path: A string containing the full file path of the request file.
        base_path: The base path for data files.

    Returns:
        A dictionary containing the customer request, translation result, categories result, response result and check result.
    """
    # Load customer request from 
    customer_request = load_text_file(full_file_path)

    # Translate the customer request
    translation_result = translate_and_log(customer_request)
    translated_request = translation_result['translated_request']

    # Categorize the translated request. 
    categories_result = categorize_and_log(translated_request)

    # Formulate a response
    response_and_context = formulate_response_and_log(translated_request, categories_result, base_path)
    assistant_response = response_and_context["assistant_response"]
    category_context = response_and_context["category_context"]

    # Check the response
    check_result = check_and_log(translated_request, category_context, assistant_response)

    return {
        "customer_request": customer_request,
        "translation_result": translation_result,
        "categories_result": categories_result,
        "assistant_response": assistant_response,
        "check_result": check_result,
    }