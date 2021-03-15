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
    filters.command("send", COMMM_AND_PRE_FIX) & filters.chat(AUTH_CHANNEL)
)
async def missed_noti(client: Client, message: Message):
    inputm = message.text
    try:
        comm, url, title, tab = inputm.split("|")
    except:
        await client.send_message(
            chat_id=AUTH_CHANNEL,
            text="Format:\n/send|notice_url|notice_title|notice_tab",
        )
        return
    file_id = getDocId(url)
    broadcast_list = user_list()
    total = len(broadcast_list)
    mongo_url, db1 = MONGO_URL.split("net/")
    mongo_url = mongo_url + "net/dtu"
    os.system(
        "mongoexport --uri={} -c=users --type json --out bot/hf/users_{}".format(
            mongo_url, datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        )
    )
    _, _, filenames = next(os.walk("bot/hf/"))
    logging.info(filenames)
    for f in filenames:
        if not ".py" in f:
            await message.reply_document("bot/hf/{}".format(f))
    time.sleep(3)
    alerts = 1
    failed_users = set()
    failed = 0
    while alerts < 2:
        for i in range(0, (total)):
            try:
                pp = "[{}]: DTU Site has been Updated!\n\nLatest Notice Title - \n{}\n\nUnder Tab --> {}\n\nCheers!".format(
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"), title, tab
                )
                send_status = sendtelegram(1, broadcast_list[i], file_id, pp)
                if send_status == 200:
                    i += 1
                    logging.info("[*] Alert Sent to {}/{} people.".format(i, total))
                    time.sleep(0.3)
                elif send_status == 404:
                    failed += 1
                    i += 1
                    failed_users.add(broadcast_list[i])
                    time.sleep(0.3)
            except Exception as e:
                logging.error("[*] {}".format(e))
        alerts += 1
        time.sleep(1)

    time.sleep(1)
    done = "[*] Notice Alert Sent to {}/{} people.\n {} user(s) were removed from database.".format(
        (int(total - failed)), total, failed
    )
    sendtelegram(
        3, AUTH_CHANNEL, "https://telegra.ph/file/d88f31ee50c8362e86aa8.mp4", done
    )
    logging.critical(done)
    sys.exit()

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
