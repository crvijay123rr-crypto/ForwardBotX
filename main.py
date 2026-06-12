import logging
import asyncio
from pyrogram import Client, idle
from config import *
from database.mongo import ping_database

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

async def start_bot():
    # 1. Database Check (Sabse pehle ye hoga)
    print("\n🔄 Connecting to Database...")
    db_ok = await ping_database()
    
    if not db_ok:
        print("❌ DATABASE CONNECTION FAILED. Exiting...")
        return
    
    # 2. Bot Start
    await app.start()
    print("\n"
          "━━━━━━━━━━━━━━━━━━━━━━\n"
          "🚀 FORWARD BOT IS RUNNING\n"
          "━━━━━━━━━━━━━━━━━━━━━━\n")
    
    # 3. Idle mode
    await idle()
    
    # 4. Stop
    await app.stop()
    print("\n🛑 Bot Stopped.")

if __name__ == "__main__":
    try:
        app.run(start_bot())
    except Exception as e:
        print(f"❌ Error: {e}")
        
