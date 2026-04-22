from telegram import Update
from telegram.constants import ChatMemberStatus
from config import Config

async def is_subscribed(bot, user_id):
    if user_id == Config.OWNER_ID: return True
    try:
        for chat_id in [Config.FS_CHANNEL, Config.FS_GROUP]:
            member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
            if member.status in [ChatMemberStatus.LEFT, ChatMemberStatus.BANNED]:
                return False
        return True
    except: return False

async def is_group_admin(update: Update):
    if update.effective_user.id == Config.OWNER_ID: return True
    member = await update.effective_chat.get_member(update.effective_user.id)
    return member.status in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]
