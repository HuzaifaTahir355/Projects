from langchain_openai import ChatOpenAI
from langchain_together import ChatTogether
from env import Env



# Initialize the LLM model
def get_llm(user_selection: str):
    if user_selection == "gpt-4o-mini":
        return ChatOpenAI(model="gpt-4o-mini")
    elif user_selection == "meta-llama/Llama-3-70b-chat-hf":
        print(Env.get("TOGETHER_API_KEY"))
        return ChatTogether(
            together_api_key=Env.get("TOGETHER_API_KEY"),
            model="meta-llama/Llama-3-70b-chat-hf"
            )


def get_response_from_llm(context: str, languages: list[str], model):
    prompt = f"""
    Your task is to identify the product names available in the given context. After that, extract the product description for each identified product from the context provided within the triple backticks.

    ```{context}```

    Once you have extracted the product names and their descriptions, translate the descriptions into the specified languages: {', '.join(languages)}.

    The output must be a list of dictionaries formatted as follows:

    [
        {{
            "product_name": "name of the product",
            "description": {{
                "English": "Description in English",
                "name of other language": "translated product description in the specified language"
            }}
        }}
    ]

    If no products are found in the provided context, respond with "No Product found". 

    Return the response only in the format specified above. No additional text or explanations are needed. Ensure the instructions are strictly followed.
    """

    response = model.invoke(prompt)
    return response.content


def verify_translated_response(description_in_english: str, language: str, translated_language_description: str, model):
    prompt = f"""
    You are a universal translation checker. I will provide you with content in English, the language it has been translated into, and the translated content. 

    content in english = '{description_in_english}'
    language = '{language}'
    translated content = '{translated_language_description}'

    Your responsibilities are:
    1. Check whether the translated content is accurate.
    2. If the translation is correct, respond with "verified" (string output).
    3. If the translation needs improvement, correct the translation and return the improved content in the provided language (string output).

    Return only the string output as specified.
    """
    
    response = model.invoke(prompt)
    return response.content