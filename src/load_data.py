import json
import logging
import os

# Set logging level to INFO
logging.basicConfig(level=logging.INFO)
# Get a logger instance
logger = logging.getLogger(__name__)

def load_json(base_path, filename):
    """Load data from a JSON file."""
    full_path = os.path.join(base_path, filename)
    try:
        with open(full_path, 'r') as f:
            data = json.load(f)
        logger.info(f"Successfully loaded data from {full_path}")
        return data
    except FileNotFoundError as e:
        logger.error(f"Failed to load data from {full_path}. Reason: {e}")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON data from {full_path}. Reason: {e}")
        return None

def load_text_file(base_path, filename):
    """Load data from a text file."""
    full_path = os.path.join(base_path, filename)
    try:
        with open(full_path, 'r') as f:
            data = f.read()
        logger.info(f"Successfully loaded data from {full_path}")
        return data
    except FileNotFoundError as e:
        logger.error(f"Failed to load data from {full_path}. Reason: {e}")
        return None

