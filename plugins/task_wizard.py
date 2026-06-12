from pyrogram import Client, filters
from pyrogram.types import (
InlineKeyboardMarkup,
InlineKeyboardButton
)

from database.tasks import (
create_task,
update_task
)

from utils.states import (
FIRST_LINK,
LAST_LINK,
DESTINATION,
RENAME_MODE
)

==========================

NEW TASK

==========================

@Client.on_callback_query(
filters.regex("^new_task$")
)
async def new_task(
client,
query
):

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

Example:

https://t.me/channel/1
"""
)

==========================

MESSAGE HANDLER

==========================

@Client.on_message(
filters.private &
filters.text
)
async def task_handler(
client,
message
):

user_id = message.from_user.id

# ----------------------
# FIRST LINK
# ----------------------

if user_id in FIRST_LINK:

    task_id = FIRST_LINK.pop(
        user_id
    )

    try:

        first_id = int(
            message.text.split("/")[-1]
        )

        parts = message.text.split("/")

        if len(parts) >= 5:

            username = parts[-2]

            await update_task(
                task_id,
                "source_chat_username",
                username
            )

    except:

        return await message.reply_text(
            "❌ Invalid Link"
        )

    await update_task(
        task_id,
        "first_link",
        first_id
    )

    LAST_LINK[user_id] = task_id

    return await message.reply_text(
        """

✅ First Link Saved

🔗 Send Last Message Link
"""
)

# ----------------------
# LAST LINK
# ----------------------

if user_id in LAST_LINK:

    task_id = LAST_LINK.pop(
        user_id
    )

    try:

        last_id = int(
            message.text.split("/")[-1]
        )

    except:

        return await message.reply_text(
            "❌ Invalid Link"
        )

    await update_task(
        task_id,
        "last_link",
        last_id
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

# ----------------------
# DESTINATION
# ----------------------

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

        RENAME_MODE[user_id] = task_id

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "📂 Keep Original",
                    callback_data="keep_original"
                )
            ],
            [
                InlineKeyboardButton(
                    "✏ Rename Files",
                    callback_data="rename_files"
                )
            ],
            [
                InlineKeyboardButton(
                    "⏭ Skip Rename",
                    callback_data="skip_rename"
                )
            ]
        ])

        return await message.reply_text(
            f"""

✅ Destination Saved

📢 Channel:
{chat.title}

━━━━━━━━━━━━━━

Select Rename Mode
""",
reply_markup=keyboard
)

    except Exception as e:

        return await message.reply_text(
            f"❌ Error\n\n{e}"
        )

==========================

KEEP ORIGINAL

==========================

@Client.on_callback_query(
filters.regex("^keep_original$")
)
async def keep_original(
client,
query
):

user_id = query.from_user.id

task_id = RENAME_MODE.pop(
    user_id,
    None
)

if not task_id:

    return await query.answer(
        "Task Expired",
        show_alert=True
    )

await update_task(
    task_id,
    "rename_mode",
    "keep"
)

keyboard = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            "🚀 START FORWARD",
            callback_data=f"start_{task_id}"
        )
    ]
])

await query.message.edit_text(
    """

📂 Original File Names Will Be Kept

Task Ready To Start
""",
reply_markup=keyboard
)

==========================

RENAME FILES

==========================

@Client.on_callback_query(
filters.regex("^rename_files$")
)
async def rename_files(
client,
query
):

user_id = query.from_user.id

task_id = RENAME_MODE.pop(
    user_id,
    None
)

if not task_id:

    return await query.answer(
        "Task Expired",
        show_alert=True
    )

await update_task(
    task_id,
    "rename_mode",
    "rename"
)

keyboard = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            "🚀 START FORWARD",
            callback_data=f"start_{task_id}"
        )
    ]
])

await query.message.edit_text(
    """

✏ File Rename Mode Enabled

Task Ready To Start
""",
reply_markup=keyboard
)

==========================

SKIP RENAME

==========================

@Client.on_callback_query(
filters.regex("^skip_rename$")
)
async def skip_rename(
client,
query
):

user_id = query.from_user.id

task_id = RENAME_MODE.pop(
    user_id,
    None
)

if not task_id:

    return await query.answer(
        "Task Expired",
        show_alert=True
    )

await update_task(
    task_id,
    "rename_mode",
    "skip"
)

keyboard = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            "🚀 START FORWARD",
            callback_data=f"start_{task_id}"
        )
    ]
])

await query.message.edit_text(
    """

⏭ Rename Skipped

Task Ready To Start
""",
reply_markup=keyboard
        )
