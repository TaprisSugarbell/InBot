import asyncio
import logging
import queue
import os

import pyrogram

from InBot.helper.logger_configs.logger_config import log_file
from InBot.helper.mongo_connect import Mongo, confirm
from InBot.__vars__ import LOG_CHANNEL, BOT_NAME, BOT_TOKEN, API_ID, API_HASH, human_hour_readable
from InBot.helper.utils import create_folder
from InBot.strings import get_string


logger = logging.getLogger(__name__)
sayulogs = logging.getLogger(BOT_NAME)
PACKAGE = __package__


def logging_stream_info(msg):
    __logger_level = logger.level
    logger.setLevel("INFO")
    logger.info(msg)
    logger.setLevel(__logger_level)


# Client
plugins = dict(root=f"{BOT_NAME}/plugins")
app = pyrogram.Client(BOT_NAME, bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH, plugins=plugins)


async def auth_users():
    _u = Mongo(database=BOT_NAME, collection="users")
    _c = await confirm(_u, {})
    return [i["user_id"] for i in _c] if _c else []


async def logs_channel_update(message: str = None, _mode: str = "send_message", _app=None, *args, **kwargs):
    if message is None:
        message = get_string("log_channel").format(bot_name=BOT_NAME, date=human_hour_readable())

    _app = _app or app
    _snd_Txt = ["send_message", "edit_message_text"]
    if LOG_CHANNEL:
        t__ = {"text": message} if _mode in _snd_Txt else {_mode.split("_")[-1]: message}
        kwargs |= t__
        await getattr(_app, _mode)(LOG_CHANNEL, *args, **kwargs)
        if os.path.exists(message) and message != log_file:
            os.remove(message)
    else:
        try:
            print(message)
        except Exception as e:
            print(e)
        # logger.info(message)


# queue_ = asyncio.PriorityQueue()
queue_ = queue.PriorityQueue()

