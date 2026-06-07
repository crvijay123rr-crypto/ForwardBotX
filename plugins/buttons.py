from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from database.buttons import (
    get_buttons,
    add_button,
    delete_button,
    enable_buttons,
    disable_buttons
)

from utils.states import (
    BUTTON_TEXT_WAIT,
    BUTTON_URL_WAIT
)


TEMP_BUTTONS = {}


@Client.on_callback_query(
    filters.regex("^button_settings$")
)
async def button_settings(
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

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "➕ Add Button",
                callback_data="add_button"
            )
        ],
        [
            InlineKeyboardButton(
                "📋 View Buttons",
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
        ]
    ])

    await query.message.edit_text(
        f"""
🔘 BUTTON SETTINGS

Status : {status}

Manage Custom URL Buttons
""",
        reply_markup=keyboard
    )


@Client.on_callback_query(
    filters.regex("^add_button$")
)
async def add_button_start(
    client,
    query
):

    BUTTON_TEXT_WAIT[
        query.from_user.id
    ] = True

    await query.message.reply_text(
        "✏ Send Button Text"
    )


@Client.on_message(
    filters.private &
    filters.text
)
async def button_text_handler(
    client,
    message
):

    user_id = message.from_user.id

    if user_id not in BUTTON_TEXT_WAIT:
        return

    BUTTON_TEXT_WAIT.pop(
        user_id
    )

    TEMP_BUTTONS[user_id] = {
        "text": message.text
    }

    BUTTON_URL_WAIT[user_id] = True

    await message.reply_text(
        "🔗 Send Button URL"
    )


@Client.on_message(
    filters.private &
    filters.text
)
async def button_url_handler(
    client,
    message
):

    user_id = message.from_user.id

    if user_id not in BUTTON_URL_WAIT:
        return

    BUTTON_URL_WAIT.pop(
        user_id
    )

    text = TEMP_BUTTONS[
        user_id
    ]["text"]

    await add_button(
        user_id,
        text,
        message.text
    )

    TEMP_BUTTONS.pop(
        user_id,
        None
    )

    await message.reply_text(
        "✅ Button Added Successfully"
    )


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

        return await query.message.reply_text(
            "❌ No Buttons Found"
        )

    text = "📋 SAVED BUTTONS\n\n"

    count = 1

    for button in buttons:

        text += (
            f"{count}. "
            f"{button['text']}\n"
            f"{button['url']}\n\n"
        )

        count += 1

    await query.message.reply_text(
        text
    )


@Client.on_callback_query(
    filters.regex("^enable_buttons$")
)
async def enable_btn(
    client,
    query
):

    await enable_buttons(
        query.from_user.id
    )

    await query.answer(
        "Buttons Enabled ✅"
    )


@Client.on_callback_query(
    filters.regex("^disable_buttons$")
)
async def disable_btn(
    client,
    query
):

    await disable_buttons(
        query.from_user.id
    )

    await query.answer(
        "Buttons Disabled ❌"
    )
