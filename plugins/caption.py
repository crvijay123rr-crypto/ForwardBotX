from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from database.captions import (
    get_caption,
    set_caption,
    enable_caption,
    disable_caption,
    delete_caption
)

from utils.states import CAPTION_WAIT


@Client.on_callback_query(
    filters.regex("^caption_settings$")
)
async def caption_settings(
    client,
    query
):

    data = await get_caption(
        query.from_user.id
    )

    status = (
        "✅ Enabled"
        if data["enabled"]
        else "❌ Disabled"
    )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "✏ Set Caption",
                callback_data="set_caption"
            )
        ],
        [
            InlineKeyboardButton(
                "👀 View Caption",
                callback_data="view_caption"
            )
        ],
        [
            InlineKeyboardButton(
                "✅ Enable",
                callback_data="enable_caption"
            ),
            InlineKeyboardButton(
                "❌ Disable",
                callback_data="disable_caption"
            )
        ],
        [
            InlineKeyboardButton(
                "🗑 Reset",
                callback_data="reset_caption"
            )
        ]
    ])

    await query.message.edit_text(
        f"""
📝 CAPTION SETTINGS

Status : {status}

Supported Variables:

{{filename}}
{{topic}}
{{index}}
{{batch}}
{{message_id}}
""",
        reply_markup=keyboard
    )


@Client.on_callback_query(
    filters.regex("^set_caption$")
)
async def set_caption_start(
    client,
    query
):

    CAPTION_WAIT[
        query.from_user.id
    ] = True

    await query.message.reply_text(
        """
✏ Send New Caption

Example:

📚 {topic}

📂 {filename}

🎯 {batch}
"""
    )


@Client.on_message(
    filters.private &
    filters.text
)
async def save_caption(
    client,
    message
):

    user_id = message.from_user.id

    if user_id not in CAPTION_WAIT:
        return

    CAPTION_WAIT.pop(
        user_id
    )

    await set_caption(
        user_id,
        message.text
    )

    await message.reply_text(
        "✅ Caption Saved Successfully"
    )


@Client.on_callback_query(
    filters.regex("^view_caption$")
)
async def view_caption(
    client,
    query
):

    data = await get_caption(
        query.from_user.id
    )

    await query.message.reply_text(
        f"""
📝 CURRENT CAPTION

{data['caption']}
"""
    )


@Client.on_callback_query(
    filters.regex("^enable_caption$")
)
async def enable_cap(
    client,
    query
):

    await enable_caption(
        query.from_user.id
    )

    await query.answer(
        "Caption Enabled ✅"
    )


@Client.on_callback_query(
    filters.regex("^disable_caption$")
)
async def disable_cap(
    client,
    query
):

    await disable_caption(
        query.from_user.id
    )

    await query.answer(
        "Caption Disabled ❌"
    )


@Client.on_callback_query(
    filters.regex("^reset_caption$")
)
async def reset_cap(
    client,
    query
):

    await delete_caption(
        query.from_user.id
    )

    await query.answer(
        "Caption Reset ✅"
    )
