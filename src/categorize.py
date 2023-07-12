from api import call_llm

# Categorization system message
CATEGORIZATION_SYSTEM_MESSAGE = """
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

class CategorizationError(Exception):
    """Custom exception for errors during categorization."""
    pass

def get_parent_category_and_child_category(customer_request):
    """
    Categorize the customer request into one of the predefined categories.

    This function makes a call to OpenAI API to classify the customer request.

    Parameters:
    customer_request (str): The customer request text.

    Returns:
    str: A string in the format "parent_category_child_category".
    """
    system_message = CATEGORIZATION_SYSTEM_MESSAGE
    user_message = customer_request

    try:
        llm_result = call_llm(system_message, user_message)
        categories_result = llm_result.choices[0].message.content

        if categories_result is None:
            raise CategorizationError("No result from call_llm.")

    except Exception as e:
        raise CategorizationError("Error categorizing request.") from e

    return categories_result
