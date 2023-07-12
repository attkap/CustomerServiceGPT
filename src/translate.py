from api import call_llm
from system_message_constants import LANGUAGE_DETECTION_SYSTEM_MESSAGE, TRANSLATION_SYSTEM_MESSAGE

def translate_request(customer_request):

    # Language detection
    language_detection = call_llm(LANGUAGE_DETECTION_SYSTEM_MESSAGE, customer_request)
    detected_language = language_detection.choices[0].message.content

    # Translation to English
    translation = call_llm(TRANSLATION_SYSTEM_MESSAGE, customer_request)
    translated_request = translation.choices[0].message.content

    # Return the results in a structured dictionary
    return {"detected_language": detected_language, "translated_request": translated_request}