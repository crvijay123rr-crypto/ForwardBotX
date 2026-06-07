from pyrogram import Client
from pyrogram import filters

from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from database.users import add_user

@Client.on_message(filters.command("start"))
async def start(client, message):

    await add_user(
        message.from_user.id
    )

    buttons = InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "➕ NEW TASK",
                callback_data="new_task"
            )
        ],

        [
            InlineKeyboardButton(
                "⚙ SETTINGS",
                callback_data="settings"
            ),

            InlineKeyboardButton(
                "📊 TASKS",
                callback_data="tasks"
            )
        ],

        [
            InlineKeyboardButton(
                "📝 CAPTION",
                callback_data="caption_panel"
            ),

            InlineKeyboardButton(
                "🔘 BUTTONS",
                callback_data="button_panel"
            )
        ],

        [
            InlineKeyboardButton(
                "📚 TOPICS",
                callback_data="topics"
            ),

            InlineKeyboardButton(
                "📈 STATS",
                callback_data="stats"
            )
        ]
    ])

    text = """
🚀 FORWARDBOT X

⚡ High Speed Forward System

📚 Smart Topic Detection

📝 Custom Caption System

🔘 Custom Button System

📊 Live Progress Tracking

━━━━━━━━━━━━━━━
Version : 1.0
━━━━━━━━━━━━━━━
"""

    await message.reply_text(
        text,
        reply_markup=buttons
    )
