import json
from pathlib import Path
from typing import Any, Dict

def save_output(output_dict: Dict[str, Any], output_file_path: str) -> None:
    """
    Save output to a JSON file.

    Parameters:
    output_dict (dict): The data to save.
    output_file_path (str): The path to the output file.

    Raises:
    OSError: If there's an error during file writing.
    """
    # Create the directory for output_file_path if it does not exist
    Path(output_file_path).parent.mkdir(parents=True, exist_ok=True)

    try:
        # Save the output
        with open(output_file_path, 'w') as f:
            json.dump(output_dict, f, indent=4)  # Add the indent parameter here
    except OSError as e:
        print(f"Error saving output to file: {e}")
        raise
