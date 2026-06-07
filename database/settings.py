from database.mongo import settings

async def set_filename_mode(
    user_id,
    mode
):

    await settings.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "filename_mode": mode
            }
        },
        upsert=True
    )

async def get_settings(user_id):

    return await settings.find_one(
        {"user_id": user_id}
    )
