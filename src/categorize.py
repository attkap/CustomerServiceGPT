# src/categorize.py
import json
import logging
import os
from typing import Dict, Optional

import api
import load_data

# Set logging level to INFO
logging.basicConfig(level=logging.INFO)
# Get a logger instance
logger = logging.getLogger(__name__)

# Load Data
base_path = "../data"
try:
    categories = load_data.load_json(
        (base_path, "company_setup"), "category_list.json"
    )
    customer_request = load_data.load_text_file(
        os.path.join(base_path, "customer_requests"), "customer_request_1.txt"
    )
except (FileNotFoundError, json.JSONDecodeError) as e:
    logger.error("Error loading data: %s", e)
    raise


# Categorization
def get_subcategory(customer_request: str, category: str) -> str:
    """
    Categorize the customer request into one of the predefined subcategories
    under the given category.

    This function makes a call to OpenAI API to classify the customer request
    into a subcategory within the specified category.

    Parameters:
    customer_request (str): The customer request text.
    category (str): The category under which to classify the request.

    Returns:
    str: The subcategory into which the request was classified.
    """
    messages = [
        {
            "role": "system",
            "content": "Categorize the customer request into one of the "
            "following subcategories:",
        },
        {"role": "assistant", "content": "\n".join(categories[category])},
        {"role": "user", "content": customer_request},
    ]

    try:
        subcategorization = api.call_openai_api("gpt-4", messages)
        return subcategorization.choices[0].message.content.strip()
    except Exception as e:
        logger.error("Error subcategorizing request: %s", e)
        raise


def get_category(customer_request: str) -> Dict[str, Optional[str]]:
    """
    Categorize the customer request into one of the predefined categories.

    This function makes a call to OpenAI API to classify the customer request.
    If the category is not "Other", it also gets the subcategory.

    Parameters:
    customer_request (str): The customer request text.

    Returns:
    dict: A dictionary containing 'category' and 'subcategory' keys.
    """
    messages = [
        {
            "role": "system",
            "content": "Categorize this customer request into one of the "
            "following categories:\n\n" + "\n".join(categories.keys()) + "\n",
        },
        {"role": "user", "content": customer_request},
    ]

    try:
        categorization = api.call_openai_api("gpt-4", messages)
        category = categorization.choices[0].message.content.strip()
    except Exception as e:
        logger.error("Error categorizing request: %s", e)
        raise

    if category == "Other":
        subcategory = None
    else:
        try:
            subcategory = get_subcategory(customer_request, category)
        except Exception as e:
            logger.error("Error getting subcategory: %s", e)
            raise

    logger.info("Category: %s", category)
    logger.info("Subcategory: %s", subcategory)

    return {"category": category, "subcategory": subcategory}


try:
    results = get_category(customer_request)
except Exception as e:
    logger.error("Error executing categorization: %s", e)
    raise
