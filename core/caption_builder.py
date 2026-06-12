def safe(value):

    if value is None:
        return ""

    return str(value)


def build_caption(
    template,
    filename="",
    topic="",
    batch="",
    message_id="",
    original_caption=""
):

    if not template:

        return original_caption or ""

    caption = template

    variables = {

        "{filename}": safe(
            filename
        ),

        "{topic}": safe(
            topic
        ),

        "{batch}": safe(
            batch
        ),

        "{message_id}": safe(
            message_id
        ),

        "{original_caption}": safe(
            original_caption
        )
    }

    for key, value in variables.items():

        caption = caption.replace(
            key,
            value
        )

    return caption
