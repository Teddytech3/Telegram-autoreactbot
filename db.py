from motor.motor_asyncio import AsyncIOMotorClient
from config import Config
from datetime import datetime

client = AsyncIOMotorClient(Config.MONGO_URI)
db = client.react_bot

groups_col = db.groups
users_col = db.users
settings_col = db.settings

async def add_user(user_id, username, name):
    await users_col.update_one(
        {"user_id": user_id},
        {"$set": {"username": username, "name": name, "last_seen": datetime.now()}},
        upsert=True
    )

async def add_group(chat_id, title, added_by):
    await groups_col.update_one(
        {"chat_id": chat_id},
        {"$set": {
            "title": title, 
            "added_by": added_by, 
            "autoreact": True,
            "is_admin": True,
            "date_added": datetime.now()
        }},
        upsert=True
    )

async def get_setting(key, default):
    res = await settings_col.find_one({"key": key})
    return res["value"] if res else default
