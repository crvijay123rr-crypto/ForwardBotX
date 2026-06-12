# ==========================
# TASK STATES
# ==========================

FIRST_LINK = {}

LAST_LINK = {}

DESTINATION = {}

RENAME_MODE = {}

TASK_RUNNING = {}

TASK_PAUSED = {}

TASK_STOPPED = {}


# ==========================
# CAPTION STATES
# ==========================

WAITING_CAPTION = {}

EDIT_CAPTION = {}


# ==========================
# BUTTON STATES
# ==========================

WAITING_BUTTON_TEXT = {}

WAITING_BUTTON_URL = {}

TEMP_BUTTON = {}


# ==========================
# SETTINGS STATES
# ==========================

WAITING_SPEED = {}

WAITING_TOPIC_NAME = {}

WAITING_TOPIC_LINK = {}


# ==========================
# ADMIN STATES
# ==========================

WAITING_BROADCAST = {}

WAITING_BAN_USER = {}

WAITING_UNBAN_USER = {}

WAITING_DELETE_TASK = {}


# ==========================
# CLEANUP HELPERS
# ==========================

def clear_task_states(user_id):

    FIRST_LINK.pop(user_id, None)

    LAST_LINK.pop(user_id, None)

    DESTINATION.pop(user_id, None)

    RENAME_MODE.pop(user_id, None)


def clear_caption_states(user_id):

    WAITING_CAPTION.pop(user_id, None)

    EDIT_CAPTION.pop(user_id, None)


def clear_button_states(user_id):

    WAITING_BUTTON_TEXT.pop(user_id, None)

    WAITING_BUTTON_URL.pop(user_id, None)

    TEMP_BUTTON.pop(user_id, None)


def clear_admin_states(user_id):

    WAITING_BROADCAST.pop(user_id, None)

    WAITING_BAN_USER.pop(user_id, None)

    WAITING_UNBAN_USER.pop(user_id, None)

    WAITING_DELETE_TASK.pop(user_id, None)


def clear_all_states(user_id):

    clear_task_states(user_id)

    clear_caption_states(user_id)

    clear_button_states(user_id)

    clear_admin_states(user_id)
