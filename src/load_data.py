import json
import logging
from typing import Any

# Set logging level to INFO
logging.basicConfig(level=logging.INFO)
# Get a logger instance
logger = logging.getLogger(__name__)

def load_json(file_path: str) -> Any:
    """
    Load data from a JSON file.

    Parameters:
    file_path (str): The full path to the JSON file.

    Returns:
    dict/list: The data loaded from the JSON file. 

    Raises:
    FileNotFoundError: If the file does not exist.
    json.JSONDecodeError: If the file is not valid JSON.
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        logger.debug(f"Successfully loaded data from {file_path}")
        return data
    except FileNotFoundError as e:
        logger.error(f"Failed to load data from {file_path}. Reason: {e}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON data from {file_path}. Reason: {e}")
        raise

def load_text_file(file_path: str) -> str:
    """
    Load data from a text file.

    Parameters:
    file_path (str): The full path to the text file.

    Returns:
    str: The data loaded from the text file.

    Raises:
    FileNotFoundError: If the file does not exist.
    """
    try:
        with open(file_path, 'r') as f:
            data = f.read()
        logger.debug(f"Successfully loaded data from {file_path}")
        return data
    except FileNotFoundError as e:
        logger.error(f"Failed to load data from {file_path}. Reason: {e}")
        raise