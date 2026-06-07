from pyrogram import Client
from config import *

app = Client(
    "ForwardBotX",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins")
)

print("🚀 ForwardBotX Started")

app.run()
