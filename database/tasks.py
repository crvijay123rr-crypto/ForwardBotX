from database.mongo import tasks

async def create_task(user_id):
    await tasks.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "first_link": None,
                "last_link": None,
                "destination": None,
                "status": "waiting"
            }
        },
        upsert=True
    )

async def set_first_link(user_id, link):
    await tasks.update_one(
        {"user_id": user_id},
        {"$set": {"first_link": link}}
    )

async def set_last_link(user_id, link):
    await tasks.update_one(
        {"user_id": user_id},
        {"$set": {"last_link": link}}
    )

async def set_destination(user_id, channel):
    await tasks.update_one(
        {"user_id": user_id},
        {"$set": {"destination": channel}}
    )

async def get_task(user_id):
    return await tasks.find_one({"user_id": user_id})
