# src/categorize.py
import logging

from api import call_llm

# Set logging level to INFO
logging.basicConfig(level=logging.INFO)
# Get a logger instance
logger = logging.getLogger(__name__)

# Categorization
def get_parent_category_and_child_category(customer_request):
    """
    Categorize the customer request into one of the predefined categories.

    This function makes a call to OpenAI API to classify the customer request.

    Parameters:
    customer_request (str): The customer request text.
    categories_list (Dict): The list of available categories.

    Returns:
    dict: A dictionary containing 'parent_category' and 'child_category' keys.
    """

    system_message = ("""
        You will be provided with a customer service request.\
        Output a string in the format "parent_category_child_category",
        For example: "Delivery_Missing_Package"

        Parent categories: Delivery, Product_Feedback, Product_Support, Subscription, Other

        Delivery child categories: 
        Missing_Package
        Damaged_Package
        Out_of_Stock

        Product_Feedback child categories:
        Taste_Feedback
        Satiation_Feedback
        Tolerance_Feedback

        Product_Support child categories:
        Texture_Questions
        Storage_Questions

        Product_Recommendations
        Subscription child categories:
        Cancellations
        Address_Changes
        Delivery_Date_Changes

        Other child categories:
        All_other

        Output a string in the format "parent_category_child_category",
        For example: Delivery_Missing_Package

        """
    )
    user_message = customer_request
    try:
        llm_result = call_llm(system_message, user_message)
        categories_result = llm_result.choices[0].message.content
        if categories_result is None:
            logging.warning("No result from call_llm.")
        else:
            logging.info(categories_result)        
    except Exception as e:
        logger.error("Error categorizing request: %s", e)    
    return categories_result
