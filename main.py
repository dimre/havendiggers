"""Main module"""
import logging
import os
from telegram import BotCommand
from telegram.ext import CommandHandler, Dispatcher, Updater

from modules.commands import help_cmd, start_cmd, list_cmd, count_cmd
from modules.data import config_map
from modules.jobs import update_following

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def add_commands(up: Updater):
    """Adds the list of commands with their description to the bot

    Args:
        up (Updater): supplyed Updater
    """
    commands = [
        BotCommand("start", "starts the bot"),
        BotCommand("help ", "help message and list of commands"),
        BotCommand("list ", "shows who the specified user is following"),
        BotCommand("count ", "shows how many users each user follows"),
    ]
    up.bot.set_my_commands(commands=commands)


def add_handlers(dp: Dispatcher):
    """Adds all the needed handlers to the dispatcher

    Args:
        dp (Dispatcher): supplyed dispatcher
    """
    # Error handler
    #dp.add_error_handler(error_handler)

    # Command handlers
    dp.add_handler(CommandHandler("start", start_cmd))
    dp.add_handler(CommandHandler("help", help_cmd))
    dp.add_handler(CommandHandler("list", list_cmd))
    dp.add_handler(CommandHandler("count", count_cmd))


def add_jobs(dp: Dispatcher):
    """Adds all the jobs to be scheduled to the dispatcher

    Args:
        dp (Dispatcher): supplyed dispatcher
    """
    dp.job_queue.run_repeating(update_following, interval=config_map['loop_time'], first=10)


def main():
    """Main function
    """
    updater = Updater(config_map['telegram_token'],
                      request_kwargs={
                          'read_timeout': 20,
                          'connect_timeout': 20
                      },
                      use_context=True)
    add_commands(updater)
    add_handlers(updater.dispatcher)
    add_jobs(updater.dispatcher)

    if os.getenv("WEBHOOK_URL", None):
        PORT = int(os.getenv('PORT', '8443'))
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=config_map['telegram_token'],
                              webhook_url=os.getenv("WEBHOOK_URL") + config_map['telegram_token'])
    else:
        updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
