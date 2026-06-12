from database.mongo import settings


DEFAULT_SETTINGS = {

    "speed": 3,

    "caption": True,

    "buttons": True,

    "topic_detect": True,

    "duplicate_filter": True,

    "auto_delete": False,

    "auto_forward": True
}


async def get_settings(user_id):

    data = await settings.find_one(
        {
            "user_id": user_id
        }
    )

    if not data:

        data = {

            "user_id": user_id,

            **DEFAULT_SETTINGS
        }

        await settings.insert_one(
            data
        )

        return data

    return data


async def update_setting(
    user_id,
    key,
    value
):

    await settings.update_one(
        {
            "user_id": user_id
        },
        {
            "$set": {
                key: value
            }
        },
        upsert=True
    )


async def toggle_setting(
    user_id,
    key
):

    data = await get_settings(
        user_id
    )

    current = data.get(
        key,
        False
    )

    new_value = not current

    await update_setting(
        user_id,
        key,
        new_value
    )

    return new_value


async def set_speed(
    user_id,
    speed
):

    if speed < 1:
        speed = 1

    if speed > 10:
        speed = 10

    await update_setting(
        user_id,
        "speed",
        speed
    )


async def get_speed(user_id):

    data = await get_settings(
        user_id
    )

    return data.get(
        "speed",
        3
    )


async def reset_settings(user_id):

    await settings.update_one(
        {
            "user_id": user_id
        },
        {
            "$set": DEFAULT_SETTINGS
        },
        upsert=True
    )


async def delete_settings(user_id):

    await settings.delete_one(
        {
            "user_id": user_id
        }
    )


async def caption_enabled(user_id):

    data = await get_settings(
        user_id
    )

    return data.get(
        "caption",
        True
    )


async def buttons_enabled(user_id):

    data = await get_settings(
        user_id
    )

    return data.get(
        "buttons",
        True
    )


async def topic_detection_enabled(
    user_id
):

    data = await get_settings(
        user_id
    )

    return data.get(
        "topic_detect",
        True
    )


async def duplicate_filter_enabled(
    user_id
):

    data = await get_settings(
        user_id
    )

    return data.get(
        "duplicate_filter",
        True
    )


async def auto_delete_enabled(
    user_id
):

    data = await get_settings(
        user_id
    )

    return data.get(
        "auto_delete",
        False
    )
