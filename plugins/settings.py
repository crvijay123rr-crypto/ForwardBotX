from pyrogram import Client
from pyrogram.types import CallbackQuery
from pyrogram.types import InlineKeyboardMarkup
from pyrogram.types import InlineKeyboardButton

@Client.on_callback_query()
async def callbacks(client, query):

    data = query.data

    if data == "settings":

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "📝 Caption",
                    callback_data="caption"
                )
            ],
            [
                InlineKeyboardButton(
                    "🔘 Buttons",
                    callback_data="buttons"
                )
            ],
            [
                InlineKeyboardButton(
                    "📂 Filename",
                    callback_data="filename"
                )
            ]
        ])

        await query.message.edit_text(
            "⚙ Settings Panel",
            reply_markup=keyboard
        )
