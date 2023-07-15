import unittest
from unittest.mock import patch, MagicMock
from src.utils.request_handlers._1_translate import translate_request

class TestTranslateRequest(unittest.TestCase):
    @patch('src.utils.translate.call_llm')
    def test_translate_request(self, mock_call_llm):
        # Define the mock responses for language detection and translation
        mock_language_detection_response = MagicMock()
        mock_language_detection_response.choices[0].message.content = 'fr'
        mock_translation_response = MagicMock()
        mock_translation_response.choices[0].message.content = 'Hello, world'
        
        # Define the behavior of the mock function
        mock_call_llm.side_effect = [mock_language_detection_response, mock_translation_response]

        # Call the function with a test request
        result = translate_request("Bonjour le monde")
        
        # Assert that the function correctly processed the mocked API responses
        self.assertEqual(result, {'detected_language': 'fr', 'translated_request': 'Hello, world'})

if __name__ == '__main__':
    unittest.main()
