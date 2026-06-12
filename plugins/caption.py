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

from utils.states import (
    WAITING_CAPTION
)


# ==========================
# CAPTION PANEL
# ==========================

@Client.on_callback_query(
    filters.regex("^caption_panel$")
)
async def caption_panel(
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

    text = f"""
📝 CAPTION MANAGER

━━━━━━━━━━━━━━

Status:
{status}

━━━━━━━━━━━━━━

Variables:

{{filename}}

{{topic}}

{{batch}}

{{message_id}}

{{original_caption}}

━━━━━━━━━━━━━━
"""

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📝 Set Caption",
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
                "🗑 Delete Caption",
                callback_data="delete_caption"
            )
        ]
    ])

    await query.message.edit_text(
        text,
        reply_markup=keyboard
    )


# ==========================
# SET CAPTION
# ==========================

@Client.on_callback_query(
    filters.regex("^set_caption$")
)
async def set_caption_callback(
    client,
    query
):

    WAITING_CAPTION[
        query.from_user.id
    ] = True

    await query.message.edit_text(
        """
📝 Send Your New Caption

Example:

📚 {topic}

📂 {filename}

━━━━━━━━━━━━━━

Join @YourChannel
"""
    )


# ==========================
# RECEIVE CAPTION
# ==========================

@Client.on_message(
    filters.private &
    filters.text
)
async def save_caption(
    client,
    message
):

    user_id = message.from_user.id

    if user_id not in WAITING_CAPTION:
        return

    WAITING_CAPTION.pop(
        user_id
    )

    await set_caption(
        user_id,
        message.text
    )

    await enable_caption(
        user_id
    )

    await message.reply_text(
        "✅ Caption Saved Successfully"
    )


# ==========================
# VIEW CAPTION
# ==========================

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

    caption = data.get(
        "caption",
        "No Caption Set"
    )

    await query.message.edit_text(
        f"""
📝 CURRENT CAPTION

━━━━━━━━━━━━━━

{caption}
"""
    )


# ==========================
# ENABLE
# ==========================

@Client.on_callback_query(
    filters.regex("^enable_caption$")
)
async def enable_caption_handler(
    client,
    query
):

    await enable_caption(
        query.from_user.id
    )

    await query.answer(
        "Caption Enabled ✅"
    )


# ==========================
# DISABLE
# ==========================

@Client.on_callback_query(
    filters.regex("^disable_caption$")
)
async def disable_caption_handler(
    client,
    query
):

    await disable_caption(
        query.from_user.id
    )

    await query.answer(
        "Caption Disabled ❌"
    )


# ==========================
# DELETE
# ==========================

@Client.on_callback_query(
    filters.regex("^delete_caption$")
)
async def delete_caption_handler(
    client,
    query
):

    await delete_caption(
        query.from_user.id
    )

    await query.message.edit_text(
        """
🗑 Caption Deleted Successfully
"""
    )
