from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from database.buttons import (
    add_button,
    get_buttons,
    delete_all_buttons,
    enable_buttons,
    disable_buttons
)

from utils.states import (
    WAITING_BUTTON_TEXT,
    WAITING_BUTTON_URL,
    TEMP_BUTTON
)


# ==========================
# BUTTON PANEL
# ==========================

@Client.on_callback_query(
    filters.regex("^buttons_panel$")
)
async def buttons_panel(
    client,
    query
):

    data = await get_buttons(
        query.from_user.id
    )

    status = (
        "✅ Enabled"
        if data["enabled"]
        else "❌ Disabled"
    )

    total = len(
        data.get(
            "buttons",
            []
        )
    )

    text = f"""
🔘 BUTTON MANAGER

━━━━━━━━━━━━━━

Status:
{status}

Total Buttons:
{total}

━━━━━━━━━━━━━━
"""

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "➕ Add Button",
                callback_data="add_button"
            )
        ],
        [
            InlineKeyboardButton(
                "👀 View Buttons",
                callback_data="view_buttons"
            )
        ],
        [
            InlineKeyboardButton(
                "✅ Enable",
                callback_data="enable_buttons"
            ),
            InlineKeyboardButton(
                "❌ Disable",
                callback_data="disable_buttons"
            )
        ],
        [
            InlineKeyboardButton(
                "🗑 Delete All",
                callback_data="delete_all_buttons"
            )
        ]
    ])

    await query.message.edit_text(
        text,
        reply_markup=keyboard
    )


# ==========================
# ADD BUTTON
# ==========================

@Client.on_callback_query(
    filters.regex("^add_button$")
)
async def add_button_callback(
    client,
    query
):

    WAITING_BUTTON_TEXT[
        query.from_user.id
    ] = True

    await query.message.edit_text(
        """
🔘 Send Button Text

Example:

Join Channel
"""
    )


# ==========================
# BUTTON TEXT
# ==========================

@Client.on_message(
    filters.private &
    filters.text
)
async def receive_button_text(
    client,
    message
):

    user_id = message.from_user.id

    if user_id not in WAITING_BUTTON_TEXT:
        return

    WAITING_BUTTON_TEXT.pop(
        user_id
    )

    TEMP_BUTTON[user_id] = {
        "text": message.text
    }

    WAITING_BUTTON_URL[
        user_id
    ] = True

    await message.reply_text(
        """
🌐 Send Button URL

Example:

https://t.me/YourChannel
"""
    )


# ==========================
# BUTTON URL
# ==========================

@Client.on_message(
    filters.private &
    filters.text
)
async def receive_button_url(
    client,
    message
):

    user_id = message.from_user.id

    if user_id not in WAITING_BUTTON_URL:
        return

    WAITING_BUTTON_URL.pop(
        user_id
    )

    data = TEMP_BUTTON.pop(
        user_id
    )

    await add_button(
        user_id,
        data["text"],
        message.text
    )

    await enable_buttons(
        user_id
    )

    await message.reply_text(
        "✅ Button Added Successfully"
    )


# ==========================
# VIEW BUTTONS
# ==========================

@Client.on_callback_query(
    filters.regex("^view_buttons$")
)
async def view_buttons(
    client,
    query
):

    data = await get_buttons(
        query.from_user.id
    )

    buttons = data.get(
        "buttons",
        []
    )

    if not buttons:

        return await query.message.edit_text(
            "❌ No Buttons Added"
        )

    text = "🔘 SAVED BUTTONS\n\n"

    for button in buttons:

        text += (
            f"• {button['text']}\n"
            f"{button['url']}\n\n"
        )

    await query.message.edit_text(
        text
    )


# ==========================
# ENABLE
# ==========================

@Client.on_callback_query(
    filters.regex("^enable_buttons$")
)
async def enable_buttons_handler(
    client,
    query
):

    await enable_buttons(
        query.from_user.id
    )

    await query.answer(
        "Buttons Enabled ✅"
    )


# ==========================
# DISABLE
# ==========================

@Client.on_callback_query(
    filters.regex("^disable_buttons$")
)
async def disable_buttons_handler(
    client,
    query
):

    await disable_buttons(
        query.from_user.id
    )

    await query.answer(
        "Buttons Disabled ❌"
    )


# ==========================
# DELETE ALL
# ==========================

@Client.on_callback_query(
    filters.regex("^delete_all_buttons$")
)
async def delete_all_buttons_handler(
    client,
    query
):

    await delete_all_buttons(
        query.from_user.id
    )

    await query.message.edit_text(
        "🗑 All Buttons Deleted"
    )
