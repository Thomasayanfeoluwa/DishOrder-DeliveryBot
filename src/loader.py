from groq import Groq
from src.prompt import system_instruction
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY environment variable not set.")

client = Groq(api_key=api_key)


# Initialize LLM
messages = [
    {"role": "system", "content": system_instruction}
]

def order_request(messages, model="openai/gpt-oss-120b", temperature=0):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content


