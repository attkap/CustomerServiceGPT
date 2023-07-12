import os
import json
from translate_request import translate_request
from categorize import get_parent_category_and_child_category
from respond_to_request import get_response
from save_data import save_output
from load_data import load_json, load_text_file

def process_files():
    # Paths
    base_path = "../data"
    requests_dir = os.path.join(base_path, "customer_requests")
    outputs_dir = os.path.join(base_path, "LLM_outputs")

    # Load categories
    categories_list = load_json(os.path.join(base_path, "company_setup"), "category_list.json")

    # Loop over all files in the customer_requests directory
    for filename in os.listdir(requests_dir):
        if filename.endswith(".txt"):
            # Load customer request
            customer_request = load_text_file(requests_dir, filename)

            # Translate the customer request
            translation_result = translate_request(customer_request)

            # Categorize the translated request
            categories_result = get_parent_category_and_child_category(translation_result["translated_request"], categories_list)

            # Formulate a response
            category_context_file = f"{categories_result['parent_category']}_{categories_result['child_category']}.txt"
            category_context_dir = os.path.join(base_path, "category_contexts")
            category_context = load_text_file(category_context_dir, category_context_file)

            response_result = get_response(translation_result["translated_request"], categories_result["parent_category"], categories_result["child_category"], category_context)

            # Prepare output
            output = {
                "customer_request": customer_request,
                "translation_result": translation_result,
                "categories_result": categories_result,
                "response_result": response_result,
            }

            # Save output
            save_output(output, filename, outputs_dir)


if __name__ == "__main__":
    process_files()
