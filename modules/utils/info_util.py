"""Common info needed in both command and callback handlers"""
from telegram import Bot, Update, Message, CallbackQuery
from telegram.ext import CallbackContext
from modules.data import config_map


class EventInfo():
    """Class that contains all the relevant information related to an event
    """

    def __init__(self,
                 bot: Bot,
                 ctx: CallbackContext,
                 update: Update = None,
                 message: Message = None,
                 query: CallbackQuery = None):
        self.__bot = bot
        self.__ctx = ctx
        self.__update = update
        self.__message = message
        self.__query = query

    @property
    def bot(self) -> Bot:
        """:class:`telegram.Bot`: Istance of the telegram bot"""
        return self.__bot

    @property
    def context(self) -> CallbackContext:
        """:class:`telegram.ext.CallbackContext`: Context generated by some event"""
        return self.__ctx

    @property
    def update(self) -> Update:
        """:class:`telegram.update.Update`: Update generated by some event. Defaults to None"""
        return self.__update

    @property
    def message(self) -> Message:
        """:class:`telegram.Message`: Message that caused the update. Defaults to None"""
        return self.__message

    @property
    def args(self) -> list:
        """:class:`list`: List of args passed to the context"""
        return self.__ctx.args

    @property
    def chat_id(self) -> int:
        """:class:`int`: Id of the chat where the event happened. Defaults to None"""
        if self.__message is None:
            return None
        return self.__message.chat_id

    @property
    def text(self) -> str:
        """:class:`str`: Text of the message that caused the update. Defaults to None"""
        if self.__message is None:
            return None
        return self.__message.text

    @property
    def message_id(self) -> int:
        """:class:`int`: Id of the message that caused the update. Defaults to None"""
        if self.__message is None:
            return None
        return self.__message.message_id

    @property
    def user_id(self) -> int:
        """:class:`int`: Id of the user that caused the update. Defaults to None"""
        if self.__query is not None:
            return self.__query.from_user.id
        if self.__message is not None:
            return self.__message.from_user.id
        return None

    @classmethod
    def from_message(cls, update: Update, ctx: CallbackContext):
        """Istance of EventInfo created by a message update

        Args:
            update (Update): update event
            context (CallbackContext): context passed by the handler

        Returns:
            EventInfo: istance of the class
        """
        if update.message.chat_id not in config_map['telegram_user_list']:
            return None
        return cls(bot=ctx.bot, ctx=ctx, update=update, message=update.message)

    @classmethod
    def from_job(cls, ctx: CallbackContext):
        """Istance of EventInfo created by a job update

        Args:
            context (CallbackContext): context passed by the handler

        Returns:
            EventInfo: istance of the class
        """
        return cls(bot=ctx.bot, ctx=ctx)
