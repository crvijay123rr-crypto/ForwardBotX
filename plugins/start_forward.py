from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from database.tasks import get_task
from database.settings import get_settings
from core.progress import generate_progress


@Client.on_callback_query(
    filters.regex("^start_(.+)")
)
async def start_forward(
    client,
    query
):

    task_id = query.data.split("_", 1)[1]

    task = await get_task(task_id)

    if not task:
        return await query.answer(
            "Task Not Found",
            show_alert=True
        )

    settings = await get_settings(
        query.from_user.id
    )

    total = task.get("total", 0)

    forwarded = task.get(
        "forwarded",
        0
    )

    topics = task.get(
        "topics_found",
        0
    )

    remaining = max(
        total - forwarded,
        0
    )

    bar, percent = generate_progress(
        forwarded,
        total
    )

    filename_mode = settings.get(
        "filename_mode",
        "keep_original"
    )

    keyboard = InlineKeyboardMarkup([

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
        ],

        [
            InlineKeyboardButton(
                "📚 Topics",
                callback_data=f"topics_{task_id}"
            ),

            InlineKeyboardButton(
                "🔄 Refresh",
                callback_data=f"refresh_{task_id}"
            )
        ]
    ])

    text = f"""
╔════❰ FORWARD STATUS ❱════╗

🆔 Task:
{task_id[:8]}

📢 Destination:
{task.get('destination_title','Unknown')}

━━━━━━━━━━━━━━

📦 Total : {total}

✅ Forwarded : {forwarded}

🔄 Remaining : {remaining}

📚 Topics : {topics}

📂 Filename :
{filename_mode}

📈 Progress :
{percent}%

{bar}

━━━━━━━━━━━━━━

⚙ Status :
READY

╚═══════════════════╝
"""

    await query.message.edit_text(
        text,
        reply_markup=keyboard
    )
