import openai
import logging
from typing import Dict, Any
from .openai_api import OpenAI_API

class CustomerRequest:
    def __init__(self, request_text: str, openai_api: OpenAI_API) -> None:
        """
        Initialize a CustomerRequest.

        :param request_text: The customer request text.
        :param openai_api: An instance of OpenAI_API class.
        """
        self.request_text = request_text
        self.translated_text = None
        self.category = None
        self.response = None
        self.is_harmful = None
        self.openai_api = openai_api  

        # Get a logger instance
        self.logger = logging.getLogger(__name__)

    def translate(self) -> None:
        """
        Translate the request text to English.
        """
        system_message = "Translate this text to English: {}"
        user_message = self.request_text
        llm_result = self.openai_api.call_llm(system_message.format(user_message), user_message)
        self.translated_text = llm_result.choices[0].message.content

    def categorize(self) -> None:
        """
        Categorize the translated request text.
        """
        system_message = "Categorize this customer request: {}"
        user_message = self.translated_text
        llm_result = self.openai_api.call_llm(system_message.format(user_message), user_message)
        self.category = llm_result.choices[0].message.content

    def formulate_response(self) -> None:
        """
        Formulate a response to the translated request text.
        """
        system_message = "Respond to this customer request: {}"
        user_message = self.translated_text
        llm_result = self.openai_api.call_llm(system_message.format(user_message), user_message)
        self.response = llm_result.choices[0].message.content

    def check_response(self) -> None:
        """
        Perform moderation and correctness checks on the formulated response.
        """
        # Moderation check
        moderation_response = openai.Moderation.create(input=self.response)
        moderation_result = moderation_response["results"][0]

        # Correctness check
        system_message = "Check the correctness of this response: {}"
        user_message = f"""
        Customer Request: {self.translated_text} 
        ###
        Category Context: {self.category}
        ###
        Assistant Response: {self.response}"""
        check_response = self.openai_api.call_llm(system_message.format(user_message), user_message)
        correctness_result = check_response.choices[0].message.content

        self.is_harmful = {"moderation_result": moderation_result, "correctness_result": correctness_result}

    def process_request(self) -> None:
        """
        Process the request: translate it, categorize it, formulate a response, and perform moderation and
        correctness checks on the response.
        """
        self.translate()
        self.logger.info(f'Translation: {self.translated_text}')
        
        self.categorize()
        self.logger.info(f'Category: {self.category}')
        
        self.formulate_response()
        self.logger.info(f'Response: {self.response}')
        
        self.check_response()
        self.logger.info(f'Moderation and correctness check: {self.is_harmful}')
