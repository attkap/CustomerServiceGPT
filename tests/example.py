import unittest
import logging
import os
import openai
from dotenv import load_dotenv

# Initialize logging
logging.basicConfig(filename='test_logs.log', level=logging.INFO)

class TestOpenAI(unittest.TestCase):
    def setUp(self):
        load_dotenv("/Users/attilakaplan/CustomerBotMVP/.env")
        openai.api_key = os.environ["OpenAI_API_KEY"]

    def test_language_detection_and_translation(self):
        customer_request = """
        Guten Tag,
        ich habe heute eine Lieferung von Ihnen erhalten.
        #128492
        Bestelldatum: 03.07.23
        Leider fehlt der im Lieferschein enthaltende Messlöffel.
        Sonst ist alles da, auch der kostenfreie Shaker. Nur fehlt mir jetzt leider der Dosier- bzw. Messlöffel.
        Es wäre schön, wenn wir den noch erhalten könnten.
        Mit freundlichen Grüßen
        Jan Gärtner
        """

        # Language detection
        language_detection = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", temperature=0.0,
            messages=[
                {"role": "system", "content": "What language is being used in the following user message? Output only the ISO 639-1 code of the language. Provide your output in pretty-printed json format with the key: 'ISO_639-1'."},
                {"role": "user", "content": customer_request}
            ]
        )

        detected_language = language_detection.choices[0].message.content
        logging.info(f'Detected Language: {detected_language}')

        self.assertIsNotNone(detected_language)

        # Translation to English
        translation = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", temperature=0.0,
            messages=[
                {"role": "system", "content": "Translate the following user message into precise and clear English that is maximally readable for GPT but still readable for humans. Do not add any information such as subject, etc."},
                {"role": "user", "content": customer_request}
            ]
        )

        translated_request = translation.choices[0].message.content
        logging.info(f'Translated Request: {translated_request}')

        self.assertIsNotNone(translated_request)


if __name__ == '__main__':
    unittest.main()
