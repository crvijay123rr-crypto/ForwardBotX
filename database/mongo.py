from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI


mongo = AsyncIOMotorClient(
    MONGO_URI
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

        await mongo.admin.command(
            "ping"
        )

        print(
            "✅ MongoDB Connected"
        )

        return True

    except Exception as e:

        print(
            f"❌ MongoDB Error: {e}"
        )

        return False
