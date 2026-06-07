from database.mongo import users

async def add_user(user_id):

    user = await users.find_one(
        {"user_id": user_id}
    )

    if user:
        return

    await users.insert_one({
        "user_id": user_id,
        "premium": False,
        "joined": True
    })

async def total_users():

    return await users.count_documents({})
