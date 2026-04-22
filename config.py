import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    OWNER_ID = int(os.getenv("OWNER_ID", 0))
    MONGO_URI = os.getenv("MONGO_URI")
    
    # Force Subscribe IDs (Must be integers)
    FS_CHANNEL = int(os.getenv("FORCE_SUB_CHANNEL", 0))
    FS_GROUP = int(os.getenv("FORCE_SUB_GROUP", 0))
    
    # Custom Banner
    START_IMG = "https://files.catbox.moe/13nyhx.jpg"
    
    DEFAULT_EMOJIS = ['❤️', '🔥', '💫', '👍', '😂', '🎉', '💯', '⚡']
