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
        "well as track steps along your way.\n\n"
        
        "Start typin' the first step on your journey to get started."
    )

    username, user_id, message_text = get_meta_from_update(update)

    bot.send_chat_action(user_id, ChatAction.TYPING)
    bot.sendMessage(
        chat_id=user_id, parse_mode=ParseMode.MARKDOWN,
        text=WELCOME_MESSAGE_TEXT
    )


def next_step(bot, update):
    """TODO"""

    NEXT_STEP_MESSAGE = (
        "Cool. Keep typin' in more steps (one per message) to keep "
        "addin' to the list, or send `/done` if you're done."
    )

    username, user_id, message_text = get_meta_from_update(update)

    bot.send_chat_action(user_id, ChatAction.TYPING)
    bot.sendMessage(
        chat_id=user_id, parse_mode=ParseMode.MARKDOWN,
        text=NEXT_STEP_MESSAGE
    )


def ask_for_eta(bot, update):
    """TODO"""

    ASK_ETA_MESSAGE = (
        "Cool. When do you think you'll be done?"
    )

    username, user_id, message_text = get_meta_from_update(update)

    bot.send_chat_action(user_id, ChatAction.TYPING)
    bot.sendMessage(
        chat_id=user_id, parse_mode=ParseMode.MARKDOWN,
        text=ASK_ETA_MESSAGE
    )

def confirm_start(bot, update):
    """TODO"""

    username, user_id, message_text = get_meta_from_update(update)

    CONFIRM_MESSAGE = (
        "Nice! Your progress has begun bein' tracked. Others can "
        f"follow it by typing in `@underway_bot {username}`.\n\n"

        "Here's what it looks like right now:\n\n"

        f"TODO_FUNC_CALL\n\n"

        "To move forward a step, send me `/step`. To move backwards, `/unstep`."
    )

    bot.send_chat_action(user_id, ChatAction.TYPING)
    bot.sendMessage(
        chat_id=user_id, parse_mode=ParseMode.MARKDOWN,
        text=CONFIRM_MESSAGE
    )

@log_command
def on_command_help(bot, update):
    """
    Provides the user with information about the bot.
    """

    HELP_COMMAND_TEXT = (
        "/start -- Creates a new series of steps to track!\n"
    )

    username, user_id, message_text = get_meta_from_update(update)

    bot.send_chat_action(user_id, ChatAction.TYPING)
    bot.sendMessage(
        chat_id=user_id, parse_mode=ParseMode.MARKDOWN,
        text=HELP_COMMAND_TEXT
    )

# TODO
from jinja2 import Environment, FileSystemLoader
from os import getcwd
from os.path import join
@log_command
def on_command_debug(bot, update):
    username, user_id, message_text = get_meta_from_update(update)
    env = Environment(loader=FileSystemLoader(join(getcwd(), 'templates')))
    bot.send_chat_action(user_id, ChatAction.TYPING)

    bot.sendMessage(
        chat_id=user_id, parse_mode=ParseMode.MARKDOWN,
        text=env.get_template('response_template.j2').render({
            'username': 'Jinhai',
            'status': 'is *in transit*',
            'time_notes': 'ETA 11:30 PM PT',
            'completion_percent': 75,
            'steps': [
                {'completed': True, 'description': 'Gym stuff'},
                {'completed': True, 'description': 'I gotta do a quick shower, and also test how this thing handles really long lines!'},
                {'completed': True, 'description': 'Gonna MAKE SOME FISH. Gonna add BONITO FLAKES AND CAROT ✨'},
                {'completed': False, 'description': 'Gonna do 2.5 relaxes.'},
            ]
        })
    )
