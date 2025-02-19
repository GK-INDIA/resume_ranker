import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
try:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
except:
    print("message: ", "Enter a valid openai key")


client = OpenAI(api_key=OPENAI_API_KEY)

SEED = 42


def get_completion(prompt):

    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        seed=SEED,
        temperature=0,  # this is the degree of randomness of the model's output
        response_format={"type": "json_object"},
    )
    return response.choices[0].message.content
