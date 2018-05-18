from logger import log_cateify, log_command
from helpers import inline_query_transform, get_meta_from_update
from response_controller import generate_inline_response
from telegram import ParseMode, ChatAction


@log_cateify
def on_inline_query(bot, update) -> None:
    """
    Forward the query to the controller method and respond
    """

    username, user_id, query_text = get_meta_from_update(update)

    if not query_text:
        update.inline_query.answer(inline_query_transform(''))
        return

    update.inline_query.answer(inline_query_transform(
        generate_inline_response(query_text=query_text)
    ))


@log_cateify
def on_message_text(bot, update) -> None:
    """
    Forward the message text to the controller method and respond
    """

    username, user_id, message_text = get_meta_from_update(update)

    if not message_text:
        return

    bot.send_chat_action(user_id, ChatAction.TYPING)

    bot.sendMessage(
        chat_id=user_id,
        parse_mode=ParseMode.MARKDOWN,
        text=generate_inline_response(query_text=message_text)
    )


@log_command
def on_command_start(bot, update):
    """Welcome message handler for /start"""

    WELCOME_MESSAGE_TEXT = (
        "Yo! My name is **UnderwayBot.** I can help you send ETAs "
        "to your friends to tell 'em __when you'll be ready,__ as "
        "well as track steps along your way."
    )

    username, user_id, message_text = get_meta_from_update(update)

    bot.send_chat_action(user_id, ChatAction.TYPING)
    bot.sendMessage(
        chat_id=user_id, parse_mode=ParseMode.MARKDOWN,
        text=WELCOME_MESSAGE_TEXT
    )


@log_command
def on_command_help(bot, update):
    """
    Provides the user with information about the bot.
    """

    HELP_COMMAND_TEXT = (
        "TODO IMPLEMENT"
    )

    username, user_id, message_text = get_meta_from_update(update)

    bot.send_chat_action(user_id, ChatAction.TYPING)
    bot.sendMessage(
        chat_id=user_id, parse_mode=ParseMode.MARKDOWN,
        text=HELP_COMMAND_TEXT
    )
