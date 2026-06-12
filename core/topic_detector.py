import re


TOPIC_PATTERNS = [

    r"Topic:\s*(.+)",

    r"Subject:\s*(.+)",

    r"Chapter:\s*(.+)",

    r"Unit:\s*(.+)"
]


def clean_topic(topic):

    if not topic:
        return None

    topic = topic.strip()

    topic = topic.replace(
        "\n",
        ""
    )

    topic = topic.replace(
        "\r",
        ""
    )

    return topic[:100]


def detect_topic(text):

    if not text:
        return None

    for pattern in TOPIC_PATTERNS:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            topic = match.group(
                1
            )

            return clean_topic(
                topic
            )

    return None
