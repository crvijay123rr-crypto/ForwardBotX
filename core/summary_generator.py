from database.topics import get_all_topics


async def generate_summary(task_id):

    cursor = await get_all_topics(
        task_id
    )

    topics = []

    async for topic in cursor:

        topics.append(
            topic
        )

    if not topics:

        return """
📚 TOPIC INDEX

No Topics Found
"""

    text = """
📚 TOPIC INDEX

━━━━━━━━━━━━━━

"""

    count = 1

    for topic in topics:

        topic_name = topic.get(
            "topic_name",
            "Unknown"
        )

        total = topic.get(
            "message_count",
            0
        )

        text += (
            f"{count}. {topic_name}\n"
            f"   📦 Files : {total}\n\n"
        )

        count += 1

    text += "━━━━━━━━━━━━━━"

    return text
