from pyrogram import (
    Client,
    filters
)
from pyrogram.types import (
    Message
)
from bot import (
    AUTH_CHANNEL,
    COMMM_AND_PRE_FIX,
    LOG_FILE_ZZGEVC,
    HELP_MEHH
)
from bot.hf.flifi import uszkhvis_chats_ahndler
from .broadcast import check_status

@Client.on_message(filters.command("help", COMMM_AND_PRE_FIX))
async def get_this_man_some_help(_, message: Message):
    await message.reply_text(
        HELP_MEHH,
        quote=True
    )

@Client.on_message(filters.command("status", COMMM_AND_PRE_FIX))
async def tu_ruk_baba_me_dekhta_na(_, message:Message):
    check_status(message.from_user.id, message.from_user.username)

@Client.on_message(
    filters.command('logs', COMMM_AND_PRE_FIX) &
    uszkhvis_chats_ahndler([AUTH_CHANNEL])
)
async def ye_dekh_kya_hogaya(_, message: Message):
    await message.reply_document(
        "{}".format(LOG_FILE_ZZGEVC)
    )
