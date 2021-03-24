"""Utilities for sending messages"""
from telegram import Bot, ParseMode
from telegram.error import Unauthorized, BadRequest
from telegram.utils.helpers import escape_markdown
from modules.data import config_map


def notify_user(bot: Bot,
                follower_name: str,
                new_following: set,
                user_id_list: list = config_map['telegram_user_list'],
                start_message: str = "ha iniziato a seguire i seguenti account"):
    """Notifies the telegram users (or chats)

    Args:
        ctx: context passed by the handler
        follower_name: name of the user that started following someone
        new_following: set of new user the follower user started following
        user_id_list: list of users to notify on telegram. Defaults to config_map['telegram_user_list']
        start_message: message to put on the starting line. Defaults to "ha iniziato a seguire i seguenti account"
    """
    if len(new_following) == 0:
        text = f"*{get_name_with_link(follower_name)} non ha following nel database*"
    else:
        text = f"*{get_name_with_link(follower_name)} {start_message}:*\n\n"
        new_following_text = "\n".join((get_name_with_link(followed.screen_name) for followed in new_following))
        text += new_following_text

    for user_id in user_id_list:
        try:
            send_message(bot=bot, chat_id=user_id, text=text)
        except (Unauthorized, BadRequest):
            pass


def send_message(bot: Bot, chat_id: int, text: str):
    """Replies with a message, making sure the maximum lenght text allowed is respected

    Args:
        bot: telegram bot
        chat_id: id of the chat to send the message to
        text: text to send
    """
    msg = ""
    righe = text.split('\n')
    for riga in righe:
        if len(msg) > 3500:
            bot.send_message(chat_id=chat_id, text=msg, parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)
            msg = ""
        else:
            msg += f"{riga}\n"
    bot.send_message(chat_id=chat_id, text=msg, parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)


def get_name_with_link(name: str) -> str:
    """Applies the following function: name -> [@{name}](https://twitter.com/{name})

    Args:
        name (:class:`str`): user_name

    Returns:
        :class:`str`: name and link in markdown format
    """
    return f"[@{escape_markdown(name)}](https://twitter.com/{name})"
