import re

def extract_topic(caption):

    if not caption:
        return "Unknown"

    match = re.search(
        r"Topic\s*:\s*(.+)",
        caption,
        re.IGNORECASE
    )

    if match:
        topic = match.group(1).strip()

        topic = topic.split("\n")[0]

        return topic

    return "Unknown"
