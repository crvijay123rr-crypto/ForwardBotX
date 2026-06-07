from pyrogram import Client, filters

from utils.states import *
from database.tasks import *

@Client.on_message(filters.private & filters.text)
async def link_handler(client, message):

    user_id = message.from_user.id

    if FIRST_LINK.get(user_id):

        FIRST_LINK.pop(user_id)

        await set_first_link(
            user_id,
            message.text
        )

        LAST_LINK[user_id] = True

        return await message.reply_text(
            "🔗 Send Last Message Link"
        )

    if LAST_LINK.get(user_id):

        LAST_LINK.pop(user_id)

        await set_last_link(
            user_id,
            message.text
        )

        DESTINATION[user_id] = True

        return await message.reply_text(
            "📢 Send Destination Channel Username\n\nExample:\n@mychannel"
        )

    if DESTINATION.get(user_id):

        DESTINATION.pop(user_id)

        await set_destination(
            user_id,
            message.text
        )

        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🚀 Start Task",
                    callback_data="start_forward"
                )
            ]
        ])

        return await message.reply_text(
            "✅ Task Created Successfully",
            reply_markup=keyboard
        )
