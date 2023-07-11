from translate import translate_text
from data_saver import save_output

def process_file(input_file_path):
    # Read the contents of the input file
    with open(input_file_path, 'r') as f:
        customer_request = f.read()

    # Translate the customer request
    result = translate_text(customer_request)

    # Save the translation result to a JSON file
    save_output(result, input_file_path)

# Example usage
input_file_path = "data/customer_requests/customer_request_1.txt"
process_file(input_file_path)
