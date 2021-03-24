"""/list <name> ... command"""
from telegram import Update
from telegram.ext import CallbackContext
import twitter
from modules.utils import EventInfo, notify_user
from modules.data import DbManager


def list_cmd(update: Update, context: CallbackContext):
    """Handles the /list <name> command.
    Sends a list of users the one requested is currently following

    Args:
        update (Update): update event
        context (CallbackContext): context passed by the handler
    """
    info = EventInfo.from_message(update, context)
    if info is None:
        return
    if info.args is None or len(info.args) == 0:
        info.bot.send_message(chat_id=info.chat_id, text="use: /list <user_name> ...")
        return

    for user in info.args:
        following = DbManager.select_from(select="followed_id, followed_name",
                                          table_name="followed_users",
                                          where="follower_name = %s",
                                          where_args=(user,))
        following = set(map(lambda row: twitter.User(id=row['followed_id'], screen_name=row['followed_name']), following))
        notify_user(bot=info.bot,
                    follower_name=user,
                    new_following=following,
                    user_id_list=[info.chat_id],
                    start_message=f"follows {len(following)} users")
