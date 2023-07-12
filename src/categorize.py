# src/categorize.py
import json
import logging
import os
from typing import Dict, Optional

import load_data
from api import call_llm

# Set logging level to INFO
logging.basicConfig(level=logging.INFO)
# Get a logger instance
logger = logging.getLogger(__name__)

# Categorization
def get_category(customer_request: str, categories) -> Dict[str, Optional[str]]:
    """
    Categorize the customer request into one of the predefined categories.

    This function makes a call to OpenAI API to classify the customer request.
    If the category is not "Other", it also gets the subcategory.

    Parameters:
    customer_request (str): The customer request text.

    Returns:
    dict: A dictionary containing 'category' and 'subcategory' keys.
    """
    system_message = (
        "Categorize the customer request into one of the following categories:\n"
        + "\n".join(categories.keys())
    )
    user_message = customer_request

    try:
        categorization = call_llm(system_message, user_message)
        parent_category = categorization.choices[0].message.content.strip()
    except Exception as e:
        logger.error("Error categorizing request: %s", e)
        raise

    return parent_category

def get_subcategory(customer_request: str, categories) -> str:
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
    system_message = (
        "Categorize the customer request into one of the following subcategories:\n"
        + "\n".join(categories.keys())
    )
    user_message = customer_request

    try:
        subcategorization = call_llm(system_message, user_message)
        child_category = subcategorization.choices[0].message.content.strip()
    except Exception as e:
        logger.error("Error subcategorizing request: %s", e)
        raise

    return child_category


def get_parent_category_and_child_category(customer_request, categories):
    try:
        category = get_category(customer_request, categories)
    except Exception as e:
        logger.error("Error getting subcategory: %s", e)
        raise
    logger.info("Category: %s", category)

    try:
        subcategory = get_subcategory(customer_request, categories)
    except Exception as e:
        logger.error("Error getting subcategory: %s", e)
        raise
    logger.info("Subcategory: %s", subcategory)

    return {"parent_category": category, "child_category": subcategory}