from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from database.tasks import (
    create_task,
    update_task,
    get_task
)

from utils.states import (
    FIRST_LINK,
    LAST_LINK,
    DESTINATION
)


@Client.on_callback_query(
    filters.regex("^new_task$")
)
async def new_task(client, query):

    user_id = query.from_user.id

    task_id = await create_task(
        user_id
    )

    FIRST_LINK[user_id] = task_id

    await query.message.edit_text(
        f"""
🚀 NEW TASK CREATED

🆔 Task ID:
{task_id}

━━━━━━━━━━━━━━

🔗 Send First Message Link
"""
    )


@Client.on_message(
    filters.private &
    filters.text
)
async def task_handler(
    client,
    message
):

    user_id = message.from_user.id

    # FIRST LINK

    if user_id in FIRST_LINK:

        task_id = FIRST_LINK.pop(
            user_id
        )

        await update_task(
            task_id,
            "first_link",
            message.text
        )

        LAST_LINK[user_id] = task_id

        return await message.reply_text(
            """
✅ First Link Saved

🔗 Send Last Message Link
"""
        )

    # LAST LINK

    if user_id in LAST_LINK:

        task_id = LAST_LINK.pop(
            user_id
        )

        await update_task(
            task_id,
            "last_link",
            message.text
        )

        DESTINATION[user_id] = task_id

        return await message.reply_text(
            """
✅ Last Link Saved

📢 Send Destination Channel

Example:
@mychannel

or

-100xxxxxxxxxx
"""
        )

    # DESTINATION

    if user_id in DESTINATION:

        task_id = DESTINATION.pop(
            user_id
        )

        try:

            chat = await client.get_chat(
                message.text
            )

            await update_task(
                task_id,
                "destination_id",
                chat.id
            )

            await update_task(
                task_id,
                "destination_title",
                chat.title
            )

            await update_task(
                task_id,
                "destination_username",
                chat.username
            )

            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🚀 START FORWARD",
                        callback_data=f"start_{task_id}"
                    )
                ]
            ])

            return await message.reply_text(
                f"""
✅ TASK CONFIGURED

📢 Channel:
{chat.title}

🆔 Channel ID:
{chat.id}

━━━━━━━━━━━━━━

Ready To Start
""",
                reply_markup=keyboard
            )

        except Exception as e:

            return await message.reply_text(
                f"""
❌ Invalid Channel

Error:
{e}
"""
)
