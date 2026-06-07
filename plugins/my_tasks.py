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

from core.progress import (
    build_dashboard
)


@Client.on_message(
    filters.private &
    filters.command("tasks")
)
async def my_tasks(
    client,
    message
):

    cursor = await get_user_tasks(
        message.from_user.id
    )

    tasks = []

    async for task in cursor:
        tasks.append(task)

    if not tasks:

        return await message.reply_text(
            "❌ No Tasks Found"
        )

    keyboard = []

    for task in tasks[:20]:

        task_id = task["task_id"]

        status = task.get(
            "status",
            "waiting"
        )

        keyboard.append([
            InlineKeyboardButton(
                f"{status.upper()} | {task_id[:8]}",
                callback_data=f"task_{task_id}"
            )
        ])

    await message.reply_text(
        "📋 YOUR TASKS",
        reply_markup=InlineKeyboardMarkup(
            keyboard
        )
    )


@Client.on_callback_query(
    filters.regex("^task_(.+)")
)
async def open_task(
    client,
    query
):

    task_id = query.data.split(
        "_",
        1
    )[1]

    task = await get_task(
        task_id
    )

    if not task:

        return await query.answer(
            "Task Not Found",
            show_alert=True
        )

    text = build_dashboard(
        task
    )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "▶ Resume",
                callback_data=f"resume_{task_id}"
            ),
            InlineKeyboardButton(
                "⏸ Pause",
                callback_data=f"pause_{task_id}"
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
                "🗑 Delete",
                callback_data=f"delete_{task_id}"
            )
        ]
    ])

    await query.message.edit_text(
        text,
        reply_markup=keyboard
    )


@Client.on_callback_query(
    filters.regex("^delete_(.+)")
)
async def delete_task_handler(
    client,
    query
):

    task_id = query.data.split(
        "_",
        1
    )[1]

    await delete_task(
        task_id
    )

    await query.answer(
        "Task Deleted ✅",
        show_alert=True
    )

    await query.message.edit_text(
        "🗑 Task Deleted Successfully"
    )
