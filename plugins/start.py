from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.users import add_user

START_TEXT = """
🚀 FORWARD BOT PRO

━━━━━━━━━━━━━━

⚡ Ultra Fast Forwarding

📚 Smart Topic Detection

📝 Custom Captions

🔘 Custom Buttons

📊 Live Progress Tracking

🔄 Pause / Resume / Stop

━━━━━━━━━━━━━━

Select An Option Below 👇
"""

@Client.on_message(filters.private & filters.command("start"))
async def start_command(client, message):
    # Debugging: User ka process track karne ke liye
    try:
        print(f"DEBUG: Trying to add user {message.from_user.id} to database...")
        await add_user(message.from_user)
        print("DEBUG: User processed successfully.")
    except Exception as e:
        # Agar error aayi, toh wo yahan print ho jayegi
        print(f"❌ CRITICAL ERROR in add_user: {e}")

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 New Task", callback_data="new_task")],
        [
            InlineKeyboardButton("📂 My Tasks", callback_data="my_tasks"),
            InlineKeyboardButton("⚙ Settings", callback_data="settings_panel")
        ],
        [
            InlineKeyboardButton("📝 Caption", callback_data="caption_panel"),
            InlineKeyboardButton("🔘 Buttons", callback_data="buttons_panel")
        ],
        [InlineKeyboardButton("📊 Statistics", callback_data="stats_panel")],
        [InlineKeyboardButton("ℹ Help", callback_data="help_panel")]
    ])

    await message.reply_text(
        START_TEXT,
        reply_markup=keyboard
    )
    
