from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from telegram import ParseMode

import config.connector as connector


def start(update, _context):
    user_name = update.message.from_user.name
    bot_id = _context.bot.id
    update.message.reply_text(text=f"Привет!\nБот успешно запущен. ID: {bot_id}", parse_mode=ParseMode.HTML)


def main():
    """Start the bot."""
    updater = Updater(connector.TOKEN, request_kwargs=connector.BOT_REQUEST_KWARGS, use_context=True)

    dp = updater.dispatcher

    # service
    dp.add_handler(CommandHandler("start", start))

    updater.start_polling(bootstrap_retries=5)
    updater.idle()


if __name__ == "__main__":
    main()
