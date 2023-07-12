from api import call_llm

# Initial part of the system message
SYSTEM_MESSAGE = """
You are a customer service representative for Saturo. Saturo is a European company that specializes in creating nutritionally complete, ready-to-drink meals and powders that aim to provide balanced nutrition in a convenient format. Your name is Gregor.
You will be provided with a customer message which has been classified as part of the following category:
"""

def get_response(translated_request, categories_result, category_context):
    # Prepare the messages to send to OpenAI
    system_message = SYSTEM_MESSAGE + f"""
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
