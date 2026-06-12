import logging
from pyrogram import Client, idle  # <--- 'idle' yahan import karna zaroori hai
from config import *

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = Client(
    "ForwardBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="plugins")
)

if __name__ == "__main__":
    print("\n🚀 FORWARD BOT IS STARTING...\n")
    
    # Bot start karein
    app.start()
    print(f"✅ Number of loaded handlers: {len(app.dispatcher.groups)}")
    print("🤖 Bot is now running! Press Ctrl+C to stop.")
    
    # Sahi tarika: 'app.idle()' nahi, sirf 'idle()' call karein
    idle()
    
    # Bot stop hone par
    app.stop()
    
