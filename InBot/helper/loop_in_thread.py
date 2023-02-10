import asyncio
import logging
import time

from danbooru import Danbooru, arm_link
from pyrogram.types import (InputMediaPhoto, InputMediaAnimation, InputMediaVideo)
from InBot import queue_
from InBot.helper.mongo_connect import *
from ..helper.__inline_butns__ import *

logger = logging.getLogger(__name__)
tc = Mongo(URI, "DanbooruBot", "tag_code")
db = Mongo(URI, "DanbooruBot", "user_settings")


def run_asyncio(obj, *args, **kwargs):
    asyncio.run(obj(*args, **kwargs))


async def read_and_execute(app):
    while True:
        # pass
        _start = time.perf_counter()
        # __tags = ""
        # show_seq = ["prev", "next"]
        # if not queue_.empty():
        #     __item_g = queue_.get()
        #     __item = __item_g[1]
        #     print(__item_g)
        #     print(__item)
        #     user_id = __item["user_id"]
        #     inline_message_id = __item["inline_message_id"]
        #     _mode = __item["mode"]
        #     seq = __item["seq"]
        #     _tags_code = __item["tag_code"]
        #     post_id = __item["post_id"]
        #     _c_ = await confirm(db, {"user_id": user_id})
        #     if _c_:
        #         user_settings = _c_[0]
        #         _username = user_settings["username"]
        #         _api_key = user_settings["api_key"]
        #         _password = user_settings["password"]
        #         _host = user_settings["host"]
        #         dbr = Danbooru(_username, _api_key, _password, host=_host)
        #     else:
        #         _host = "safebooru"
        #         dbr = Danbooru(host=_host)
        #         await add_(db, {"user_id": user_id,
        #                         "username": None,
        #                         "api_key": None,
        #                         "password": None,
        #                         "host": _host})
        #     _c = await confirm(
        #         tc,
        #         {
        #             "tags_code": _tags_code
        #         }
        #     )
        #     if _c:
        #         _c = _c[0]
        #         __tags = _c["tags"]
        #         if __tags == "order:rank":
        #             __tags = ""
        #     # https://danbooru.donmai.us/posts/5406792/show_seq?q=underwear&seq=prev
        #     xsa = lambda x, y: getattr(x, y)
        #     if seq in show_seq:
        #         _srch = dbr.searchs()
        #         info = dbr.show_seq(int(post_id), q=__tags, seq=seq)
        #         _has_parent = True if info.parent_id or info.has_children else False
        #         Pbtns = post_buttons(
        #             info.id,
        #             _mode,
        #             _tags_code,
        #             _has_parent
        #         )
        #         _ext = info.file_ext
        #         match _ext:
        #             case "gif":
        #                 _mode_input_use = InputMediaAnimation
        #             case "mp4" | "mkv" | "webm":
        #                 _mode_input_use = InputMediaVideo
        #             case _:
        #                 _mode_input_use = InputMediaPhoto
        #         try:
        #             lnk = arm_link(info, "large_file_url", ())
        #             await app.edit_inline_media(inline_message_id,
        #                                         media=_mode_input_use(lnk[1], ""))
        #             await app.edit_inline_reply_markup(
        #                 inline_message_id,
        #                 reply_markup=Pbtns
        #             )
        #         except Exception as e:
        #             lnk = arm_link(info, abso=())
        #             await app.edit_inline_media(inline_message_id,
        #                                         media=_mode_input_use(lnk[1], ""))
        #             await app.edit_inline_reply_markup(
        #                 inline_message_id,
        #                 reply_markup=Pbtns
        #             )
        #     elif seq == "file":
        #         # _srch = dbr.searchs()
        #         _post_id = dbr.post(int(post_id))
        #         info = dbr.show_seq(int(post_id), q=__tags)
        #         _has_parent = True if info.parent_id or info.has_children else False
        #         Pbtns = post_buttons(
        #             info.id,
        #             _mode,
        #             _tags_code,
        #             _has_parent
        #         )
        #         _ext = info.file_ext
        #         match _ext:
        #             case "gif":
        #                 _mode_input_use = InputMediaAnimation
        #             case "mp4" | "mkv":
        #                 _mode_input_use = InputMediaVideo
        #             case _:
        #                 _mode_input_use = InputMediaPhoto
        #         # lnk = arm_link(info, abso=())
        #         # print(info)
        #         # print(lnk)
        #         try:
        #             fmsl = await app.send_document(
        #                 user_id,
        #                 _post_id.file_url
        #             )
        #             print(fmsl)
        #             logger.info(f"Todo subido en {round(time.perf_counter() - _start, 3)}s :3")
        #         except UserIsBlocked:
        #             logger.info(f"No se pudo enviar archivo a \"{user_id}\" (UserIsBlocked)")
        #         except PeerIdInvalid:
        #             logger.info(f"No se pudo enviar archivo a \"{user_id}\" (PeerIdInvalid)")
        #         except Exception as e:
        #             print(e)
        print(f"Todo subido en {round(time.perf_counter() - _start, 3)}s :3")
        await asyncio.sleep(180)
# await asyncio.sleep(15)
