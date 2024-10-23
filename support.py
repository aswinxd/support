from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio

API_ID = "7980140"
API_HASH = "db84e318c6894f560a4087c20c33ce0a"
BOT_TOKEN = "7123013710:AAGUUb-cirJUhvUNIFar91zAKTGo7h6WkNs"


SUPPORT_GROUP_ID = -1001535538162  


app = Client("support_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


user_message_map = {}

@app.on_message(filters.command("start") & filters.private)
async def start_message(client: Client, message: Message):
    """
    Sends a welcome message when the user starts the bot.
    """
    await message.reply_text(
        "Hello! Welcome to our support bot. Please send your questions or concerns, and we will forward them to the moderators."
    )

@app.on_message(filters.private & (filters.text | filters.media))
async def forward_to_support_group(client: Client, message: Message):
    """
    When a user sends a message (text/media), forward it to the support group.
    """
    user = message.from_user 
    forwarded_message = await message.forward(chat_id=SUPPORT_GROUP_ID)
    
    
    user_message_map[forwarded_message.id] = user.id
    
 
    await asyncio.sleep(5)  
    await message.reply_text(
        "Your message has been sent to the moderators. Please wait for their response."
    )


    await forwarded_message.reply_text(
        f"User @{user.username} sent a message. Reply here to respond."
    )

@app.on_message(filters.group & filters.reply)
async def reply_to_user(client: Client, message: Message):
    """
    When an admin replies to a forwarded message in the group, forward the response to the user.
    """
    if message.reply_to_message and message.reply_to_message.id in user_message_map:
        user_id = user_message_map[message.reply_to_message.id]
        
       
        if message.text:
            await client.send_message(chat_id=user_id, text=message.text)
        elif message.media:
            await message.copy(chat_id=user_id)

        await message.reply_text("Reply sent to the user.")


app.run()
