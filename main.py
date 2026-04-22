import logging
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ChatMemberHandler, CallbackQueryHandler, filters
from config import Config
import handlers

logging.basicConfig(level=logging.INFO)

def main():
    if not Config.BOT_TOKEN:
        return

    app = ApplicationBuilder().token(Config.BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", handlers.start))
    app.add_handler(CommandHandler("broadcast", handlers.broadcast))
    app.add_handler(CallbackQueryHandler(handlers.help_callback, pattern="help_menu"))
    app.add_handler(ChatMemberHandler(handlers.chat_member_update, ChatMemberHandler.MY_CHAT_MEMBER))
    
    app.add_handler(MessageHandler(
        filters.TEXT & (~filters.COMMAND) & filters.ChatType.GROUPS, 
        handlers.auto_react_handler
    ))

    print("Bot is alive and compatible with Python 3.12+!")
    app.run_polling()

if __name__ == "__main__":
    main()
