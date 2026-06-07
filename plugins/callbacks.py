from pyrogram import Client
from pyrogram import filters

@Client.on_callback_query()
async def callback_router(
    client,
    query
):

    data = query.data

    print(
        f"Callback : {data}"
    )
