import os
import logging
from src.utils.request_handler import RequestHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO
    format='%(asctime)s %(levelname)s:%(name)s: %(message)s',  # Include timestamp, level, module name in logs
    datefmt='%Y-%m-%d %H:%M:%S',  # Timestamp format
)


def main(requests_dir: str, outputs_dir: str) -> None:
    """
    Main function that initializes a RequestHandler and processes customer requests.

    :param requests_dir: Directory containing customer request files.
    :param outputs_dir: Directory where to save output files.
    """
    # Create a RequestHandler instance and process the files
    request_handler = RequestHandler(requests_dir, outputs_dir)
    request_handler.process_files()

    # Log the total cost
    request_handler.openai_api.log_total_cost()


if __name__ == "__main__":
    # Paths
    base_path = "./data"
    requests_dir = os.path.join(base_path, "customer_requests")
    outputs_dir = os.path.join(base_path, "LLM_outputs")

    main(requests_dir, outputs_dir)
