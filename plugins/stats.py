from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from database.tasks import (
    get_user_tasks
)


@Client.on_callback_query(
    filters.regex("^stats_panel$")
)
async def stats_panel(
    client,
    query
):

    user_id = query.from_user.id

    total_tasks = 0
    total_forwarded = 0
    total_topics = 0
    total_duplicates = 0
    total_deleted = 0
    total_skipped = 0

    cursor = get_user_tasks(
        user_id
    )

    async for task in cursor:

        total_tasks += 1

        total_forwarded += task.get(
            "forwarded",
            0
        )

        total_topics += task.get(
            "topics_found",
            0
        )

        total_duplicates += task.get(
            "duplicate",
            0
        )

        total_deleted += task.get(
            "deleted",
            0
        )

        total_skipped += task.get(
            "skipped",
            0
        )

    text = f"""
📊 USER STATISTICS

━━━━━━━━━━━━━━

📂 Total Tasks:
{total_tasks}

📨 Total Forwarded:
{total_forwarded}

📚 Topics Found:
{total_topics}

♻️ Duplicates:
{total_duplicates}

🗑 Deleted:
{total_deleted}

⏭ Skipped:
{total_skipped}

━━━━━━━━━━━━━━

🚀 Forward Bot Pro
"""

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🏠 Back",
                callback_data="back_home"
            )
        ]
    ])

    await query.message.edit_text(
        text,
        reply_markup=keyboard
    )
