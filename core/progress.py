def generate_bar(percent):

    total_blocks = 20

    filled = int(
        (percent / 100) * total_blocks
    )

    empty = total_blocks - filled

    return (
        "█" * filled
        +
        "░" * empty
    )


def build_dashboard(task):

    total = task.get(
        "total",
        0
    )

    forwarded = task.get(
        "forwarded",
        0
    )

    duplicate = task.get(
        "duplicate",
        0
    )

    deleted = task.get(
        "deleted",
        0
    )

    skipped = task.get(
        "skipped",
        0
    )

    filtered = task.get(
        "filtered",
        0
    )

    topics = task.get(
        "topics_found",
        0
    )

    status = task.get(
        "status",
        "waiting"
    ).upper()

    remaining = max(
        total - forwarded,
        0
    )

    percent = 0

    if total > 0:

        percent = int(
            (
                forwarded / total
            ) * 100
        )

    bar = generate_bar(
        percent
    )

    text = f"""
╔════❰ FORWARD STATUS ❱════╗

📦 Total Messages : {total}

✅ Successfully Forwarded : {forwarded}

🔄 Remaining Messages : {remaining}

📚 Topics Found : {topics}

📑 Duplicate Messages : {duplicate}

🗑 Deleted Messages : {deleted}

⏭ Skipped Messages : {skipped}

🚫 Filtered Messages : {filtered}

📈 Progress : {percent}%

{bar}

⚡ Current Status : {status}

╚══════════════════════╝
"""

    return text


def build_completed_dashboard(task):

    total = task.get(
        "total",
        0
    )

    forwarded = task.get(
        "forwarded",
        0
    )

    duplicate = task.get(
        "duplicate",
        0
    )

    deleted = task.get(
        "deleted",
        0
    )

    skipped = task.get(
        "skipped",
        0
    )

    filtered = task.get(
        "filtered",
        0
    )

    topics = task.get(
        "topics_found",
        0
    )

    return f"""
╔════❰ FORWARD STATUS ❱════╗

📦 Total Messages : {total}

✅ Successfully Forwarded : {forwarded}

📚 Topics Found : {topics}

📑 Duplicate Messages : {duplicate}

🗑 Deleted Messages : {deleted}

⏭ Skipped Messages : {skipped}

🚫 Filtered Messages : {filtered}

📈 Progress : 100%

████████████████████

⚡ Current Status : COMPLETED

╚══════❰ FINISHED ❱══════╝
"""
