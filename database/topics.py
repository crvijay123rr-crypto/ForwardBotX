from database.mongo import topics


async def create_topic(
    task_id,
    topic_name,
    first_message_id
):

    topic = await topics.find_one(
        {
            "task_id": task_id,
            "topic_name": topic_name
        }
    )

    if topic:
        return False

    await topics.insert_one(
        {
            "task_id": task_id,

            "topic_name": topic_name,

            "first_message_id": first_message_id,

            "message_count": 1
        }
    )

    return True


async def get_topic(
    task_id,
    topic_name
):

    return await topics.find_one(
        {
            "task_id": task_id,
            "topic_name": topic_name
        }
    )


async def increase_topic_count(
    task_id,
    topic_name
):

    await topics.update_one(
        {
            "task_id": task_id,
            "topic_name": topic_name
        },
        {
            "$inc": {
                "message_count": 1
            }
        }
    )


async def get_all_topics(
    task_id
):

    return topics.find(
        {
            "task_id": task_id
        }
    )


async def total_topics(
    task_id
):

    return await topics.count_documents(
        {
            "task_id": task_id
        }
    )


async def delete_topics(
    task_id
):

    await topics.delete_many(
        {
            "task_id": task_id
        }
    )
