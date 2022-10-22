import time
import pyrogram.errors
from .. import sayulogs
from pyrogram import Client, filters
from danbooru import Danbooru, arm_links, arm_link


@Client.on_message(filters.command(["sfw"]))
async def __sfw__(bot, update):
    print(update)
    chat_id = update.chat.id
    data = "".join(update.text.split()[-1])
    dbr = Danbooru(host="safebooru")
    try:
        post_id = int(data)
        search = dbr.post(post_id)
        _lnk = arm_link(search)
        try:
            await bot.send_photo(chat_id,
                                 _lnk)
        except pyrogram.errors.MediaEmpty:
            _lnk = arm_link(search,
                            _type="large_file_url")
            await bot.send_photo(chat_id,
                                 _lnk)
    except ValueError:
        search = dbr.post_random()
        _lnk = arm_link(search)
        try:
            await bot.send_photo(chat_id,
                                 _lnk)
        except pyrogram.errors.MediaEmpty:
            _lnk = arm_link(search,
                            _type="large_file_url")
            await bot.send_photo(chat_id,
                                 _lnk)

