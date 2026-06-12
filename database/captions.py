from database.mongo import captions


DEFAULT_CAPTION = ""


async def get_caption(user_id):

    data = await captions.find_one(
        {
            "user_id": user_id
        }
    )

    if not data:

        data = {

            "user_id": user_id,

            "enabled": False,

            "caption": DEFAULT_CAPTION
        }

        await captions.insert_one(
            data
        )

        return data

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
                "caption": DEFAULT_CAPTION,
                "enabled": False
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


async def get_caption_text(
    user_id
):

    data = await get_caption(
        user_id
    )

    return data.get(
        "caption",
        DEFAULT_CAPTION
    )
