def progress_bar(
    current,
    total
):

    percent = round(
        current * 100 / total
    )

    done = int(percent / 10)

    bar = (
        "█" * done
        +
        "░" * (10 - done)
    )

    return bar, percent
