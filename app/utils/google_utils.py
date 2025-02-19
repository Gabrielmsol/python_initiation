# %% [markdown]
# # Google  Utils
# Responsavel por cuidar de assustos
# relacionados à API da google.
#
# Para criar a sua chave va no [Google AI Studio](https://aistudio.google.com/apikey)
# e crie a sua chave.
# %%
from google import genai
from dotenv import load_dotenv
import os


load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

instructions = """
The please write down in brazilian portuguese, follow the instructions:
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
"""  # Poe as informações do jeito que quiser

client = genai.Client(api_key=GOOGLE_API_KEY)


def analyze_with_ai(data: dict) -> dict:
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=[instructions, str(data)]
    )
    return response.to_json_dict()
    