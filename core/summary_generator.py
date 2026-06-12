from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


async def build_topic_summary(
    task_id,
    topics_cursor
):

    topics = []

    async for topic in topics_cursor:

        topics.append(topic)

    total_topics = len(topics)

    text = f"""
📚 TOPIC INDEX

━━━━━━━━━━━━━━

📖 Total Topics : {total_topics}

━━━━━━━━━━━━━━

"""

    keyboard = []

    for topic in topics:

        topic_name = topic.get(
            "topic_name",
            "Unknown Topic"
        )

        topic_link = topic.get(
            "topic_link"
        )

        count = topic.get(
            "message_count",
            0
        )

        text += (
            f"🔹 {topic_name}"
            f" ({count})\n"
        )

        if topic_link:

            keyboard.append(
                [
                    InlineKeyboardButton(
                        text=f"📚 {topic_name}",
                        url=topic_link
                    )
                ]
            )

    text += """

━━━━━━━━━━━━━━

✅ Forward Completed
"""

    markup = None

    if keyboard:

        markup = InlineKeyboardMarkup(
            keyboard
        )

    return (
        text,
        markup
    )


def build_completion_report(
    task
):

    return f"""
🏁 TASK COMPLETED

━━━━━━━━━━━━━━

📦 Total Messages :
{task.get('total', 0)}

✅ Forwarded :
{task.get('forwarded', 0)}

📚 Topics :
{task.get('topics_found', 0)}

📑 Duplicate :
{task.get('duplicate', 0)}

🗑 Deleted :
{task.get('deleted', 0)}

⏭ Skipped :
{task.get('skipped', 0)}

🚫 Filtered :
{task.get('filtered', 0)}

━━━━━━━━━━━━━━

🎉 Forwarding Finished
"""
