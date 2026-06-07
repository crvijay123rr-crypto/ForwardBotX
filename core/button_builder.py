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

        text = button.get("text")
        url = button.get("url")

        if not text or not url:
            continue

        row.append(
            InlineKeyboardButton(
                text=text,
                url=url
            )
        )

        if len(row) == 2:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    if not keyboard:
        return None

    return InlineKeyboardMarkup(keyboard)


def build_topic_buttons(topics):

    if not topics:
        return None

    keyboard = []

    for topic in topics:

        topic_name = topic.get(
            "topic_name"
        )

        link = topic.get(
            "first_message_link"
        )

        if not topic_name or not link:
            continue

        keyboard.append([
            InlineKeyboardButton(
                text=f"📚 {topic_name[:50]}",
                url=link
            )
        ])

    if not keyboard:
        return None

    return InlineKeyboardMarkup(
        keyboard
    )


def build_mixed_buttons(
    custom_buttons,
    topic_buttons=None
):

    keyboard = []

    row = []

    if custom_buttons:

        for button in custom_buttons:

            text = button.get("text")
            url = button.get("url")

            if not text or not url:
                continue

            row.append(
                InlineKeyboardButton(
                    text=text,
                    url=url
                )
            )

            if len(row) == 2:
                keyboard.append(row)
                row = []

        if row:
            keyboard.append(row)

    if topic_buttons:

        for topic in topic_buttons:

            name = topic.get(
                "topic_name"
            )

            link = topic.get(
                "first_message_link"
            )

            if not name or not link:
                continue

            keyboard.append([
                InlineKeyboardButton(
                    text=f"📚 {name[:50]}",
                    url=link
                )
            ])

    if not keyboard:
        return None

    return InlineKeyboardMarkup(
        keyboard
    )
