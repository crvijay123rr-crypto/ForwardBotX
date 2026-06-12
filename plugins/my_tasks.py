from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from database.tasks import (
    get_user_tasks,
    get_task,
    delete_task,
    set_status
)


# ==========================
# MY TASKS PANEL
# ==========================

@Client.on_callback_query(
    filters.regex("^my_tasks$")
)
async def my_tasks(
    client,
    query
):

    user_id = query.from_user.id

    cursor = await get_user_tasks(
        user_id
    )

    keyboard = []

    count = 0

    async for task in cursor:

        count += 1

        keyboard.append(
            [
                InlineKeyboardButton(
                    f"📂 Task {count}",
                    callback_data=f"task_{task['task_id']}"
                )
            ]
        )

    if not keyboard:

        return await query.message.edit_text(
            """
📂 MY TASKS

━━━━━━━━━━━━━━

❌ No Tasks Found
"""
        )

    keyboard.append(
        [
            InlineKeyboardButton(
                "🔙 Back",
                callback_data="back_home"
            )
        ]
    )

    await query.message.edit_text(
        """
📂 MY TASKS

Select A Task Below
""",
        reply_markup=InlineKeyboardMarkup(
            keyboard
        )
    )


# ==========================
# TASK DETAILS
# ==========================

@Client.on_callback_query(
    filters.regex("^task_")
)
async def task_details(
    client,
    query
):

    task_id = query.data.replace(
        "task_",
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

    text = f"""
📂 TASK DETAILS

━━━━━━━━━━━━━━

🆔 Task ID:
{task['task_id']}

📢 Destination:
{task.get('destination_title')}

📊 Status:
{task.get('status')}

📦 Total:
{task.get('total')}

✅ Forwarded:
{task.get('forwarded')}

━━━━━━━━━━━━━━
"""

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "▶ Start",
                callback_data=f"start_{task_id}"
            ),
            InlineKeyboardButton(
                "⏸ Pause",
                callback_data=f"pause_{task_id}"
            )
        ],
        [
            InlineKeyboardButton(
                "🔄 Resume",
                callback_data=f"resume_{task_id}"
            ),
            InlineKeyboardButton(
                "⛔ Stop",
                callback_data=f"stop_{task_id}"
            )
        ],
        [
            InlineKeyboardButton(
                "🗑 Delete",
                callback_data=f"delete_{task_id}"
            )
        ]
    ])

    await query.message.edit_text(
        text,
        reply_markup=keyboard
    )


# ==========================
# PAUSE
# ==========================

@Client.on_callback_query(
    filters.regex("^pause_")
)
async def pause_task(
    client,
    query
):

    task_id = query.data.replace(
        "pause_",
        ""
    )

    await set_status(
        task_id,
        "paused"
    )

    await query.answer(
        "Task Paused ⏸"
    )


# ==========================
# RESUME
# ==========================

@Client.on_callback_query(
    filters.regex("^resume_")
)
async def resume_task(
    client,
    query
):

    task_id = query.data.replace(
        "resume_",
        ""
    )

    await set_status(
        task_id,
        "running"
    )

    await query.answer(
        "Task Resumed ▶"
    )


# ==========================
# STOP
# ==========================

@Client.on_callback_query(
    filters.regex("^stop_")
)
async def stop_task(
    client,
    query
):

    task_id = query.data.replace(
        "stop_",
        ""
    )

    await set_status(
        task_id,
        "stopped"
    )

    await query.answer(
        "Task Stopped ⛔"
    )


# ==========================
# DELETE
# ==========================

@Client.on_callback_query(
    filters.regex("^delete_")
)
async def delete_task_handler(
    client,
    query
):

    task_id = query.data.replace(
        "delete_",
        ""
    )

    await delete_task(
        task_id
    )

    await query.message.edit_text(
        """
🗑 Task Deleted Successfully
"""
    )
