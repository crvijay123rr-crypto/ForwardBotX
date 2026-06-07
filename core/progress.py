from datetime import datetime


def progress_bar(current, total):

    if total <= 0:
        return "░░░░░░░░░░", 0

    percent = int(
        (current / total) * 100
    )

    filled = int(
        percent / 10
    )

    bar = (
        "█" * filled
        +
        "░" * (10 - filled)
    )

    return bar, percent


def remaining_messages(
    forwarded,
    total
):

    remaining = total - forwarded

    if remaining < 0:
        remaining = 0

    return remaining


def get_status(
    task_status
):

    status_map = {

        "waiting":
        "🟡 Waiting",

        "running":
        "🟢 Running",

        "paused":
        "⏸ Paused",

        "stopped":
        "🔴 Stopped",

        "completed":
        "✅ Completed"
    }

    return status_map.get(
        task_status,
        "❓ Unknown"
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

    status = get_status(
        task.get(
            "status",
            "waiting"
        )
    )

    remaining = remaining_messages(
        forwarded,
        total
    )

    bar, percent = progress_bar(
        forwarded,
        total
    )

    return f"""
╔════❰ ғᴏʀᴡᴀʀᴅ sᴛᴀᴛᴜs ❱════╗

📦 ᴛᴏᴛᴀʟ ᴍᴇssᴀɢᴇs : {total}

✅ ғᴏʀᴡᴀʀᴅᴇᴅ : {forwarded}

🔄 ʀᴇᴍᴀɪɴɪɴɢ : {remaining}

📚 ᴛᴏᴘɪᴄs : {topics}

📑 ᴅᴜᴘʟɪᴄᴀᴛᴇ : {duplicate}

🗑 ᴅᴇʟᴇᴛᴇᴅ : {deleted}

⏭ sᴋɪᴘᴘᴇᴅ : {skipped}

🚫 ғɪʟᴛᴇʀᴇᴅ : {filtered}

📈 ᴘʀᴏɢʀᴇss : {percent}%

{bar}

⚙ sᴛᴀᴛᴜs : {status}

╚════════════════════╝
"""
