"""update_following job"""
import logging
from telegram import Bot
from telegram.ext import CallbackContext
import twitter
from modules.data import config_map, DbManager
from modules.utils import EventInfo, notify_user

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def update_following(ctx: CallbackContext):
    """Updates the followed_users table, if any have changed

    Args:
        ctx (:class:`CallbackContext`): context passed by the handler
    """
    info = EventInfo.from_job(ctx)
    api = twitter.Api(consumer_key=config_map['twitter_api_key'],
                      consumer_secret=config_map['twitter_api_key_secret'],
                      access_token_key=config_map['twitter_access_token'],
                      access_token_secret=config_map['twitter_access_token_secret'],
                      sleep_on_rate_limit=True)

    for user in config_map['twitter_user_list']:
        logger.info("Finding following of %s", user)

        old_following = DbManager.select_from(select="followed_id, followed_name",
                                              table_name="followed_users",
                                              where="follower_name = %s",
                                              where_args=(user,))
        if len(old_following) == 0:
            get_friends(api, user)
        else:
            old_following = set(map(lambda row: row['followed_id'], old_following))
            current_following = set(api.GetFriendIDs(screen_name=user))

            get_new_friends(api, info.bot, old_following, current_following, user)
            get_removed_friends(info.bot, old_following, current_following, user)


def get_friends(api: twitter.Api, user: str):
    """Get following users

    Args:
        api: twitter api
        user: user to check the following of
    """
    new_following = set(
        map(lambda user: twitter.User(id=user.id, screen_name=user.screen_name), api.GetFriends(screen_name=user)))
    if len(new_following) > 0:
        logger.info("Inserting new following of %s", user)
        new_following_values = tuple(map(lambda e: (user, e.id, e.screen_name), new_following))
        DbManager.insert_into(table_name="followed_users",
                              columns=("follower_name", "followed_id", "followed_name"),
                              values=new_following_values,
                              multiple_rows=True)


def get_new_friends(api: twitter.Api, bot: Bot, old_following: list, current_following: set, user: str):
    """Get following ids

    Args:
        api: twitter api
        bot: telegram bot
        old_following: the following already in memory
        user: user to check the following of
    """
    new_following = tuple(current_following.difference(old_following))
    if len(new_following) > 0:
        logger.info("Updating following of %s", user)
        new_following_users = []
        for new_following_istance in (new_following[x:x + 100] for x in range(0, len(new_following), 100)):
            new_following_users += api.UsersLookup(user_id=new_following_istance)
        new_following_values = tuple(map(lambda e: (user, e.id, e.screen_name), new_following_users))
        DbManager.insert_into(table_name="followed_users",
                              columns=("follower_name", "followed_id", "followed_name"),
                              values=new_following_values,
                              multiple_rows=True)
        notify_user(bot=bot,
                    follower_name=user,
                    new_following=new_following_users,
                    start_message=f"started following {len(new_following)} new users")


def get_removed_friends(bot: Bot, old_following: set, current_following: set, user: str):
    """Get following ids

    Args:
        api: twitter api
        bot: telegram bot
        old_following: the following already in memory
        user: user to check the following of
    """
    removed_following = tuple(old_following.difference(current_following))
    if len(removed_following) > 0:
        logger.info("Removing following of %s", user)
        where = f"followed_id IN ({', '.join(['%s' for _ in removed_following])})"
        removed_following_values = DbManager.select_from(select="DISTINCT followed_id, followed_name",
                                                         table_name="followed_users",
                                                         where=where,
                                                         where_args=removed_following)

        removed_following_users = tuple(
            map(lambda user: twitter.User(id=user['followed_id'], screen_name=user['followed_name']),
                removed_following_values))
        DbManager.delete_from(table_name="followed_users", where=where, where_args=removed_following)
        notify_user(bot=bot,
                    follower_name=user,
                    new_following=removed_following_users,
                    start_message=f"stopped following {len(removed_following)} users")
