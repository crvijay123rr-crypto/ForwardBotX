from database.mongo import buttons


async def get_buttons(user_id):

    data = await buttons.find_one(
        {
            "user_id": user_id
        }
    )

    if not data:

        default = {
            "user_id": user_id,
            "enabled": False,
            "buttons": []
        }

        await buttons.insert_one(
            default
        )

        return default

    return data


async def add_button(
    user_id,
    text,
    url
):

    await buttons.update_one(
        {
            "user_id": user_id
        },
        {
            "$push": {
                "buttons": {
                    "text": text,
                    "url": url
                }
            }
        },
        upsert=True
    )


async def delete_button(
    user_id,
    text
):

    await buttons.update_one(
        {
            "user_id": user_id
        },
        {
            "$pull": {
                "buttons": {
                    "text": text
                }
            }
        }
    )


async def enable_buttons(
    user_id
):

    await buttons.update_one(
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


async def disable_buttons(
    user_id
):

    await buttons.update_one(
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


async def buttons_enabled(
    user_id
):

    data = await get_buttons(
        user_id
    )

    return data.get(
        "enabled",
        False
    )


async def clear_buttons(
    user_id
):

    await buttons.update_one(
        {
            "user_id": user_id
        },
        {
            "$set": {
                "buttons": []
            }
        }
    )
