import asyncio
from pyrogram.errors import FloodWait

# Saare Imports Upar (Top) par hone chahiye
from database.tasks import (
    get_task, update_many, increase_forwarded, 
    increase_deleted, increase_skipped, set_status
)
from database.topics import create_topic, increase_topic_count, get_all_topics
from core.topic_detector import detect_topic
from core.progress import build_dashboard, build_completed_dashboard
from database.captions import get_caption
from database.buttons import get_buttons
from core.caption_builder import build_caption
from core.button_builder import build_buttons
from core.summary_generator import build_topic_summary, build_completion_report

async def start_forwarding(client, task_id, status_message):
    task = await get_task(task_id)
    if not task:
        return

    first_id = int(task["first_link"])
    last_id = int(task["last_link"])
    destination_id = int(task["destination_id"])

    forwarded = 0
    deleted = 0
    skipped = 0
    topics_found = 0
    current_topic = None

    for message_id in range(first_id, last_id + 1):
        task = await get_task(task_id)
        if not task or task["status"] == "stopped":
            return

        while task["status"] == "paused":
            await asyncio.sleep(3)
            task = await get_task(task_id)

        try:
            source_chat = task.get("source_chat_id")
            message = await client.get_messages(source_chat, message_id)

            if not message:
                deleted += 1
                await increase_deleted(task_id)
                continue

            caption = message.caption or ""
            topic = detect_topic(caption)

            if topic:
                if topic != current_topic:
                    current_topic = topic
                    created = await create_topic(task_id, topic, message_id)
                    if created:
                        topics_found += 1
                else:
                    await increase_topic_count(task_id, topic)

            # File Name Logic
            filename = ""
            if message.document: filename = message.document.file_name or ""
            elif message.video: filename = message.video.file_name or ""
            elif message.audio: filename = message.audio.file_name or ""

            # Caption & Buttons
            caption_data = await get_caption(task["user_id"])
            final_caption = caption
            if caption_data and caption_data.get("enabled"):
                final_caption = build_caption(
                    template=caption_data.get("caption"),
                    filename=filename, topic=topic, batch="",
                    message_id=message_id, original_caption=caption
                )

            buttons_data = await get_buttons(task["user_id"])
            reply_markup = None
            if buttons_data and buttons_data.get("enabled"):
                reply_markup = build_buttons(buttons_data.get("buttons", []))

            # Forwarding
            try:
                await message.copy(chat_id=destination_id, caption=final_caption, reply_markup=reply_markup)
                forwarded += 1
                await increase_forwarded(task_id)
            except FloodWait as e:
                await asyncio.sleep(e.value)
                continue
            except Exception:
                skipped += 1
                await increase_skipped(task_id)
                continue

            # Update Progress
            if forwarded % 10 == 0:
                await update_many(task_id, {"forwarded": forwarded, "deleted": deleted, "skipped": skipped, "topics_found": topics_found})
                try:
                    dashboard = build_dashboard(await get_task(task_id))
                    await status_message.edit_text(dashboard)
                except: pass

        except Exception:
            deleted += 1
            await increase_deleted(task_id)
            continue

    # Completion Logic
    await update_many(task_id, {"forwarded": forwarded, "deleted": deleted, "skipped": skipped, "topics_found": topics_found, "remaining": 0, "percentage": 100})
    await set_status(task_id, "completed")
    
    # Dashboard & Reports
    try:
        await status_message.edit_text(build_completed_dashboard(await get_task(task_id)))
        topics_cursor = get_all_topics(task_id)
        text, markup = await build_topic_summary(task_id, topics_cursor)
        await client.send_message(destination_id, text, reply_markup=markup)
        await client.send_message(task["user_id"], build_completion_report(await get_task(task_id)))
    except: pass
        
