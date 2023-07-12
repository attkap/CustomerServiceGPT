import logging

from api import call_openai_api
from load_data import load_text_file

# Configure the root logger to log DEBUG and above to the console.
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(message)s")

# Simulating the output of your previous function
output1 = {"category": "Dummy_Category", "subcategory": "Dummy_Subcategory"}

# Access the category and subcategory
category = output1["category"]
subcategory = output1["subcategory"]

# Log the category and subcategory
logging.info(f"Category: {category}, Subcategory: {subcategory}")

# Simulating the output of another function
output2 = {
    "detected_language": "Dummy Language",
    "translated_text": "Dummy Translated Text",
}

# Access the detected language and translated text
detected_language = output2["detected_language"]
translated_text = output2["translated_text"]

# Log the detected language and translated text
logging.info(
    f"Detected Language: {detected_language}, Translated Text: {translated_text}"
)

# Now, we'll load the context file based on the given category and subcategory
category_context_file = f"{category}_{subcategory}.txt"
base_path = "../data/category_contexts"
category_context = load_text_file(base_path, category_context_file)

if category_context is not None:
    logging.info(f"Loaded context: {category_context}")
else:
    logging.error(f"Failed to load context file {category_context_file}")


def get_response(translated_text, category, subcategory, category_context):
    # Prepare the messages to send to OpenAI
    messages = [
        {
            "role": "system",
            "content": f"""
        You are a customer service representative for Saturo. Saturo is a European company that specializes in creating nutritionally complete, ready-to-drink meals and powders that aim to provide balanced nutrition in a convenient format. Your name is Gregor.
        You will be provided with a customer message which has been classified as part of the following category:
        {category} {subcategory}
        Here is some additional context:
        {category_context}
        """,
        },
        {"role": "user", "content": translated_text},
    ]

    # Print the messages
    logging.info(f"Sending the following messages to OpenAI API: {messages}")

    # Make an API call to OpenAI with the translated query and the context
    logging.info("Sending request to OpenAI API...")
    response = call_openai_api("gpt-3.5-turbo", messages)

    # Extract the assistant's response
    assistant_response = response.choices[0].message.content

    logging.info("Received response from OpenAI API: %s", assistant_response)

    return assistant_response


assistant_response = get_response(
    translated_text, category, subcategory, category_context
)

logging.info(f"Assistant Response: {assistant_response}")
