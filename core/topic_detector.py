import re


def extract_topic(caption):

    if not caption:
        return None

    patterns = [

        r"Topic\s*:\s*(.+)",

        r"topic\s*:\s*(.+)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            caption,
            re.IGNORECASE
        )

        if match:

            topic = match.group(1)

            topic = topic.split("\n")[0]

            topic = topic.strip()

            if topic:
                return topic

    return None


def normalize_topic(topic):

    if not topic:
        return None

    topic = topic.strip()

    topic = re.sub(
        r"\s+",
        " ",
        topic
    )

    return topic


def detect_topic(caption):

    topic = extract_topic(
        caption
    )

    topic = normalize_topic(
        topic
    )

    return topic
