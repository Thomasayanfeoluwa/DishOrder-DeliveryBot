import chainlit as cl
from src.loader import order_request, messages
from src.notification import  __init__, send_sms, send_whatsapp, send_emails


@cl.on_message 
async def main(message: cl.Message):
    messages.append({"role": "user", "content": message.content})
    response = order_request(messages)
    messages.append({"role": "assistant", "content": response})

    # Send message back to the user
    await cl.Message(
        content=response,
    ).send()

