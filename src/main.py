import os
import logging

from src.utils.request_handlers._5_process_and_log import process_request
from src.utils.data_processing.save_data import save_output

# Configure the root logger to log DEBUG and above to the console.
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(message)s")
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Paths
    base_path = "./data"
    requests_dir = os.path.join(base_path, "customer_requests")
    outputs_dir = os.path.join(base_path, "LLM_outputs")

    def process_files() -> None:
        """
        Processes all text files in the customer_requests directory.

        For each file, this function loads the customer request, translates it, categorizes it, 
        formulates a response, and saves the output.

        Raises:
            Any exceptions raised during processing are logged and do not stop the processing of subsequent files.
        """
        # Loop over all files in the customer_requests directory
        for filename in os.listdir(requests_dir):
            if filename.endswith(".txt"):
                
                # Construct the full file path
                full_file_path = os.path.join(requests_dir, filename)
                
                try:
                    output = process_request(full_file_path, base_path)
                    
                    # Construct the output file path
                    base_filename_without_ext = os.path.splitext(filename)[0]
                    output_file_path = os.path.join(outputs_dir, f"{base_filename_without_ext}_output.json")
                    
                    # Save output
                    save_output(output, output_file_path)
                except Exception as e:
                    logger.error(f"Failed to process file {filename}. Reason: {e}")

    process_files()
