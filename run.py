from logger import log
from config import API_KEY
from handlers import (
    on_command_start, on_command_help, on_message_text, on_inline_query
)
from telegram.ext import (
    Updater, InlineQueryHandler, MessageHandler, CommandHandler, Filters
)


def start():
    """Connects to Telegram and starts the bot."""

    bot = Updater(token=API_KEY)
    dp = bot.dispatcher

    # Register inline_query handler
    dp.add_handler(InlineQueryHandler(on_inline_query))

    # Register command handlers
    dp.add_handler(CommandHandler("start", on_command_start))
    dp.add_handler(CommandHandler("help", on_command_help))

    # Register text message handler
    dp.add_handler(MessageHandler(Filters.text, on_message_text))

    log.info("Bot ready, dood! Connected as {username} (with ID {id}).".format(
        username=bot.bot.username,
        id=bot.bot.id
    ))
    bot.start_polling()
    bot.idle()


def _onboard_config():
    global API_KEY

    with open('config.py', 'r') as f:
        config_contents = f.read()

    print("Hiya. Looks like you're startin' underway_bot for the first time.")
    bot_token = input("What's your bot token? ")

    with open('config.py', 'w') as f:
        f.write(config_contents.format(api_key=bot_token))

    API_KEY = bot_token
    print("Done!")


if __name__ == '__main__':
    if API_KEY == '{api_key}':
        _onboard_config()
    start()
