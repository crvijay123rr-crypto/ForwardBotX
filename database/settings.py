from database.mongo import settings

DEFAULT_SETTINGS = {

    "filename_mode": "keep_original",

    "topic_detection": True,

    "caption_enabled": False,

    "button_enabled": False,

    "duplicate_skip": True,

    "summary_enabled": True
}

async def get_settings(user_id):

    data = await settings.find_one(
        {"user_id": user_id}
    )

    if not data:

        await settings.insert_one({
            "user_id": user_id,
            **DEFAULT_SETTINGS
        })

        return DEFAULT_SETTINGS

    return data

async def update_setting(
    user_id,
    key,
    value
):

    await settings.update_one(
        {"user_id": user_id},
        {"$set": {key: value}},
        upsert=True
    )
