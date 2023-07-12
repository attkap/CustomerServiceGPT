# src/main.py
#from translate import translate_text
#from data_saver import save_output
import json
import os
from categorize import get_parent_category_and_child_category
from load_data import load_json
from load_data import load_text_file



def process_file(): #input_file_path
    # Read the contents of the input file
    #with open(input_file_path, 'r') as f:
    #    customer_request = f.read()

    # Translate the customer request
    #result = translate_text(customer_request)

    # Save the translation result to a JSON file
    #save_output(result, input_file_path)

    # Example usage
    #input_file_path = "../data/customer_requests/customer_request_1.txt"
    #process_file(input_file_path)

    # Load Data
    base_path = "../data"
    try:
        categories_list = load_json(
            os.path.join(base_path, "company_setup"), "category_list.json"
        )
        customer_request = load_text_file(
            os.path.join(base_path, "customer_requests"), "customer_request_1.txt"
        )
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error("Error loading data: %s", e)
        raise

    cat = get_parent_category_and_child_category(customer_request, categories_list)


if __name__ == "__main__":
    process_file()