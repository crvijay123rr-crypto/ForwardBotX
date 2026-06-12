from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def build_buttons(
    buttons_data
):

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

        if not text:
            continue

        if not url:
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


def build_single_button(
    text,
    url
):

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=text,
                    url=url
                )
            ]
        ]
    )


def build_topic_buttons(
    topics
):

    if not topics:

        return None

    keyboard = []

    for topic in topics:

        topic_name = topic.get(
            "topic_name"
        )

        topic_link = topic.get(
            "topic_link"
        )

        if not topic_name:
            continue

        if not topic_link:
            continue

        keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"📚 {topic_name}",
                    url=topic_link
                )
            ]
        )

    if not keyboard:

        return None

    return InlineKeyboardMarkup(
        keyboard
    )


def build_control_buttons(
    task_id
):

    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "⏸ Pause",
                    callback_data=f"pause_{task_id}"
                ),
                InlineKeyboardButton(
                    "▶ Resume",
                    callback_data=f"resume_{task_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    "⛔ Stop",
                    callback_data=f"stop_{task_id}"
                )
            ]
        ]
    )
