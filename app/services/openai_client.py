import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)


def ask_ai(prompt):
    response = client.responses.create(
        model="gpt-6-luna",
        input=prompt
    )

    return response.output_text