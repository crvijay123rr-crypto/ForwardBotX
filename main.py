import logging
logging.basicConfig(level=logging.INFO)
from pyrogram import Client
from config import *

app = Client(
    "ForwardBot",

    api_id=API_ID,

    api_hash=API_HASH,

    bot_token=BOT_TOKEN,

    plugins=dict(
        root="plugins"
    )
)


if __name__ == "__main__":

    print(
        "\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🚀 FORWARD BOT STARTED\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
    )

    app.run()
