# %% [markdown]
# # Google  Utils
# Responsavel por cuidar de assustos
# relacionados à API da google.
#
# Para criar a sua chave va no [Google AI Studio](https://aistudio.google.com/apikey)
# e crie a sua chave.
# %%
from google import genai
from google.genai import types
from dotenv import load_dotenv
from pydantic import BaseModel
import os


load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

class Email(BaseModel):
    subject: str
    sender: str
    received_date: str

class Analysis(BaseModel):
    summary: str
    keywords: list[str]
    sentiment: str

class EmailInfo(BaseModel):
    email: Email
    analysis: Analysis
    
instructions = """
The please write down in brazilian portuguese, follow the instructions:
You will receive data in JSON format. Please parse the data and organize it into a response following this structure:

Please ensure that your response follows this exact structure, with valid JSON syntax.
"""  # Poe as informações do jeito que quiser

client = genai.Client(api_key=GOOGLE_API_KEY)


def analyze_with_ai(data: dict) -> dict:
  
    response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=instructions,
    config=types.GenerateContentConfig(
        response_mime_type='application/json',
        response_schema=EmailInfo,
        ),
    )
    
    return response.to_json_dict()
    