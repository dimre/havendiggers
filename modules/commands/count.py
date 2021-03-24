"""/count command"""
from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from modules.utils import EventInfo, get_name_with_link
from modules.data import DbManager, config_map


def count_cmd(update: Update, context: CallbackContext):
    """Handles the /count command.
    Shows how many users each user follows

    Args:
        update (Update): update event
        context (CallbackContext): context passed by the handler
    """
    info = EventInfo.from_message(update, context)
    if info is None:
        return

    text = []
    for user in config_map['twitter_user_list']:
        n_following = DbManager.count_from(table_name="followed_users", where="follower_name = %s", where_args=(user,))
        text.append(f"*{get_name_with_link(user)} follows {n_following} users*")
    text = "\n".join(text) if text else "No user found in the settings file"
    info.bot.send_message(chat_id=info.chat_id, text=text, parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)
