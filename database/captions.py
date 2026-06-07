from database.mongo import captions


DEFAULT_CAPTION = """
📚 {topic}

📂 {filename}

━━━━━━━━━━━━━━
Powered By ForwardBotX
━━━━━━━━━━━━━━
"""


async def get_caption(user_id):

    data = await captions.find_one(
        {
            "user_id": user_id
        }
    )

    if not data:

        await captions.insert_one(
            {
                "user_id": user_id,
                "enabled": False,
                "caption": DEFAULT_CAPTION
            }
        )

        return {
            "enabled": False,
            "caption": DEFAULT_CAPTION
        }

    return data


async def set_caption(
    user_id,
    caption
):

    await captions.update_one(
        {
            "user_id": user_id
        },
        {
            "$set": {
                "caption": caption
            }
        },
        upsert=True
    )


async def enable_caption(
    user_id
):

    await captions.update_one(
        {
            "user_id": user_id
        },
        {
            "$set": {
                "enabled": True
            }
        },
        upsert=True
    )


async def disable_caption(
    user_id
):

    await captions.update_one(
        {
            "user_id": user_id
        },
        {
            "$set": {
                "enabled": False
            }
        },
        upsert=True
    )


async def delete_caption(
    user_id
):

    await captions.update_one(
        {
            "user_id": user_id
        },
        {
            "$set": {
                "caption": DEFAULT_CAPTION
            }
        },
        upsert=True
    )


async def caption_enabled(
    user_id
):

    data = await get_caption(
        user_id
    )

    return data.get(
        "enabled",
        False
    )
