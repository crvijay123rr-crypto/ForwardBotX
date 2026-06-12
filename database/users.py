from database.mongo import users
from datetime import datetime


async def add_user(user):

    user_id = user.id

    exists = await users.find_one(
        {
            "user_id": user_id
        }
    )

    if exists:
        return False

    data = {

        "user_id": user_id,

        "name": user.first_name,

        "username": user.username,

        "is_banned": False,

        "is_premium": False,

        "premium_expiry": None,

        "total_tasks": 0,

        "total_forwarded": 0,

        "joined_at": datetime.utcnow()
    }

    await users.insert_one(data)

    return True


async def get_user(user_id):

    return await users.find_one(
        {
            "user_id": user_id
        }
    )


async def user_exists(user_id):

    user = await users.find_one(
        {
            "user_id": user_id
        }
    )

    return bool(user)


async def total_users():

    return await users.count_documents(
        {}
    )


async def get_all_users():

    return users.find(
        {}
    )


async def ban_user(user_id):

    await users.update_one(
        {
            "user_id": user_id
        },
        {
            "$set": {
                "is_banned": True
            }
        }
    )


async def unban_user(user_id):

    await users.update_one(
        {
            "user_id": user_id
        },
        {
            "$set": {
                "is_banned": False
            }
        }
    )


async def is_banned(user_id):

    user = await users.find_one(
        {
            "user_id": user_id
        }
    )

    if not user:
        return False

    return user.get(
        "is_banned",
        False
    )


async def make_premium(
    user_id,
    expiry_date
):

    await users.update_one(
        {
            "user_id": user_id
        },
        {
            "$set": {
                "is_premium": True,
                "premium_expiry": expiry_date
            }
        }
    )


async def remove_premium(user_id):

    await users.update_one(
        {
            "user_id": user_id
        },
        {
            "$set": {
                "is_premium": False,
                "premium_expiry": None
            }
        }
    )


async def is_premium(user_id):

    user = await users.find_one(
        {
            "user_id": user_id
        }
    )

    if not user:
        return False

    return user.get(
        "is_premium",
        False
    )


async def increase_task_count(user_id):

    await users.update_one(
        {
            "user_id": user_id
        },
        {
            "$inc": {
                "total_tasks": 1
            }
        }
    )


async def increase_forward_count(
    user_id,
    count=1
):

    await users.update_one(
        {
            "user_id": user_id
        },
        {
            "$inc": {
                "total_forwarded": count
            }
        }
    )


async def delete_user(user_id):

    await users.delete_one(
        {
            "user_id": user_id
        }
    )
