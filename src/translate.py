import os
import openai
from dotenv import load_dotenv

def translate_text(customer_request):
    load_dotenv("/Users/attilakaplan/CustomerBotMVP/.env")

    openai.api_key = os.environ["OpenAI_API_KEY"]

    # Language detection
    language_detection = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", temperature=0.0,
        messages=[
            {"role": "system", "content": "What language is being used in the following user message? Output only the ISO 639-1 code of the language. Provide your output in pretty-printed json format with the key: 'ISO_639-1'."},
            {"role": "user", "content": customer_request}
        ]
    )

    detected_language = language_detection.choices[0].message.content

    # Translation to English
    translation = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", temperature=0.0,
        messages=[
            {"role": "system", "content": "Translate the following user message into precise and clear English that is maximally readable for GPT but still readable for humans. Do not add any information such as subject, etc."},
            {"role": "user", "content": customer_request}
        ]
    )

    translated_request = translation.choices[0].message.content

    # Return the results in a structured dictionary
    return {"detected_language": detected_language, "translated_text": translated_request}
