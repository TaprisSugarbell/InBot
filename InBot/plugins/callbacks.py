import logging
import time

import cloudscraper
from danbooru import Danbooru, arm_link
from pyrogram import Client, filters
from pyrogram.errors import UserIsBlocked, PeerIdInvalid
from pyrogram.types import (InputMediaPhoto, InputMediaAnimation,
                            InputMediaVideo)

from ..helper.__inline_butns__ import *
from ..helper.mongo_connect import *

# VARS
sayulogs = logging.getLogger(__name__)
tc = Mongo(URI, "DanbooruBot", "tag_code")
db = Mongo(URI, "DanbooruBot", "user_settings")
requests = cloudscraper.create_scraper(cloudscraper.Session())


@Client.on_callback_query(filters.regex(r"sfw_\d*"))
async def __callback_safe__(bot, update):
    print(update)
    __tags = ""
    callback_query_id = update.id
    user_id = update.from_user.id
    inline_message_id = update.inline_message_id
    _mode, seq, _tags_code, post_id = iter(update.data.split("_"))
    _start = time.perf_counter()
    __tags = ""
    show_seq = ["prev", "next"]
    _c_ = await confirm(db, {"user_id": user_id})
    if _c_:
        user_settings = _c_[0]
        _username = user_settings["username"]
        _api_key = user_settings["api_key"]
        _password = user_settings["password"]
        _host = user_settings["host"]
        dbr = Danbooru(_username, _api_key, _password, host=_host)
    else:
        _host = "safebooru"
        dbr = Danbooru(host=_host)
        await add_(db, {"user_id": user_id,
                        "username": None,
                        "api_key": None,
                        "password": None,
                        "host": _host})
    _c = await confirm(
        tc,
        {
            "tags_code": _tags_code
        }
    )
    if _c:
        _c = _c[0]
        __tags = _c["tags"]
        if __tags == "order:rank":
            __tags = ""
    # https://danbooru.donmai.us/posts/5406792/show_seq?q=underwear&seq=prev
    xsa = lambda x, y: getattr(x, y)
    if seq in show_seq:
        _srch = dbr.searchs()
        info = dbr.show_seq(int(post_id), q=__tags, seq=seq)
        _has_parent = bool(info.parent_id or info.has_children)
        Pbtns = post_buttons(
            info.id,
            _mode,
            _tags_code,
            _has_parent
        )
        _ext = info.file_ext
        match _ext:
            case "gif":
                _mode_input_use = InputMediaAnimation
            case "mp4" | "mkv" | "webm":
                _mode_input_use = InputMediaVideo
            case _:
                _mode_input_use = InputMediaPhoto
        try:
            lnk = arm_link(info, "large_file_url", ())
            await bot.edit_inline_media(inline_message_id,
                                        media=_mode_input_use(lnk[1], ""))
            await bot.edit_inline_reply_markup(
                inline_message_id,
                reply_markup=Pbtns
            )
        except Exception as e:
            lnk = arm_link(info, abso=())
            await bot.edit_inline_media(inline_message_id,
                                        media=_mode_input_use(lnk[1], ""))
            await bot.edit_inline_reply_markup(
                inline_message_id,
                reply_markup=Pbtns
            )
    elif seq == "file":
        # _srch = dbr.searchs()
        _post_id = dbr.post(int(post_id))
        info = dbr.show_seq(int(post_id), q=__tags)
        _has_parent = bool(info.parent_id or info.has_children)
        Pbtns = post_buttons(
            info.id,
            _mode,
            _tags_code,
            _has_parent
        )
        _ext = info.file_ext
        match _ext:
            case "gif":
                _mode_input_use = InputMediaAnimation
            case "mp4" | "mkv":
                _mode_input_use = InputMediaVideo
            case _:
                _mode_input_use = InputMediaPhoto
        # lnk = arm_link(info, abso=())
        # print(info)
        # print(lnk)
        try:
            fmsl = await bot.send_document(
                user_id,
                _post_id.file_url
            )
            print(fmsl)
            await bot.answer_callback_query(
                callback_query_id,
                "El archivo se subio en privado."
            )
            sayulogs.info(f"Todo subido en {round(time.perf_counter() - _start, 3)}s :3")
        except UserIsBlocked:
            await bot.answer_callback_query(
                callback_query_id,
                "No se pudo subir el archivo porque has bloqueado el bot.\nEntra en @KhoruBot",
                show_alert=True
            )
            sayulogs.info(f"No se pudo enviar archivo a \"{user_id}\" (UserIsBlocked)")
        except PeerIdInvalid:
            await bot.answer_callback_query(
                callback_query_id,
                "No se pudo subir el archivo porque no has abierto chat con el bot.\nEntra en @KhoruBot",
                show_alert=True
            )
            sayulogs.info(f"No se pudo enviar archivo a \"{user_id}\" (PeerIdInvalid)")
        except Exception as e:
            await bot.answer_callback_query(
                callback_query_id,
                "No se pudo subir el archivo por algún fallo que no puedo reconocer."
                "\nEntra en @KhoruBot sino tienes chat con el bot o reportalo a @SayuOgiwara",
                show_alert=True
            )
            sayulogs.error("Error:", exc_info=e)

