from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from config import OWNER_ID

from database.users import (
    total_users,
    get_all_users
)

from database.tasks import (
    get_task
)

from database.bans import (
    ban_user,
    unban_user,
    total_banned
)

from utils.states import (
    WAITING_BROADCAST,
    WAITING_BAN_USER,
    WAITING_UNBAN_USER
)


# ==========================
# ADMIN PANEL
# ==========================

@Client.on_message(
    filters.private &
    filters.command("admin")
)
async def admin_panel(
    client,
    message
):

    if message.from_user.id != OWNER_ID:
        return

    users = await total_users()

    banned = await total_banned()

    text = f"""
👑 ADMIN PANEL

━━━━━━━━━━━━━━

👥 Total Users:
{users}

🚫 Banned Users:
{banned}

━━━━━━━━━━━━━━
"""

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📢 Broadcast",
                callback_data="broadcast"
            )
        ],
        [
            InlineKeyboardButton(
                "🚫 Ban User",
                callback_data="ban_user"
            ),
            InlineKeyboardButton(
                "✅ Unban User",
                callback_data="unban_user"
            )
        ]
    ])

    await message.reply_text(
        text,
        reply_markup=keyboard
    )


# ==========================
# BROADCAST
# ==========================

@Client.on_callback_query(
    filters.regex("^broadcast$")
)
async def broadcast_panel(
    client,
    query
):

    WAITING_BROADCAST[
        query.from_user.id
    ] = True

    await query.message.edit_text(
        """
📢 Send Broadcast Message
"""
    )


# ==========================
# BAN USER
# ==========================

@Client.on_callback_query(
    filters.regex("^ban_user$")
)
async def ban_user_panel(
    client,
    query
):

    WAITING_BAN_USER[
        query.from_user.id
    ] = True

    await query.message.edit_text(
        """
🚫 Send User ID To Ban
"""
    )


# ==========================
# UNBAN USER
# ==========================

@Client.on_callback_query(
    filters.regex("^unban_user$")
)
async def unban_user_panel(
    client,
    query
):

    WAITING_UNBAN_USER[
        query.from_user.id
    ] = True

    await query.message.edit_text(
        """
✅ Send User ID To Unban
"""
    )


# ==========================
# ADMIN INPUT HANDLER
# ==========================

@Client.on_message(
    filters.private &
    filters.text
)
async def admin_input(
    client,
    message
):

    if message.from_user.id != OWNER_ID:
        return

    user_id = message.from_user.id

    # BROADCAST

    if user_id in WAITING_BROADCAST:

        WAITING_BROADCAST.pop(
            user_id
        )

        sent = 0

        failed = 0

        async for user in get_all_users():

            try:

                await client.send_message(
                    user["user_id"],
                    message.text
                )

                sent += 1

            except:

                failed += 1

        return await message.reply_text(
            f"""
📢 BROADCAST COMPLETED

✅ Sent:
{sent}

❌ Failed:
{failed}
"""
        )

    # BAN

    if user_id in WAITING_BAN_USER:

        WAITING_BAN_USER.pop(
            user_id
        )

        try:

            target = int(
                message.text
            )

            await ban_user(
                target
            )

            return await message.reply_text(
                "🚫 User Banned"
            )

        except:

            return await message.reply_text(
                "❌ Invalid User ID"
            )

    # UNBAN

    if user_id in WAITING_UNBAN_USER:

        WAITING_UNBAN_USER.pop(
            user_id
        )

        try:

            target = int(
                message.text
            )

            await unban_user(
                target
            )

            return await message.reply_text(
                "✅ User Unbanned"
            )

        except:

            return await message.reply_text(
                "❌ Invalid User ID"
)
