from database.mongo import bans
from datetime import datetime


async def ban_user(
    user_id,
    reason="No Reason"
):

    data = {

        "user_id": user_id,

        "reason": reason,

        "banned_at": datetime.utcnow()
    }

    await bans.update_one(
        {
            "user_id": user_id
        },
        {
            "$set": data
        },
        upsert=True
    )


async def unban_user(
    user_id
):

    await bans.delete_one(
        {
            "user_id": user_id
        }
    )


async def is_banned(
    user_id
):

    data = await bans.find_one(
        {
            "user_id": user_id
        }
    )

    return bool(data)


async def get_ban(
    user_id
):

    return await bans.find_one(
        {
            "user_id": user_id
        }
    )


async def total_banned():

    return await bans.count_documents(
        {}
    )


async def get_all_banned():

    return bans.find(
        {}
    )


async def delete_all_bans():

    await bans.delete_many(
        {}
    )
