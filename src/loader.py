from groq import Groq
from src.prompt import system_instruction

client = Groq()

# Initialize LLM
messages = [
    {"role": "system", "content": system_instruction}
]

def order_request(messages, model="llama-3.3-70b-versatile", temperature=0):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content


