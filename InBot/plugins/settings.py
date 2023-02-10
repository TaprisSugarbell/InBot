from danbooru import Danbooru
from pyrogram import Client, filters
from ..helper.mongo_connect import *
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


db = Mongo(URI, "DanbooruBot", "user_settings")


@Client.on_callback_query(filters.regex("settings"))
async def __c_settings__(bot, update):
    print(update)
    user_id = update.from_user.id
    chat_id = update.message.chat.id
    message_id = update.message.message_id
    _c = await confirm(db, {"user_id": user_id})
    if _c:
        user_settings = _c[0]
        _host = user_settings["host"]
    else:
        _host = "safebooru"
        await add_(db, {"user_id": user_id,
                        "username": None,
                        "api_key": None,
                        "password": None,
                        "host": _host})
    if "safe" in _host:
        _mode = "🔞 NSFW 🔞"
        __o = "💮 SFW 💮"
    else:
        _mode = "💮 SFW 💮"
        __o = "🔞 NSFW 🔞"
    await bot.edit_message_text(
        chat_id,
        message_id,
        "Config.\n" + "Your mode: " + __o,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(_mode, "change_host"),
                    InlineKeyboardButton("My Account", "get_user_info")
                ]
            ]
        )
    )


@Client.on_message(filters.command(["settings"]))
async def __settings__(bot, update):
    print(update)
    chat_id = update.chat.id
    user_id = update.from_user.id
    _c = await confirm(db, {"user_id": user_id})
    if _c:
        user_settings = _c[0]
        _host = user_settings["host"]
    else:
        _host = "safebooru"
        await add_(db, {"user_id": user_id,
                        "username": None,
                        "api_key": None,
                        "password": None,
                        "host": _host})
    if "safe" in _host:
        _mode = "🔞 NSFW 🔞"
        __o = "💮 SFW 💮"
    else:
        _mode = "💮 SFW 💮"
        __o = "🔞 NSFW 🔞"
    await bot.send_message(chat_id,
                           "Config.\n" + "Your mode: " + __o,
                           reply_markup=InlineKeyboardMarkup(
                               [
                                   [
                                       InlineKeyboardButton(_mode, "change_host"),
                                       InlineKeyboardButton("My Account", "get_user_info")
                                   ]
                               ]
                           )
                           )


@Client.on_callback_query(filters.regex("change_host"))
async def __ch__(bot, update):
    print(update)
    chat_id = update.message.chat.id
    user_id = update.from_user.id
    message_id = update.message.id
    user_settings = await confirm_one(db, {"user_id": user_id})
    if user_settings:
        # user_settings = _c[0]
        _host = user_settings["host"]
        if _host == "safebooru":
            new_host = "danbooru"
        else:
            new_host = "safebooru"
        await update_one(db,
                         {"user_id": user_id},
                         {"host": new_host})
        if "safe" in new_host:
            _mode = "🔞 NSFW 🔞"
            __o = "💮 SFW 💮"
        else:
            _mode = "💮 SFW 💮"
            __o = "🔞 NSFW 🔞"
        await bot.edit_message_text(chat_id,
                                    message_id,
                                    "Config.\n" + "Your mode: " + __o,
                                    reply_markup=InlineKeyboardMarkup(
                                                [
                                                    [
                                                        InlineKeyboardButton(_mode, "change_host"),
                                                        InlineKeyboardButton("My Account", "get_user_info")
                                                    ]
                                                ]
                                            ))


@Client.on_callback_query(filters.regex("get_user_info") & filters.private)
async def __guinfo__(bot, update):
    print(update)
    chat_id = update.message.chat.id
    user_id = update.from_user.id
    message_id = update.message.message_id
    _c = await confirm(db, {"user_id": user_id})
    if _c:
        user_settings = _c[0]
        _username = user_settings["username"]
        _api_key = user_settings["api_key"]
        _password = user_settings["password"]
    else:
        _username = "None"
        _api_key = "None"
        _password = "None"

    await bot.edit_message_text(chat_id,
                                message_id,
                                f'Username: `{_username}`\n'
                                f'API: `{_api_key}`\n'
                                f'Password: `{_password}`',
                                reply_markup=InlineKeyboardMarkup(
                                    [
                                        [
                                            InlineKeyboardButton("Username", "change_username"),
                                            InlineKeyboardButton("API", "change_api_key")
                                        ],
                                        [
                                            InlineKeyboardButton("Password", "change_password"),
                                            InlineKeyboardButton("Atrás", "settings"),
                                        ]
                                    ]
                                ))


@Client.on_callback_query(filters.regex(r"change_(username|api_key|password)"))
async def __ch_username__(bot, update):
    print(update)
    chat_id = update.message.chat.id
    user_id = update.from_user.id
    message_id = update.message.message_id
    _md = update.data.replace("change_", "")
    mssg = await bot.ask(
        chat_id,
        f"Escribe tu {_md}..."
    )
    print(mssg)
    mssg_id = mssg.request.message_id
    await bot.delete_messages(
        chat_id,
        mssg.message_id
    )
    _txt = mssg.text

    while " " in _txt:
        await bot.delete_messages(
            chat_id,
            mssg_id
        )
        mssg = await bot.ask(
            chat_id,
            f'El "{_md}" no puede tener espacios, envialo de nuevo...'
        )
        mssg_id = mssg.request.message_id
        await bot.delete_messages(
            chat_id,
            mssg.message_id
        )
    _txt = mssg.text

    if _md == "api_key" and _txt != ".":
        while len(mssg.text) != 24 or " " in _txt:
            await bot.delete_messages(
                chat_id,
                mssg_id
            )
            mssg = await bot.ask(
                chat_id,
                f'No has ingresado una "{_md}" valida'
            )
            mssg_id = mssg.request.message_id
            await bot.delete_messages(
                chat_id,
                mssg.message_id
            )
    elif mssg.text == ".":
        _txt = None
        pass
    await bot.edit_message_text(
        chat_id,
        mssg_id,
        f'Se ha guardado "{mssg.text}" como {_md}'
    )
    _c = await confirm(db, {"user_id": user_id})
    user_settings = _c[0]
    _udt = {
            _md: mssg.text
        }
    await update_one(
        db,
        {
            "user_id": user_id
        },
        _udt
    )
    user_settings.update(
        _udt
    )
    _username = user_settings["username"]
    _api_key = user_settings["api_key"]
    _password = user_settings["password"]

    await bot.edit_message_text(chat_id,
                                message_id,
                                f'Username: `{_username}`\n'
                                f'API: `{_api_key}`\n'
                                f'Password: `{_password}`',
                                reply_markup=InlineKeyboardMarkup(
                                    [
                                        [
                                            InlineKeyboardButton("Username", "change_username"),
                                            InlineKeyboardButton("API", "change_api_key")
                                        ],
                                        [
                                            InlineKeyboardButton("Password", "change_password"),
                                            InlineKeyboardButton("Atrás", "settings"),
                                        ]
                                    ]
                                ))






