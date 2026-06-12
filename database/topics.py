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

        "first_message_link": None,

        "topic_link": None,

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

async def save_topic_link(
task_id,
topic_name,
link
):

await topics.update_one(
    {
        "task_id": task_id,
        "topic_name": topic_name
    },
    {
        "$set": {
            "first_message_link": link,
            "topic_link": link
        }
    }
)

async def update_topic_link(
task_id,
topic_name,
topic_link
):

await topics.update_one(
    {
        "task_id": task_id,
        "topic_name": topic_name
    },
    {
        "$set": {
            "topic_link": topic_link
        }
    }
)

async def get_topic_link(
task_id,
topic_name
):

topic = await topics.find_one(
    {
        "task_id": task_id,
        "topic_name": topic_name
    }
)

if not topic:
    return None

return topic.get(
    "topic_link"
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

async def delete_topic(
task_id,
topic_name
):

await topics.delete_one(
    {
        "task_id": task_id,
        "topic_name": topic_name
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

async def topic_exists(
task_id,
topic_name
):

topic = await topics.find_one(
    {
        "task_id": task_id,
        "topic_name": topic_name
    }
)

return bool(topic)

async def get_topic_count(
task_id,
topic_name
):

topic = await topics.find_one(
    {
        "task_id": task_id,
        "topic_name": topic_name
    }
)

if not topic:
    return 0

return topic.get(
    "message_count",
    0
)

async def rename_topic(
task_id,
old_name,
new_name
):

await topics.update_one(
    {
        "task_id": task_id,
        "topic_name": old_name
    },
    {
        "$set": {
            "topic_name": new_name
        }
    }
)

async def get_top_topics(
task_id,
limit=10
):

cursor = topics.find(
    {
        "task_id": task_id
    }
).sort(
    "message_count",
    -1
).limit(limit)

result = []

async for topic in cursor:
    result.append(topic)

return result
