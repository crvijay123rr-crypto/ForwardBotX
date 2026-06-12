from database.mongo import tasks
from datetime import datetime
import uuid

async def create_task(user_id):

task_id = str(uuid.uuid4())

data = {

    "task_id": task_id,

    "user_id": user_id,

    "source_chat_id": None,
    "source_chat_username": None,

    "first_link": None,
    "last_link": None,

    "destination_id": None,
    "destination_title": None,
    "destination_username": None,

    "rename_mode": "keep",

    "status": "waiting",

    "total": 0,
    "forwarded": 0,
    "remaining": 0,

    "topics_found": 0,

    "duplicate": 0,
    "deleted": 0,
    "skipped": 0,
    "filtered": 0,

    "percentage": 0,

    "created_at": datetime.utcnow()
}

await tasks.insert_one(data)

return task_id

async def get_task(task_id):

return await tasks.find_one(
    {
        "task_id": task_id
    }
)

async def get_user_tasks(user_id):

return tasks.find(
    {
        "user_id": user_id
    }
)

async def update_task(
task_id,
key,
value
):

await tasks.update_one(
    {
        "task_id": task_id
    },
    {
        "$set": {
            key: value
        }
    }
)

async def update_many(
task_id,
data
):

await tasks.update_one(
    {
        "task_id": task_id
    },
    {
        "$set": data
    }
)

async def set_status(
task_id,
status
):

await tasks.update_one(
    {
        "task_id": task_id
    },
    {
        "$set": {
            "status": status
        }
    }
)

async def delete_task(task_id):

await tasks.delete_one(
    {
        "task_id": task_id
    }
)

async def task_exists(task_id):

task = await tasks.find_one(
    {
        "task_id": task_id
    }
)

return bool(task)

async def increase_forwarded(task_id):

await tasks.update_one(
    {
        "task_id": task_id
    },
    {
        "$inc": {
            "forwarded": 1
        }
    }
)

async def increase_skipped(task_id):

await tasks.update_one(
    {
        "task_id": task_id
    },
    {
        "$inc": {
            "skipped": 1
        }
    }
)

async def increase_deleted(task_id):

await tasks.update_one(
    {
        "task_id": task_id
    },
    {
        "$inc": {
            "deleted": 1
        }
    }
)

async def increase_duplicate(task_id):

await tasks.update_one(
    {
        "task_id": task_id
    },
    {
        "$inc": {
            "duplicate": 1
        }
    }
)

async def increase_filtered(task_id):

await tasks.update_one(
    {
        "task_id": task_id
    },
    {
        "$inc": {
            "filtered": 1
        }
    }
)

async def total_tasks():

return await tasks.count_documents(
    {}
)
