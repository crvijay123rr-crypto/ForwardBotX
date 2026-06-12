import re


def parse_link(
    link
):

    link = link.strip()

    # ==========================
    # PUBLIC LINK
    # ==========================

    public_pattern = r"https:\/\/t\.me\/([^\/]+)\/(\d+)"

    public_match = re.match(
        public_pattern,
        link
    )

    if public_match:

        username = public_match.group(
            1
        )

        message_id = int(
            public_match.group(
                2
            )
        )

        return {

            "type": "public",

            "chat": username,

            "username": username,

            "message_id": message_id
        }

    # ==========================
    # PRIVATE LINK
    # ==========================

    private_pattern = r"https:\/\/t\.me\/c\/(\d+)\/(\d+)"

    private_match = re.match(
        private_pattern,
        link
    )

    if private_match:

        chat_id = int(
            "-100" +
            private_match.group(
                1
            )
        )

        message_id = int(
            private_match.group(
                2
            )
        )

        return {

            "type": "private",

            "chat": chat_id,

            "username": None,

            "message_id": message_id
        }

    return None


def get_message_id(
    link
):

    data = parse_link(
        link
    )

    if not data:

        return None

    return data[
        "message_id"
    ]


def get_chat(
    link
):

    data = parse_link(
        link
    )

    if not data:

        return None

    return data[
        "chat"
    ]


def is_public(
    link
):

    data = parse_link(
        link
    )

    if not data:

        return False

    return (
        data["type"]
        ==
        "public"
    )


def is_private(
    link
):

    data = parse_link(
        link
    )

    if not data:

        return False

    return (
        data["type"]
        ==
        "private"
    )
