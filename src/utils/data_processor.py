import json
import logging
from pathlib import Path
from typing import Any, Dict

class DataProcessor:
    def __init__(self, input_dir: str, output_dir: str) -> None:
        """
        Initialize a DataProcessor.

        :param input_dir: Directory containing input files.
        :param output_dir: Directory where to save output files.
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
       
        # Get a logger instance
        self.logger = logging.getLogger(__name__)

    def load_json(self, file_path: str) -> Dict[str, Any]:
        """
        Load JSON data from a file.

        :param file_path: Path to the file to load.
        :return: Loaded data.
        """
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            self.logger.debug(f"Successfully loaded data from {file_path}")
            return data
        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.logger.error(f"Failed to load or parse JSON data from {file_path}. Reason: {e}")
            raise

    def load_text_file(self, file_path: str) -> str:
        """
        Load text data from a file.

        :param file_path: Path to the file to load.
        :return: Loaded data.
        """
        try:
            with open(file_path, 'r') as f:
                data = f.read()
            self.logger.debug(f"Successfully loaded data from {file_path}")
            return data
        except FileNotFoundError as e:
            self.logger.error(f"Failed to load data from {file_path}. Reason: {e}")
            raise

    def save_output(self, output_dict: Dict[str, Any], output_file_path: str) -> None:
        """
        Save data to a JSON output file.

        :param output_dict: Data to save.
        :param output_file_path: Path to the file to save.
        """
        # Create the directory for output_file_path if it does not exist
        Path(output_file_path).parent.mkdir(parents=True, exist_ok=True)

        try:
            # Save the output
            with open(output_file_path, 'w') as f:
                json.dump(output_dict, f, indent=4)
            self.logger.debug(f"Successfully saved data to {output_file_path}")
        except OSError as e:
            self.logger.error(f"Failed to save data to {output_file_path}. Reason: {e}")
            raise
