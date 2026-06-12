from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


async def build_topic_summary(
    task_id,
    topics_cursor
):

    text = """
📚 TOPIC INDEX

━━━━━━━━━━━━━━

Select Topic Below
"""

    keyboard = []

    async for topic in topics_cursor:

        topic_name = topic.get(
            "topic_name",
            "Unknown"
        )

        topic_link = topic.get(
            "topic_link"
        )

        count = topic.get(
            "message_count",
            0
        )

        if not topic_link:
            continue

        keyboard.append(
            [
                InlineKeyboardButton(
                    f"{topic_name} ({count})",
                    url=topic_link
                )
            ]
        )

    if not keyboard:

        keyboard.append(
            [
                InlineKeyboardButton(
                    "❌ No Topics Found",
                    callback_data="no_topics"
                )
            ]
        )

    return (
        text,
        InlineKeyboardMarkup(
            keyboard
        )
    )


def build_topic_link(
    destination_username,
    message_id
):

    if not destination_username:
        return None

    return (
        f"https://t.me/"
        f"{destination_username}/"
        f"{message_id}"
    )


def build_private_topic_link(
    destination_id,
    message_id
):

    channel_id = str(
        destination_id
    ).replace(
        "-100",
        ""
    )

    return (
        f"https://t.me/c/"
        f"{channel_id}/"
        f"{message_id}"
    )
