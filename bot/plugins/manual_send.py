import time
from pyrogram import Client, filters
from pyrogram.types import Message
from bot import (
    AUTH_CHANNEL,
    REQUEST_INTERVAL,
    TG_BOT_TOKEN,
    COMMM_AND_PRE_FIX,
    LOG_FILE_ZZGEVC,
    MONGO_URL,
)
from bot.mongodb.users import user_list, remove_client_from_db
from .broadcast import getDocId, sendtelegram
from datetime import datetime
from pyrogram.errors.exceptions import UserIsBlocked, ChatWriteForbidden, PeerIdInvalid
from bot import logging
import os
import sys



@Client.on_message(
    filters.command("promo", COMMM_AND_PRE_FIX) & filters.chat(AUTH_CHANNEL)
)
async def missed_noti(client: Client, message: Message):
    inputm = message.text
    try:
        comm, mess = inputm.split("|")
    except:
        await client.send_message(
            chat_id=AUTH_CHANNEL,
            text="Format:\n/promo |message",
        )
        return
    broadcast_list = user_list()
    total = len(broadcast_list)
    failed_users = []
    failed = 0
    for i in range(0, (total)):
        try:
            send_status = sendtelegram(2, broadcast_list[i], '', mess)
            if send_status == 200:
                i += 1
                logging.info("[*] Alert Sent to {}/{} people.".format(i, total))
                time.sleep(0.3)
            elif send_status == 403:
                failed += 1
                i += 1
                failed_users.append(broadcast_list[i])
                time.sleep(0.3)
        except Exception as e:
            logging.error("[*] {}".format(e))
    done = "[*] Notice Alert Sent to {}/{} people.\n {} user(s) were removed from database.".format(
        (int(total - failed)), total, failed
    )
    logging.info(failed_users)
    sendtelegram(
        3, AUTH_CHANNEL, "https://telegra.ph/file/d88f31ee50c8362e86aa8.mp4", done
    )
    logging.critical(done)
    sys.exit()
