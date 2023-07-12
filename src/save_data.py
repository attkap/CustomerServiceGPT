import json
import os
from pathlib import Path
from typing import Any, Dict

def save_output(output_dict: Dict[str, Any], input_file_path: str, output_dir: str = '../data/LLM_outputs') -> None:
    """
    Save output to a JSON file.

    Parameters:
    output_dict (dict): The data to save.
    input_file_path (str): The path to the input file (used to construct the output file name).
    output_dir (str): The directory where the output file will be saved.

    Raises:
    OSError: If there's an error during file writing.
    """
    # Create output_dir if it does not exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Extract the base filename without extension using pathlib
    base_filename_without_ext = Path(input_file_path).stem

    # Construct the output file path
    output_filename = f'{base_filename_without_ext}_output.json'
    output_file_path = os.path.join(output_dir, output_filename)

    try:
        # Save the output
        with open(output_file_path, 'w') as f:
            json.dump(output_dict, f, indent=4)  # Add the indent parameter here
    except OSError as e:
        print(f"Error saving output to file: {e}")
        raise
