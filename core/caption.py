def build_caption(
    template,
    filename,
    topic
):

    template = template.replace(
        "{filename}",
        filename
    )

    template = template.replace(
        "{topic}",
        topic
    )

    return template
