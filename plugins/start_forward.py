from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

import asyncio

from database.tasks import (
    get_task,
    update_many,
    set_status
)

from core.progress import (
    build_dashboard
)

from plugins.forward_engine import (
    start_forwarding
)


# ==========================
# START TASK
# ==========================

@Client.on_callback_query(
    filters.regex("^start_")
)
async def start_task(
    client,
    query
):

    task_id = query.data.replace(
        "start_",
        ""
    )

    task = await get_task(
        task_id
    )

    if not task:

        return await query.answer(
            "Task Not Found",
            show_alert=True
        )

    first_id = int(
        task["first_link"]
    )

    last_id = int(
        task["last_link"]
    )

    total = (
        last_id
        -
        first_id
        +
        1
    )

    await update_many(
        task_id,
        {
            "total": total,
            "remaining": total,
            "status": "running"
        }
    )

    task = await get_task(
        task_id
    )

    dashboard = build_dashboard(
        task
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
        ]
    ])

    status_message = await query.message.reply_text(
        dashboard,
        reply_markup=keyboard
    )

    asyncio.create_task(

        start_forwarding(
            client,
            task_id,
            status_message
        )

    )

    await query.answer(
        "Forward Started 🚀"
    )
