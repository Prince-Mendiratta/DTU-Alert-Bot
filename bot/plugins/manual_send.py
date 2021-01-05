import time
from pyrogram import (
    Client,
    filters
)
from pyrogram.types import (
    Message
)
from bot import (
    AUTH_CHANNEL,
    REQUEST_INTERVAL,
    TG_BOT_TOKEN,
    COMMM_AND_PRE_FIX,
    LOG_FILE_ZZGEVC
)
from bot.hf.flifi import uszkhvis_chats_ahndler
from bot.mongodb.users import user_list, remove_client_from_db
from .broadcast import getDocId
from datetime import datetime
from pyrogram.errors.exceptions import UserIsBlocked, ChatWriteForbidden
from bot import logging


@Client.on_message(
    filters.command('send', COMMM_AND_PRE_FIX) &
    uszkhvis_chats_ahndler([AUTH_CHANNEL])
)
async def missed_noti(client: Client, message: Message):
    inputm = message.text
    try:
        comm,url,title,tab = inputm.split("|")
    except:
        await client.send_message(chat_id= AUTH_CHANNEL, text="Format:\n/send|notice_url|notice_title|notice_title")
        return
    broadcast_list = user_list()
    total = len(broadcast_list)
    alerts = 0
    while alerts < 2:
        failed = 0
        for i in range(0,(total)):
            try:
                pp = "[{}]: DTU Site has been Updated!\n\nLatest Notice Title - \n{}\n\nUnder Tab --> {}\n\nCheers!".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),title,tab)
                await client.send_document(
                    chat_id=broadcast_list[i],
                    document=url,
                    caption=pp
                    )
                i += 1
                logging.info("[*] Alert Sent to {}/{} people.".format(i,total))
                time.sleep(0.3)
            except Exception as e:
                failed += 1
                i += 1 
                remove_client_from_db(broadcast_list[i])
                logging.error("[*] {}".format(e))
        alerts += 1
        time.sleep(1)
    time.sleep(1)
    done="[*] Notice Alert Sent to {}/{} people.\n {} user(s) were removed from database.".format((int(total-failed)),total,failed)
    logging.critical(done)
    await client.send_animation(chat_id=AUTH_CHANNEL, animation="https://telegra.ph/file/d88f31ee50c8362e86aa8.mp4", caption=done)
