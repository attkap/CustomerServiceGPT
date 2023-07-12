from api import call_llm
from system_message_constants import RESPONSE_SYSTEM_MESSAGE

def get_response(translated_request, categories_result, category_context):
    # Prepare the messages to send to OpenAI
    system_message = RESPONSE_SYSTEM_MESSAGE + f"""
        {categories_result}
        Here is some additional context:
        {category_context}
        """
    user_message = translated_request

    # Make an API call to OpenAI with the translated request and the context
    response = call_llm(system_message, user_message)

    # Extract the assistant's response
    assistant_response = response.choices[0].message.content

    return assistant_response
