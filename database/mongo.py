from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI
import asyncio

# Connection client (server selection timeout add kiya hai)
mongo = AsyncIOMotorClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000 # 5 seconds mein timeout ho jayega agar connect nahi hua
)

db = mongo.ForwardBot

# ==========================
# Collections
# ==========================
users = db.users
tasks = db.tasks
topics = db.topics
settings = db.settings
captions = db.captions
buttons = db.buttons
bans = db.bans
stats = db.stats
duplicates = db.duplicates

# ==========================
# Database Check
# ==========================

async def ping_database():
    try:
        # Ping the database to verify connection
        await mongo.admin.command("ping")
        print("✅ MongoDB Connected")
        return True
    except Exception as e:
        print(f"❌ MongoDB Error: {e}")
        return False
        
