from pyrogram import Client, filters
from pyrogram.types import (
InlineKeyboardMarkup,
InlineKeyboardButton
)

HELP_TEXT = """
📚 FORWARD BOT HELP

━━━━━━━━━━━━━━

🚀 NEW TASK
Create a new forwarding task.

🔗 FIRST LINK
Send first message link.

🔗 LAST LINK
Send last message link.

📢 DESTINATION
Send destination channel.

📝 CAPTION
Set custom captions.

🔘 BUTTONS
Add custom URL buttons.

⚙ SETTINGS
Configure bot behavior.

📂 MY TASKS
View your created tasks.

━━━━━━━━━━━━━━

🛠 FEATURES

✅ Auto Topic Detection
✅ Topic Index
✅ Custom Caption
✅ Custom Buttons
✅ Pause / Resume
✅ Stop Task
✅ Live Progress
✅ Summary Report

━━━━━━━━━━━━━━

Need Support?
Contact Bot Admin.
"""

@Client.on_callback_query(
filters.regex("^help_panel$")
)
async def help_panel(
client,
query
):

keyboard = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            "🏠 Back",
            callback_data="back_home"
        )
    ]
])

await query.message.edit_text(
    HELP_TEXT,
    reply_markup=keyboard
)

@Client.on_callback_query(
filters.regex("^back_home$")
)
async def back_home(
client,
query
):

keyboard = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(
            "🚀 New Task",
            callback_data="new_task"
        )
    ],
    [
        InlineKeyboardButton(
            "📂 My Tasks",
            callback_data="my_tasks"
        ),
        InlineKeyboardButton(
            "⚙ Settings",
            callback_data="settings_panel"
        )
    ],
    [
        InlineKeyboardButton(
            "📝 Caption",
            callback_data="caption_panel"
        ),
        InlineKeyboardButton(
            "🔘 Buttons",
            callback_data="buttons_panel"
        )
    ],
    [
        InlineKeyboardButton(
            "📊 Statistics",
            callback_data="stats_panel"
        ),
        InlineKeyboardButton(
            "ℹ Help",
            callback_data="help_panel"
        )
    ]
])

await query.message.edit_text(
    """

🚀 FORWARD BOT PRO

Select An Option Below 👇
""",
reply_markup=keyboard
)
