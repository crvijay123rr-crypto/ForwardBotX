from database.mongo import topics

async def save_topic(
    task_id,
    topic_name,
    msg_id
):

    data = await topics.find_one(
        {
            "task_id": task_id,
            "topic": topic_name
        }
    )

    if data:
        return

    await topics.insert_one(
        {
            "task_id": task_id,
            "topic": topic_name,
            "first_message": msg_id
        }
    )

async def get_topics(task_id):

    return topics.find(
        {"task_id": task_id}
    )
