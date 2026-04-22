import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    OWNER_ID = int(os.getenv("OWNER_ID", 0))
    MONGO_URI = os.getenv("MONGO_URI")
    
    # Force Subscribe IDs (Should be integers starting with -100)
    FS_CHANNEL = int(os.getenv("FORCE_SUB_CHANNEL", 0))
    FS_GROUP = int(os.getenv("FORCE_SUB_GROUP", 0))
    
    DEFAULT_EMOJIS = ['❤️', '🔥', '💫', '👍', '😂', '🎉', '💯', '⚡']
