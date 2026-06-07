from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI

mongo = AsyncIOMotorClient(MONGO_URI)

db = mongo["FORWARD_BOT_X"]

users = db.users
tasks = db.tasks
settings = db.settings
topics = db.topics
captions = db.captions
buttons = db.buttons
logs = db.logs
