from database.mongo import buttons


async def get_buttons(user_id):

    data = await buttons.find_one(
        {
            "user_id": user_id
        }
    )

    if not data:

        data = {

            "user_id": user_id,

            "enabled": False,

            "buttons": []
        }

        await buttons.insert_one(
            data
        )

        return data

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


async def delete_all_buttons(
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
        },
        upsert=True
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


async def total_buttons(
    user_id
):

    data = await get_buttons(
        user_id
    )

    return len(
        data.get(
            "buttons",
            []
        )
    )


async def get_button_list(
    user_id
):

    data = await get_buttons(
        user_id
    )

    return data.get(
        "buttons",
        []
    )
