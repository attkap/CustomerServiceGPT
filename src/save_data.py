import json
import os
from pathlib import Path

def save_output(output_dict, input_file_path, output_dir='../data/LLM_outputs'):
    # Create output_dir if it does not exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Extract the base filename without extension using pathlib
    base_filename_without_ext = Path(input_file_path).stem

    # Construct the output file path
    output_filename = f'{base_filename_without_ext}_output.json'
    output_file_path = os.path.join(output_dir, output_filename)

    # Save the output
    with open(output_file_path, 'w') as f:
        json.dump(output_dict, f, indent=4)  # Add the indent parameter here