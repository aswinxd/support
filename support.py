from pyrogram import Client, filters
from pyrogram.types import Message

# Replace with your API credentials
API_ID = "7980140"
API_HASH = "db84e318c6894f560a4087c20c33ce0a"
BOT_TOKEN = "7123013710:AAGUUb-cirJUhvUNIFar91zAKTGo7h6WkNs"

# Group chat ID where admin messages are sent
SUPPORT_GROUP_ID = -1001535538162  # Replace with your group's ID

# Initialize the bot
app = Client("support_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Dictionary to store user-message to group-message mapping
user_message_map = {}

@app.on_message(filters.private & filters.text | filters.media)
async def forward_to_support_group(client: Client, message: Message):
    """
    When a user sends a message (text/media), forward it to the support group.
    """
    user = message.from_user
    forwarded_message = await message.forward(chat_id=SUPPORT_GROUP_ID)
    
    # Store the user and their message ID to map it with the admin's response
    user_message_map[forwarded_message.message_id] = user.id
    
    await forwarded_message.reply_text(
        f"User @{user.username} sent a message. Reply here to respond."
    )

@app.on_message(filters.group & filters.reply)
async def reply_to_user(client: Client, message: Message):
    """
    When an admin replies to a forwarded message in the group, forward the response to the user.
    """
    user_message_map[forwarded_message.id] = user.id
    if message.reply_to_message and message.reply_to_message.id in user_message_map:
       user_id = user_message_map[message.reply_to_message.id]
    if message.text:
        await client.send_message(chat_id=user_id, text=message.text)
     elif message.media:
        await message.copy(chat_id=user_id)

    await message.reply_text("Reply sent to the user.")

# Start the bot
app.run()
