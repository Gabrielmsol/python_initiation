# %% [markdown]
# # Open AI Utils
# Responsavel por cuidar de assustos
# relacionados á API da Open AI, é
# como se você jogasse o texto la.
#
# Não tenho a api da open Ai nem sei se funciona...
#
# Provavlemente um bando de problema vai
# acontecer então relaxa e goza ai.
# %%
from openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
instructions = """
You will receive data in JSON format. Please parse the data and organize it into a response following this structure:
{
    "email": {
        "subject": "<email_subject>",
        "sender": "<sender_email>",
        "received_date": "<date_received>"
    },
    "analysis": {
        "summary": "<brief_summary_of_email>",
        "keywords": ["<keyword1>", "<keyword2>"],
        "sentiment": "<positive/neutral/negative>"
    }
}
Please ensure that your response follows this exact structure, with valid JSON syntax.
""" # Poe as informações do jeito que quiser

def load_client() -> OpenAI | None:
    """Como não tenho chave fiz isso"""
    if openai_api_key:
        return OpenAI(api_key=openai_api_key)


def analyze_with_ai(data: dict) -> dict:
    client = load_client()
    _instructions = f"{instructions}\n{str(data)}"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": _instructions}],
        temperature=0.5,
    )

    try:
        # Força a ficar em formato de dict
        response_dict = eval(response.choices[0].message.content)
        
        # Checa se deu certo
        if isinstance(response_dict, dict):
            return response_dict
        else:
            print("Error: The response is not in dictionary format.")
            return {}
    except Exception as e:
        print(f"Error processing response: {e}")
        return {}
