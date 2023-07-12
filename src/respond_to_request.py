import logging
from api import call_llm
from load_data import load_text_file

# Configure the root logger to log DEBUG and above to the console.
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(message)s")

def get_response(translated_request, parent_category, child_category, category_context):
    # Log the parent category, child category, and translated request
    logging.info(f"Parent Category: {parent_category}")
    logging.info(f"Child Category: {child_category}")
    logging.info(f"Translated Request: {translated_request}")

    if category_context is not None:
        logging.info(f"Loaded context: {category_context}")
    else:
        logging.error(f"Failed to load context file {category_context}")

    # Prepare the messages to send to OpenAI
    system_message = f"""
        You are a customer service representative for Saturo. Saturo is a European company that specializes in creating nutritionally complete, ready-to-drink meals and powders that aim to provide balanced nutrition in a convenient format. Your name is Gregor.
        You will be provided with a customer message which has been classified as part of the following parent category and child category:
        {parent_category} {child_category}
        Here is some additional context:
        {category_context}
        """
    user_message = translated_request

    # Print the messages
    logging.info(f"Sending the following messages to OpenAI API: {system_message}, {user_message}")

    # Make an API call to OpenAI with the translated request and the context
    logging.info("Sending request to OpenAI API...")
    response = call_llm(system_message, user_message)

    # Extract the assistant's response
    assistant_response = response.choices[0].message.content

    logging.info("Received response from OpenAI API: %s", assistant_response)

    return assistant_response