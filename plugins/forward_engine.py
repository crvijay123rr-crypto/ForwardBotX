import asyncio

from pyrogram.errors import (
    FloodWait
)

from database.tasks import (
    get_task,
    update_many,
    increase_forwarded,
    increase_deleted,
    increase_skipped,
    set_status
)

from database.topics import (
    create_topic,
    increase_topic_count
)

from core.topic_detector import (
    detect_topic
)

from core.progress import (
    build_dashboard,
    build_completed_dashboard
)


async def start_forwarding(
    client,
    task_id,
    status_message
):

    task = await get_task(
        task_id
    )

    if not task:
        return

    first_id = int(
        task["first_link"]
    )

    last_id = int(
        task["last_link"]
    )

    destination_id = int(
        task["destination_id"]
    )

    forwarded = 0

    deleted = 0

    skipped = 0

    topics_found = 0

    current_topic = None

    for message_id in range(
        first_id,
        last_id + 1
    ):

        task = await get_task(
            task_id
        )

        if not task:
            return

        # STOP

        if task["status"] == "stopped":

            return

        # PAUSE

        while task["status"] == "paused":

            await asyncio.sleep(
                3
            )

            task = await get_task(
                task_id
            )

        try:

            source_chat = task.get(
                "source_chat_id"
            )

            message = await client.get_messages(
                source_chat,
                message_id
            )

            if not message:

                deleted += 1

                await increase_deleted(
                    task_id
                )

                continue

            caption = ""

            if message.caption:

                caption = (
                    message.caption
                )

            topic = detect_topic(
                caption
            )

            if topic:

                if topic != current_topic:

                    current_topic = topic

                    created = await create_topic(
                        task_id,
                        topic,
                        message_id
                    )

                    if created:

                        topics_found += 1

                else:

                    await increase_topic_count(
                        task_id,
                        topic
          )
from database.captions import (
    get_caption
)

from database.buttons import (
    get_buttons
)

from core.caption_builder import (
    build_caption
)

from core.button_builder import (
    build_buttons
)


            # ==========================
            # FILE NAME
            # ==========================

            filename = ""

            if message.document:

                filename = (
                    message.document.file_name
                    or ""
                )

            elif message.video:

                filename = (
                    message.video.file_name
                    or ""
                )

            elif message.audio:

                filename = (
                    message.audio.file_name
                    or ""
                )

            # ==========================
            # CUSTOM CAPTION
            # ==========================

            caption_data = await get_caption(
                task["user_id"]
            )

            final_caption = caption

            if caption_data:

                if caption_data.get(
                    "enabled"
                ):

                    final_caption = build_caption(

                        template=caption_data.get(
                            "caption"
                        ),

                        filename=filename,

                        topic=topic,

                        batch="",

                        message_id=message_id,

                        original_caption=caption

                    )

            # ==========================
            # BUTTONS
            # ==========================

            buttons_data = await get_buttons(
                task["user_id"]
            )

            reply_markup = None

            if buttons_data:

                if buttons_data.get(
                    "enabled"
                ):

                    reply_markup = build_buttons(
                        buttons_data.get(
                            "buttons",
                            []
                        )
                    )

            # ==========================
            # FORWARD MESSAGE
            # ==========================

            try:

                await message.copy(

                    chat_id=destination_id,

                    caption=final_caption,

                    reply_markup=reply_markup

                )

                forwarded += 1

                await increase_forwarded(
                    task_id
                )

            except FloodWait as e:

                await asyncio.sleep(
                    e.value
                )

                continue

            except Exception:

                skipped += 1

                await increase_skipped(
                    task_id
                )

                continue

            # ==========================
            # UPDATE PROGRESS
            # ==========================

            if forwarded % 10 == 0:

                await update_many(

                    task_id,

                    {

                        "forwarded":
                        forwarded,

                        "deleted":
                        deleted,

                        "skipped":
                        skipped,

                        "topics_found":
                        topics_found

                    }

                )

                fresh_task = await get_task(
                    task_id
                )

                dashboard = build_dashboard(
                    fresh_task
                )

                try:

                    await status_message.edit_text(
                        dashboard
                    )

                except:

                    pass

        except Exception:

            deleted += 1

            await increase_deleted(
                task_id
            )

            continue                  
from database.topics import (
    get_all_topics
)

from core.summary_generator import (
    build_topic_summary,
    build_completion_report
)


    # ==========================
    # FORWARD COMPLETED
    # ==========================

    await update_many(
        task_id,
        {
            "forwarded": forwarded,
            "deleted": deleted,
            "skipped": skipped,
            "topics_found": topics_found,
            "remaining": 0,
            "percentage": 100
        }
    )

    await set_status(
        task_id,
        "completed"
    )

    # ==========================
    # COMPLETED DASHBOARD
    # ==========================

    completed_task = await get_task(
        task_id
    )

    dashboard = build_completed_dashboard(
        completed_task
    )

    try:

        await status_message.edit_text(
            dashboard
        )

    except:

        pass

    # ==========================
    # TOPIC LINKS BUILD
    # ==========================

    topics_cursor = get_all_topics(
        task_id
    )

    topic_text, topic_markup = await build_topic_summary(
        task_id,
        topics_cursor
    )

    try:

        await client.send_message(

            destination_id,

            topic_text,

            reply_markup=topic_markup

        )

    except:

        pass

    # ==========================
    # COMPLETION REPORT
    # ==========================

    report = build_completion_report(
        completed_task
    )

    try:

        await client.send_message(

            task["user_id"],

            report

        )

    except:

        pass
