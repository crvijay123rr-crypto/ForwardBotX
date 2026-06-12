from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from database.settings import (
    get_settings,
    update_setting
)


# ==========================
# SETTINGS PANEL
# ==========================

@Client.on_callback_query(
    filters.regex("^settings_panel$")
)
async def settings_panel(
    client,
    query
):

    settings = await get_settings(
        query.from_user.id
    )

    speed = settings.get(
        "speed",
        0
    )

    auto_topic = settings.get(
        "auto_topic",
        True
    )

    auto_summary = settings.get(
        "auto_summary",
        True
    )

    rename_mode = settings.get(
        "rename_mode",
        "keep"
    )

    text = f"""
⚙ FORWARD SETTINGS

━━━━━━━━━━━━━━

🚀 Speed:
{speed}

📚 Auto Topic:
{'✅ ON' if auto_topic else '❌ OFF'}

📝 Auto Summary:
{'✅ ON' if auto_summary else '❌ OFF'}

📂 Rename Mode:
{rename_mode.upper()}

━━━━━━━━━━━━━━
"""

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🚀 Speed",
                callback_data="speed_settings"
            )
        ],
        [
            InlineKeyboardButton(
                "📚 Topic",
                callback_data="toggle_topic"
            ),
            InlineKeyboardButton(
                "📝 Summary",
                callback_data="toggle_summary"
            )
        ],
        [
            InlineKeyboardButton(
                "📂 Keep",
                callback_data="rename_keep"
            ),
            InlineKeyboardButton(
                "✏ Rename",
                callback_data="rename_custom"
            )
        ],
        [
            InlineKeyboardButton(
                "🔄 Reset",
                callback_data="reset_settings"
            )
        ]
    ])

    await query.message.edit_text(
        text,
        reply_markup=keyboard
    )


# ==========================
# TOPIC TOGGLE
# ==========================

@Client.on_callback_query(
    filters.regex("^toggle_topic$")
)
async def toggle_topic(
    client,
    query
):

    settings = await get_settings(
        query.from_user.id
    )

    value = not settings.get(
        "auto_topic",
        True
    )

    await update_setting(
        query.from_user.id,
        "auto_topic",
        value
    )

    await query.answer(
        "Topic Setting Updated"
    )


# ==========================
# SUMMARY TOGGLE
# ==========================

@Client.on_callback_query(
    filters.regex("^toggle_summary$")
)
async def toggle_summary(
    client,
    query
):

    settings = await get_settings(
        query.from_user.id
    )

    value = not settings.get(
        "auto_summary",
        True
    )

    await update_setting(
        query.from_user.id,
        "auto_summary",
        value
    )

    await query.answer(
        "Summary Setting Updated"
    )


# ==========================
# KEEP ORIGINAL
# ==========================

@Client.on_callback_query(
    filters.regex("^rename_keep$")
)
async def rename_keep(
    client,
    query
):

    await update_setting(
        query.from_user.id,
        "rename_mode",
        "keep"
    )

    await query.answer(
        "Keep Original Enabled"
    )


# ==========================
# RENAME
# ==========================

@Client.on_callback_query(
    filters.regex("^rename_custom$")
)
async def rename_custom(
    client,
    query
):

    await update_setting(
        query.from_user.id,
        "rename_mode",
        "rename"
    )

    await query.answer(
        "Rename Mode Enabled"
    )


# ==========================
# RESET
# ==========================

@Client.on_callback_query(
    filters.regex("^reset_settings$")
)
async def reset_settings(
    client,
    query
):

    await update_setting(
        query.from_user.id,
        "speed",
        0
    )

    await update_setting(
        query.from_user.id,
        "auto_topic",
        True
    )

    await update_setting(
        query.from_user.id,
        "auto_summary",
        True
    )

    await update_setting(
        query.from_user.id,
        "rename_mode",
        "keep"
    )

    await query.answer(
        "Settings Reset Complete"
    )


# ==========================
# SPEED PANEL
# ==========================

@Client.on_callback_query(
    filters.regex("^speed_settings$")
)
async def speed_settings(
    client,
    query
):

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🐢 Slow",
                callback_data="speed_2"
            ),
            InlineKeyboardButton(
                "⚡ Normal",
                callback_data="speed_0"
            )
        ],
        [
            InlineKeyboardButton(
                "🚀 Fast",
                callback_data="speed_1"
            )
        ]
    ])

    await query.message.edit_text(
        """
🚀 SELECT FORWARD SPEED
""",
        reply_markup=keyboard
    )


@Client.on_callback_query(
    filters.regex("^speed_")
)
async def set_speed(
    client,
    query
):

    speed = int(
        query.data.split("_")[1]
    )

    await update_setting(
        query.from_user.id,
        "speed",
        speed
    )

    await query.answer(
        "Speed Updated"
    )
