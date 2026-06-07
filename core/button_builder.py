from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def build_buttons(buttons_data):

    if not buttons_data:
        return None

    keyboard = []

    row = []

    for button in buttons_data:

        text = button.get(
            "text"
        )

        url = button.get(
            "url"
        )

        if not text or not url:
            continue

        row.append(

            InlineKeyboardButton(
                text=text,
                url=url
            )

        )

        if len(row) == 2:

            keyboard.append(
                row
            )

            row = []

    if row:

        keyboard.append(
            row
        )

    if not keyboard:
        return None

    return InlineKeyboardMarkup(
        keyboard
    )
