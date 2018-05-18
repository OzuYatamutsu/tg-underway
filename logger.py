from helpers import get_meta_from_update
from logging import getLogger, StreamHandler, FileHandler, DEBUG
from sys import stdout


def log_cateify(func):
    """
    A decorator that logs important cateification info (i.e.
    when we're calling into the response controller).
    """

    def _log_wrapper(bot, update):
        username, user_id, query = get_meta_from_update(update)

        log.debug('Cateifying: "{text}" from user {username} ({id})'.format(
            text=query, username=username, id=user_id
        ))

        return func(bot, update)
    return _log_wrapper


def log_command(func):
    """
    A decorator that logs important COMMANDification info (i.e.
    when /commands are used).
    """

    def _log_wrapper(bot, update):
        username, user_id, command = get_meta_from_update(update)

        log.debug('Command: "{command}" from user {username} ({id})'.format(
            command=command, username=username, id=user_id
        ))

        return func(bot, update)
    return _log_wrapper


log = getLogger(__name__)
log.setLevel(DEBUG)
log.addHandler(StreamHandler(stdout))
log.addHandler(FileHandler('cateify_bot.log'))
