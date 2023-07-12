import os
import logging
from api import call_llm

# Configure the root logger to log DEBUG and above to the console.
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(message)s")

input_file_path = "../data/customer_requests/customer_request_1.txt"

def translate_request(customer_request):

    # Language detection
    system_message = "What language is being used in the following user message? Output only the ISO 639-1 code of the language. Provide your output in pretty-printed json format with the key: 'ISO_639-1'."
    user_message = customer_request
    logging.info("Sending request to detect language...")
    language_detection = call_llm(system_message, user_message)

    detected_language = language_detection.choices[0].message.content
    logging.info(f"Detected language: {detected_language}")

    # Translation to English
    system_message = "Translate the following user message into precise and clear English that is maximally readable for GPT but still readable for humans. Do not add any information such as subject, etc."
    user_message = customer_request
    logging.info("Sending request for translation...")
    translation = call_llm(system_message, user_message)

    translated_request = translation.choices[0].message.content
    logging.info(f"Translated request: {translated_request}")

    # Return the results in a structured dictionary
    return {"detected_language": detected_language, "translated_request": translated_request}
