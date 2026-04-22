import random
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from telegram.error import RetryAfter as FloodWait 
from config import Config
import db
import utils

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await db.add_user(user.id, user.username, user.first_name)
    
    g_count = await db.groups_col.count_documents({})
    u_count = await db.users_col.count_documents({})
    
    # 'rf' denotes raw f-string to handle MarkdownV2 escapes correctly
    text = (
        rf"✨ *Welcome to ReactionMaster Pro, {user.first_name}\!* ✨" + "\n\n"
        rf"🚀 *The most powerful auto\-reaction bot for groups\.*" + "\n\n"
        rf"📊 *Global Statistics*" + "\n"
        rf"┣ 👤 `Users:` *{u_count}*" + "\n"
        rf"┗ 🏠 `Groups:` *{g_count}*" + "\n\n"
        rf"🛠 *Core Features*" + "\n"
        rf"• Auto\-React to Group Messages" + "\n"
        rf"• Advanced Broadcast System" + "\n"
        rf"• Force Subscription Guard"
    )

    keyboard = [
        [InlineKeyboardButton("➕ Add Me to Your Group", url=f"https://t.me/{context.bot.username}?startgroup=true")],
        [
            InlineKeyboardButton("📢 Channel", url="https://t.me/free_net_zone1"),
            InlineKeyboardButton("💬 Support", url="https://t.me/free_net_zone2")
        ],
        [InlineKeyboardButton("📜 Help & Commands", callback_data="help_menu")]
    ]
    
    await update.message.reply_photo(
        photo=Config.START_IMG,
        caption=text,
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def help_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    help_text = (
        rf"📖 *Command Manual*" + "\n\n"
        rf"🔹 `/autoreact on|off` \- Toggle reactions" + "\n"
        rf"🔹 `/setemoji <emojis>` \- Set custom set" + "\n"
        rf"🔹 `/id` \- Get Chat/User ID" + "\n"
        rf"🔹 `/broadcast` \- Global alert \(Owner\)" + "\n\n"
        rf"💡 _Note: Only group admins can toggle settings\._"
    )
    await query.edit_message_caption(caption=help_text, parse_mode=ParseMode.MARKDOWN_V2)

async def auto_react_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_chat or update.effective_chat.type == "private": return
    
    group = await db.groups_col.find_one({"chat_id": update.effective_chat.id})
    if not group or not group.get("autoreact", True): return

    emojis = await db.get_setting("custom_emojis", Config.DEFAULT_EMOJIS)
    try:
        await update.message.set_reaction(reaction=random.choice(emojis))
    except: pass

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != Config.OWNER_ID: return
    
    groups = db.groups_col.find({"is_admin": True})
    success, failed = 0, 0
    msg = update.message.reply_to_message if update.message.reply_to_message else update.message
    
    status_msg = await update.message.reply_text(rf"🚀 *Broadcasting\.\.\.*", parse_mode=ParseMode.MARKDOWN_V2)

    async for g in groups:
        try:
            await msg.copy(chat_id=g['chat_id'])
            success += 1
            await asyncio.sleep(1.5)
        except FloodWait as e:
            await asyncio.sleep(e.retry_after)
        except:
            failed += 1

    await status_msg.edit_text(rf"✅ *Sent:* `{success}`\n❌ *Failed:* `{failed}`", parse_mode=ParseMode.MARKDOWN_V2)

async def chat_member_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = update.my_chat_member
    if result.new_chat_member.status in ["administrator", "member"]:
        if not await utils.is_subscribed(context.bot, result.from_user.id):
            try:
                await context.bot.send_message(
                    result.from_user.id, 
                    rf"⚠️ *Access Denied*\n\nYou must join our Channel and Group to add me to new chats\!",
                    parse_mode=ParseMode.MARKDOWN_V2
                )
            except: pass
            await result.chat.leave()
            return
        await db.add_group(result.chat.id, result.chat.title, result.from_user.id)
