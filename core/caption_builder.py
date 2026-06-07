import re


def extract_index(text):

    if not text:
        return ""

    match = re.search(
        r"Index\s*:\s*(.+)",
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    return ""


def extract_batch(text):

    if not text:
        return ""

    match = re.search(
        r"Batch\s*:\s*(.+)",
        text,
        re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    return ""


def build_caption(
    template,
    filename="",
    topic="",
    original_caption="",
    message_id=""
):

    if not template:
        return original_caption

    index = extract_index(
        original_caption
    )

    batch = extract_batch(
        original_caption
    )

    caption = template

    variables = {

        "{filename}": filename,

        "{topic}": topic,

        "{index}": index,

        "{batch}": batch,

        "{message_id}": str(
            message_id
        )
    }

    for key, value in variables.items():

        caption = caption.replace(
            key,
            str(value)
        )

    return caption
