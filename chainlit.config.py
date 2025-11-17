import chainlit as cl

@cl.on_chat_start
async def on_chat_start():
    # This will run when the chat starts
    await cl.Message(content="**How you dey! Welcome to DishDelivery Nigerian Restaurant! 🍽️🇳🇬**").send()

