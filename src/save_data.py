import json
import os

def save_output(output_dict, input_file_path, output_dir='../data/LLM_outputs'):
    # Extract the base filename without extension
    base_filename = os.path.basename("../data/customer_requests/customer_request_1.txt")
    base_filename_without_ext = os.path.splitext(base_filename)[0]

    # Construct the output file path
    output_filename = f'{base_filename_without_ext}_output.json'
    output_file_path = os.path.join(output_dir, output_filename)

    # Save the output
    with open(output_file_path, 'w') as f:
        json.dump(output_dict, f, indent=4)  # Add the indent parameter here

