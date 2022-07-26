from pyrogram import Client, filters
from pyrogram.types import Message
from bot import AUTH_CHANNEL, COMMM_AND_PRE_FIX, LOG_FILE_ZZGEVC, HELP_MEHH, CREATOR
from .broadcast import check_status
import logging
from os import walk


@Client.on_message(filters.command("help", COMMM_AND_PRE_FIX))
async def get_this_man_some_help(_, message: Message):
    await message.reply_text(HELP_MEHH, quote=True, disable_web_page_preview=True)


@Client.on_message(filters.command("status", COMMM_AND_PRE_FIX))
async def tu_ruk_baba_me_dekhta_na(_, message: Message):
    check_status(message.from_user.id, message.from_user.username)


@Client.on_message(filters.command("creator", COMMM_AND_PRE_FIX))
async def creator(_, message: Message):
    await message.reply_text(CREATOR, quote=True, disable_web_page_preview=True)


@Client.on_message(
    filters.command("logs", COMMM_AND_PRE_FIX) & filters.chat(AUTH_CHANNEL)
)
async def ye_dekh_kya_hogaya(_, message: Message):
    await message.reply_document("{}".format(LOG_FILE_ZZGEVC))
    _, _, filenames = next(walk("bot/hf/"))
    logging.info(filenames)
    for f in filenames:
        if not ".py" in f:
            await message.reply_document("bot/hf/{}".format(f))
