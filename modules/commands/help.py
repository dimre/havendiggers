"""/help command"""
from telegram import Update, ParseMode
from telegram.ext import CallbackContext
from modules.utils import EventInfo
from modules.data import read_md


def help_cmd(update: Update, context: CallbackContext):
    """Handles the /help command.
    Sends an help message

    Args:
        update (Update): update event
        context (CallbackContext): context passed by the handler
    """
    info = EventInfo.from_message(update, context)
    if info is None:
        return
    text = read_md("help")
    info.bot.send_message(chat_id=info.chat_id, text=text, parse_mode=ParseMode.MARKDOWN_V2)
