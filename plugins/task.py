from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from utils.states import *
from database.tasks import *

@Client.on_callback_query(filters.regex("^new_task$"))
async def new_task(client, query):

    user_id = query.from_user.id

    await create_task(user_id)

    FIRST_LINK[user_id] = True

    await query.message.edit_text(
        "🔗 Send First Message Link"
    )
