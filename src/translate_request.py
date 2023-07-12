from api import call_llm

# Language detection system message
LANGUAGE_DETECTION_SYSTEM_MESSAGE = "What language is being used in the following user message? Output only the ISO 639-1 code of the language. Provide your output in pretty-printed json format with the key: 'ISO_639-1'."

# Translation to English system message
TRANSLATION_SYSTEM_MESSAGE = "Translate the following user message into precise and clear English that is maximally readable for GPT but still readable for humans. Do not add any information such as subject, etc."

def translate_request(customer_request):

    # Language detection
    language_detection = call_llm(LANGUAGE_DETECTION_SYSTEM_MESSAGE, customer_request)
    detected_language = language_detection.choices[0].message.content

    # Translation to English
    translation = call_llm(TRANSLATION_SYSTEM_MESSAGE, customer_request)
    translated_request = translation.choices[0].message.content

    # Return the results in a structured dictionary
    return {"detected_language": detected_language, "translated_request": translated_request}