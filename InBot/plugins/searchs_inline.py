import re
import time
import string
import logging
import asyncio
import sys
import traceback
import cloudscraper
from .. import queue_
import pyrogram.errors
# from ..helper import *
from ..helper.utils import tag_code
from danbooru.exceptions import *
from pyrogram import Client, filters
from ..helper.mongo_connect import *
from ..helper.__inline_butns__ import *
from ..helper.__vars__ import __error_404__
from danbooru import Danbooru, arm_links, arm_link
from danbooru.types.Danbooru_Types import get_category
from pyrogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                            InlineQueryResultPhoto, InputTextMessageContent,
                            InputMediaPhoto, InputMediaVideo, InputMediaAnimation,
                            InlineQueryResultVideo, InlineQueryResultArticle, InputMediaDocument,
                            InlineQueryResultAnimation, InputMediaVideo)

# VARS
sayulogs = logging.getLogger(__name__)
tc = Mongo(URI, "DanbooruBot", "tag_code")
db = Mongo(URI, "DanbooruBot", "user_settings")
requests = cloudscraper.create_scraper(cloudscraper.Session())


async def image_append(_dats: tuple):
    info, _mode, _tag_code, url, thumb_url = _dats
    if _tag_code == "":
        _tag_code = "0"
    _has_parent = bool(info.parent_id or info.has_children)
    xsa = lambda x, y: getattr(x, y)
    Pbtns = post_buttons(info.id, _mode, _tag_code, _has_parent)
    match info.file_ext:
        case "png" | "jpg" | "jpeg":
            return InlineQueryResultPhoto(url, thumb_url, reply_markup=Pbtns)
        case "gif":
            return InlineQueryResultAnimation(url, thumb_url=thumb_url, reply_markup=Pbtns)
        case _:
            return InlineQueryResultVideo(url, thumb_url, str(xsa(info, "id")), reply_markup=Pbtns)


@Client.on_inline_query()
async def __safebooru__(bot, update):
    _start = time.perf_counter()
    bsq = None
    bsqe = None
    imgs = []
    tasks = []
    __tags = ""
    query_id = update.id
    query = update.query
    user_id = update.from_user.id
    _c = await confirm(db, {"user_id": user_id})
    if _c:
        user_settings = _c[0]
        _username = user_settings["username"]
        _api_key = "YvA3fGthBXHpwZegzPuRdfia"
        # _api_key = user_settings["api_key"]
        _password = user_settings["password"]
        _host = user_settings["host"]
        dbr = Danbooru(_username, _api_key, _password, host=_host)
        # print(_username, _api_key, _password, _host)
    else:
        _host = "safebooru"
        dbr = Danbooru(host=_host)
        await add_(db, {"user_id": user_id,
                        "username": None,
                        "api_key": None,
                        "password": None,
                        "host": _host})
    _mode = "sfw" if "safe" in _host else "nsfw"
    try:
        offset = int(update.offset)
    except ValueError:
        offset = 1
    xsa = lambda x, y: getattr(x, y)
    if len(query.strip()) == 0:
        bsq = dbr.searchs(limit=50, page=offset)
        searchs = arm_links(bsq, "large_file_url", ())
        search_thumbs = arm_links(bsq, "preview_file_url")
        _tag_code = await tag_code(__tags)
        for (info, url), thumb_url in zip(searchs, search_thumbs):
            if thumb_url:
                # _get_tag_code = await tag_code(__tags)
                _dts = info, _mode, _tag_code, url, thumb_url
                tasks.append(asyncio.create_task(image_append(_dts)))
                # imgs.append()
                # _id = f'{_mode}_{xsa(info, "id")}'
        #         _dts = info, _mode, __tags, url, thumb_url
        #         imgs.append(
        #             image_append(_dts)
        #         )
        #         imgs.append(
        #             executor.submit(image_append, _dts).result()
        #         )
    else:
        try:
            bsqe = dbr.post(post_id=int(query))
            searchs = [arm_link(bsqe, "preview_file_url", ())]
            search_thumbs = [arm_link(bsqe, "large_file_url")]
            if bsqe.parent_id:
                bsqe = dbr.post(post_id=bsqe.parent_id)
                searchs.append(arm_link(bsqe, "large_file_url", ()))
                search_thumbs.append(arm_link(bsqe, "preview_file_url", ()))
            for (info, url), thumb_url in zip(searchs, search_thumbs):
                if thumb_url:
                    _dts = info, _mode, __tags, url, thumb_url
                    tasks.append(asyncio.create_task(image_append(_dts)))
        except ValueError:
            if query.strip() == "random":
                bsq = dbr.searchs(limit=50, random=True)
            elif "random" in query.strip():
                __tags = str(query).replace("random", "").strip()
                try:
                    bsq = dbr.searchs(tags=__tags, limit=50, random=True)
                except DanbooruLimitError:
                    bsq = None
            elif "*" in query.strip():
                __tags = str(query).replace("*", "").strip()
                _rsts = dbr.autocomplete(__tags)
                for i in _rsts:
                    imgs.append(
                        InlineQueryResultArticle(
                            title=i.label,
                            input_message_content=InputTextMessageContent(
                                f"{i.label}\n`{i.value}`"
                            ),
                            description=f"tag={i.value} category={get_category(i.category)} posts={i.post_count}",
                            reply_markup=InlineKeyboardMarkup(
                                [
                                    [
                                        InlineKeyboardButton("Find",
                                                             switch_inline_query_current_chat=i.value)
                                    ]
                                ]
                            )
                        )
                    )
            else:
                try:
                    bsq = dbr.searchs(tags=query, limit=50, page=offset)
                    __tags = query
                except DanbooruLimitError:
                    bsq = None
            if bsq is None and not imgs and "*" not in query:
                __upgrade_account_url = "https://danbooru.donmai.us/user_upgrades/new"
                st = "Only gold accounts or higher can search with more than 2 tags at the same time."
                stm = f"Only gold [accounts]({__upgrade_account_url}) or higher can search with more " \
                      f"than 2 tags at the same time."
                imgs = [
                    InlineQueryResultArticle(
                        title="You cannot search for more than 2 tags at a time.",
                        input_message_content=InputTextMessageContent(
                            stm,
                            parse_mode="md"
                        ),
                        description=st,
                        url=__upgrade_account_url,
                        thumb_url=__error_404__
                    )
                ]
            elif bsq:
                searchs = arm_links(bsq, "large_file_url", ())
                search_thumbs = arm_links(bsq, "preview_file_url")
                _tag_code = await tag_code(__tags)
                for (info, url), thumb_url in zip(searchs, search_thumbs):
                    if thumb_url:
                        _dts = info, _mode, _tag_code, url, thumb_url
                        tasks.append(asyncio.create_task(image_append(_dts)))
    if tasks:
        imgs.extend(await asyncio.gather(*tasks))
        print(f"Todo subido en {round(time.perf_counter() - _start, 3)}s :3")
    print(len(imgs))
    if bsq:
        next_offset = str(offset + 1)
        try:
            await bot.answer_inline_query(query_id,
                                          imgs,
                                          cache_time=10,
                                          is_gallery=True,
                                          next_offset=next_offset)
        except Exception as e:
            print(e)
    elif bsqe:
        try:
            await bot.answer_inline_query(query_id,
                                          imgs,
                                          cache_time=10,
                                          is_gallery=True)
        except Exception as e:
            print(e)
    else:
        try:
            await bot.answer_inline_query(query_id,
                                          imgs)
        except Exception as e:
            print(e)


# @Client.on_chosen_inline_result()
# async def __chose_safe__(bot, update):
#     print(update)
#     xsa = lambda x, y: getattr(x, y)
#     if re.fullmatch(r"n?sfw_\d*", str(update.result_id)):
#         if "n" in update.result_id:
#             _host = "danbooru"
#         else:
#             _host = "safebooru"
#         _booru = Danbooru(host=_host)
#         _pattern = int(re.sub(r"n?sfw_", "", str(update.result_id)))
#         lnk_dct = _booru.post(post_id=_pattern)
#         print(lnk_dct)
#         try:
#             lnk = arm_link(lnk_dct, "large_file_url", ())
#             await bot.edit_inline_media(
#                 update.inline_message_id,
#                 media=InputMediaPhoto(lnk[1], f'https://{_booru.host}.donmai.us/posts/{xsa(lnk[0], "id")}'))
#         except Exception as e:
#             sayulogs.error("Error en el sample.", exc_info=e)
#             lnk = arm_link(lnk_dct, abso=())
#             await bot.edit_inline_media(
#                 update.inline_message_id,
#                 media=InputMediaPhoto(lnk[1], f'https://{_booru.host}.donmai.us/posts/{xsa(lnk[0], "id")}'))


# @Client.on_callback_query(filters.regex(r"sfw_\d*"))
# async def __callback_safe__(bot, update):
#     print(update)
#     __tags = ""
#     user_id = update.from_user.id
#     inline_message_id = update.inline_message_id
#     _mode, seq, _tags_code, post_id = (_ for _ in update.data.split("_"))
#     queue_.put(
#         (
#             0,
#             {
#                 "user_id": user_id,
#                 "inline_message_id": inline_message_id,
#                 "mode": _mode,
#                 "seq": seq,
#                 "tag_code": _tags_code,
#                 "post_id": post_id
#             }
#          )
#     )
    # _c_ = await confirm(db, {"user_id": user_id})
    # if _c_:
    #     user_settings = _c_[0]
    #     _username = user_settings["username"]
    #     _api_key = user_settings["api_key"]
    #     _password = user_settings["password"]
    #     _host = user_settings["host"]
    #     dbr = Danbooru(_username, _api_key, _password, host=_host)
    # else:
    #     _host = "safebooru"
    #     dbr = Danbooru(host=_host)
    #     await add_(db, {"user_id": user_id,
    #                     "username": None,
    #                     "api_key": None,
    #                     "password": None,
    #                     "host": _host})
    # _c = await confirm(
    #     tc,
    #     {
    #         "tags_code": _tags_code
    #     }
    # )
    # if _c:
    #     _c = _c[0]
    #     __tags = _c["tags"]
    # # https://danbooru.donmai.us/posts/5406792/show_seq?q=underwear&seq=prev
    # xsa = lambda x, y: getattr(x, y)
    # if seq in show_seq:
    #     _srch = dbr.searchs()
    #     info = dbr.show_seq(int(post_id), q=__tags, seq=seq)
    #     _has_parent = True if info.parent_id or info.has_children else False
    #     Pbtns = post_buttons(
    #         info.id,
    #         _mode,
    #         _tags_code,
    #         _has_parent
    #     )
    #     _ext = info.file_ext
    #     match _ext:
    #         case "gif":
    #             _mode_input_use = InputMediaAnimation
    #         case "mp4" | "mkv":
    #             _mode_input_use = InputMediaVideo
    #         case _:
    #             _mode_input_use = InputMediaPhoto
    #     try:
    #         lnk = arm_link(info, "large_file_url", ())
    #         await bot.edit_inline_media(inline_message_id,
    #                                     media=_mode_input_use(lnk[1], ""))
    #         await bot.edit_inline_reply_markup(
    #             inline_message_id,
    #             reply_markup=Pbtns
    #         )
    #     except Exception as e:
    #         sayulogs.error("Error en el sample.", exc_info=e)
    #         lnk = arm_link(info, abso=())
    #         await bot.edit_inline_media(inline_message_id,
    #                                     media=_mode_input_use(lnk[1], ""))
    #         await bot.edit_inline_reply_markup(
    #             inline_message_id,
    #             reply_markup=Pbtns
    #         )
    # elif seq == "file":
    #     # _srch = dbr.searchs()
    #     _post_id = dbr.post(int(post_id))
    #     info = dbr.show_seq(int(post_id), q=__tags)
    #     _has_parent = True if info.parent_id or info.has_children else False
    #     Pbtns = post_buttons(
    #         info.id,
    #         _mode,
    #         _tags_code,
    #         _has_parent
    #     )
    #     _ext = info.file_ext
    #     match _ext:
    #         case "gif":
    #             _mode_input_use = InputMediaAnimation
    #         case "mp4" | "mkv":
    #             _mode_input_use = InputMediaVideo
    #         case _:
    #             _mode_input_use = InputMediaPhoto
    #     lnk = arm_link(info, abso=())
    #     # print(info)
    #     # print(lnk)
    #     fmsl = await bot.send_document(
    #         user_id,
    #         _post_id.file_url
    #     )
    #     print(fmsl)

    # xsa = lambda x, y: getattr(x, y)
    # if re.fullmatch(r"sfw_\d*", str(update.data)):
    #     _booru = Danbooru("safebooru")
    #     _pattern = int(re.sub(r"sfw_", "", str(update.data)))
    #     lnk_dct = _booru.post(post_id=_pattern)
    #     try:
    #         lnk = arm_link(lnk_dct, "large_file_url", ())
    #         await bot.edit_inline_media(update.inline_message_id,
    #                                     media=InputMediaPhoto(lnk[1],
    #                                                           f'https://safebooru.donmai.us/posts/{xsa(lnk[0], "id")}'))
    #     except Exception as e:
    #         sayulogs.error("Error en el sample.", exc_info=e)
    #         lnk = arm_link(lnk_dct, abso=())
    #         await bot.edit_inline_media(update.inline_message_id,
    #                                     media=InputMediaPhoto(lnk[1],
    #                                                           f'https://safebooru.donmai.us/posts/{xsa(lnk[0], "id")}'))
