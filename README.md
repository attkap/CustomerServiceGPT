# Customer Service Chatbot

This project implements a customer service chatbot powered by OpenAI's language model. The chatbot processes customer requests, categorizes them into predefined categories, translates them into English, generates appropriate responses, and checks the response for harm and correctness.

## Installation

1. **Clone the Repository**: Clone this repository to your local machine.
2. **Set Up Environment Variables**: Copy the `.env.example` file (if available) and rename it to `.env`. Add your OpenAI API key to the file.
3. **Install Dependencies**: Run `pip install -r requirements.txt` to install the required dependencies.
4. **Configure Virtual Environment**: Optionally, set up a virtual environment using your preferred method.

## Usage

The customer service bot operates by following these steps:

1. **Load the Customer Request**: Customer requests are captured in text files located in the `/data/customer_requests` directory. The bot reads these files to process the requests (A sample customer request is included)
2. **Translate the Customer Request**: The bot translates the customer request into English, if needed, using the configured translation service.
3. **Categorize the Customer Request**: The request is categorized into one of the predefined categories.
4. **Create a Response to the Customer Request**: A response is generated based on the category and context of the request.
5. **Check the Response for Harmfulness**: The response is checked for harmful content or language using predefined criteria.
6. **Output the Response as a JSON**: The final response, along with any relevant metadata, is output as a JSON file and stored in the `/data/LLM_outputs` directory.

All prompts used for interacting with the OpenAI API are stored in `constants/system_messages`.

### Running the Bot

You can run the customer service bot by executing the `main.py` script within the `src` directory:

```bash
python src/main.py
```

## Project Structure

The project is organized as follows:

- `src/`: Contains the source code for the project.
  - `main.py`: The main script that coordinates the processing of customer requests.
  - `utils/`: Utility functions.
  - `constants/`: Constants used throughout the project.
- `tests/`: Contains various test scripts and related data.
  - `test_prompts.py`, `test_translate.py`: Test scripts.
  - `data/`: Test data.
  - `results/`: Test results.
- `data/`: Contains data related to customer requests and categories.
  - `LLM_outputs/`: Outputs related to language models.
  - `customer_requests/`: Customer request data.
  - `category_contexts/`: Contexts related to categories.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
