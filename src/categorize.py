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
def get_parent_category(customer_request: str, categories_list: Dict) -> Dict[str, Optional[str]]:
    """
    Categorize the customer request into one of the predefined categories.

    This function makes a call to OpenAI API to classify the customer request.

    Parameters:
    customer_request (str): The customer request text.
    categories_list (Dict): The list of available categories.

    Returns:
    dict: A dictionary containing 'parent_category' and 'child_category' keys.
    """
    system_message = (
        "Categorize the customer request into one of the following categories:\n"
        + "\n".join(categories_list.keys())
    )
    user_message = customer_request

    try:
        categorization = call_llm(system_message, user_message)
        parent_category = categorization.choices[0].message.content.strip()
    except Exception as e:
        logger.error("Error categorizing request: %s", e)
        raise

    return parent_category

def get_child_category(customer_request: str, categories_list: Dict) -> str:
    """
    Categorize the customer request into one of the predefined child categories
    under the given category.

    This function makes a call to OpenAI API to classify the customer request
    into a child_category within the specified category.

    Parameters:
    customer_request (str): The customer request text.
    parent_category (str): The parent category under which to classify the request.

    Returns:
    str: The child_category into which the request was classified.
    """
    system_message = (
        "Categorize the customer request into one of the following child categories:\n"
        + "\n".join(categories_list.keys())
    )
    user_message = customer_request

    try:
        child_categorization = call_llm(system_message, user_message)
        child_category = child_categorization.choices[0].message.content.strip()
    except Exception as e:
        logger.error("Error child category request: %s", e)
        raise

    return child_category


def get_parent_category_and_child_category(customer_request, categories_list):
    try:
        parent_category = get_parent_category(customer_request, categories_list)
    except Exception as e:
        logger.error("Error getting parent_category: %s", e)
        raise
    logger.info("Parent Category: %s", parent_category)

    try:
        child_category = get_child_category(customer_request, categories_list)
    except Exception as e:
        logger.error("Error getting child_category: %s", e)
        raise
    logger.info("Child Category: %s", child_category)

    return {"parent_category": parent_category, "child_category": child_category}