from telegram import InlineQueryResultArticle, InputTextMessageContent
from uuid import uuid4


def inline_query_transform(response_text: str, title=None) -> list:
    """
    Formats a response string into a form which can be passed
    to inline_query.answer(). If the title isn't passed, will
    just use the response text as the title, too.
    """

    return [
        InlineQueryResultArticle(
            id=uuid4(),
            title=title if title else response_text,
            input_message_content=InputTextMessageContent(response_text)
        )
    ]


def get_meta_from_update(update) -> tuple:
    """Returns username, user_id (str), and the message text from an update."""

    query_username = (
        update.effective_user.username if update.effective_user
        else ''
    )
    query_user_id = (
        str(update.effective_user.id) if update.effective_user
        else ''
    )
    query_text = (
        update.inline_query.query if update.inline_query
        else update.message.text
    )

    return query_username, query_user_id, query_text
