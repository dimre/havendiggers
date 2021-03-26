"""/start command"""
from telegram import Update
from telegram.ext import CallbackContext
from modules.utils import EventInfo
from modules.data import DbManager


def remove_cmd(update: Update, context: CallbackContext):
    """Handles the /remove command.
    Removes all records of the specified user from the database

    Args:
        update (Update): update event
        context (CallbackContext): context passed by the handler
    """
    info = EventInfo.from_message(update, context)
    if info is None:
        return
    if info.args is None or len(info.args) == 0:
        info.bot.send_message(chat_id=info.chat_id, text="use: /remove <user_name> ...")
        return
    for arg in info.args:
        n_delete = DbManager.count_from(table_name="followed_users", where="follower_name = %s", where_args=(arg,))
        DbManager.delete_from(table_name="followed_users", where="follower_name = %s", where_args=(arg,))
        info.bot.send_message(chat_id=info.chat_id, text=f"{n_delete} rows have been deleted from the database")
