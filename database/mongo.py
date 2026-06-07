from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI

mongo = AsyncIOMotorClient(MONGO_URI)

db = mongo["FORWARD_BOT_X"]

users = db.users
settings = db.settings
tasks = db.tasks
topics = db.topics
buttons = db.buttons
captions = db.captions
