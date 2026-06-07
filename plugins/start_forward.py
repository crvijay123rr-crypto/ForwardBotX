from pyrogram import Client, filters
from pyrogram.types import CallbackQuery

from database.tasks import get_task

@Client.on_callback_query(filters.regex("^start_forward$"))
async def start_forward(client, query):

    user_id = query.from_user.id

    task = await get_task(user_id)

    txt = f"""
🚀 TASK STARTED

🔗 First Link:
{task['first_link']}

🔗 Last Link:
{task['last_link']}

📢 Destination:
{task['destination']}

📊 Status:
Initializing...
"""

    await query.message.edit_text(txt)
