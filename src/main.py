import logging
import os

from utils.categorize import get_parent_category_and_child_category
from utils.load_data import load_text_file
from utils.respond import get_response
from utils.save_data import save_output
from utils.translate import translate_request

# Configure the root logger to log DEBUG and above to the console.
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(message)s")
logger = logging.getLogger(__name__)

# Paths
base_path = "../data"
requests_dir = os.path.join(base_path, "customer_requests")
outputs_dir = os.path.join(base_path, "LLM_outputs")

def translate_and_log(customer_request: str) -> dict:
    """
    Translate a customer request and log the results.

    Parameters:
    customer_request (str): The customer request.

    Returns:
    dict: A dictionary containing the detected language and the translated request.
    """
    logger.info("Sending request to detect language and translate...")
    translation_result = translate_request(customer_request)
    logger.info(f"Detected language: {translation_result['detected_language']}")
    logger.info(f"Translated request: {translation_result['translated_request']}")
    return translation_result

def categorize_and_log(customer_request):
    categories_result = get_parent_category_and_child_category(customer_request)
    logger.info(f"Categories Result: {categories_result}")
    return categories_result

def formulate_response_and_log(translation_result, categories_result):
    category_context_file = f"{categories_result}.txt"
    category_context_dir = os.path.join(base_path, "category_contexts")
    # Construct the full file path
    full_file_path = os.path.join(category_context_dir, category_context_file)
    # Load category context
    category_context = load_text_file(full_file_path)
    logger.info(f"Category Context: {category_context}")
    response_result = get_response(translation_result["translated_request"], categories_result, category_context)
    logger.info(f"Response Result: {response_result}")
    return response_result

def process_request(filename):
    
    # Construct the full file path
    full_file_path = os.path.join(requests_dir, filename)
    
    # Load customer request from 
    customer_request = load_text_file(full_file_path)

    # Translate the customer request
    translation_result = translate_and_log(customer_request)

    # Categorize the translated request. 
    categories_result = categorize_and_log(customer_request)

    # Formulate a response
    response_result = formulate_response_and_log(translation_result, categories_result)

    return {
        "customer_request": customer_request,
        "translation_result": translation_result,
        "categories_result": categories_result,
        "response_result": response_result,
    }

def process_files():
    """
    Process all text files in the customer_requests directory.

    For each file, this function loads the customer request, translates it, categorizes it, 
    formulates a response, and saves the output.
    """
    # Loop over all files in the customer_requests directory
    for filename in os.listdir(requests_dir):
        if filename.endswith(".txt"):
            try:
                output = process_request(filename)
                # Save output
                save_output(output, filename, outputs_dir)
            except Exception as e:
                logger.error(f"Failed to process file {filename}. Reason: {e}")

if __name__ == "__main__":
    process_files()
