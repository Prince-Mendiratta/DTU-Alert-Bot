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
    SHA_SECRET,
    WEBHOOK_ADDRESS,
    WEBHOOK_INTEGRATION
)
from bot.hf.request import request_time
from bot.mongodb.users import user_list, remove_client_from_db
from .broadcast import getDocId, sendtelegram
from datetime import datetime
from pyrogram.errors.exceptions import UserIsBlocked, ChatWriteForbidden, PeerIdInvalid
from bot import logging
import os
import sys
import threading
import hashlib
import hmac
import requests
import json

@Client.on_message(
    filters.command("send", COMMM_AND_PRE_FIX) & filters.chat(AUTH_CHANNEL)
)
async def missed_noti(client: Client, message: Message):
    inputm = message.text
    try:
        comm, url, title, tab = inputm.split("|")
        fileId = await getDocId(url, client)
        if(WEBHOOK_INTEGRATION):
            try:
                data = {"notice": [{
                    "title": title,
                    "link": url,
                    "tab": tab
                }]}
                xhash = sign_request(json.dumps(
                    data, separators=(',', ':')))
                send_webhook_alert(xhash, json.dumps(
                    data, separators=(',', ':')))
            except Exception as e:
                logging.error(e)
        else:
            logging.info("Webhook not configured. Skipping webhook event.")
    except:
        await client.send_message(
            chat_id=AUTH_CHANNEL,
            text="Format:\n/send|notice_url|notice_title|notice_tab",
        )
        return
    t1 = threading.Thread(target=send, args=(url, title, tab, fileId,))
    t1.start()

@Client.on_message(
    filters.command("wasend", COMMM_AND_PRE_FIX) & filters.chat(AUTH_CHANNEL)
)
async def wa_missed_noti(client: Client, message: Message):
    inputm = message.text
    try:
        comm, url, title, tab = inputm.split("|")
        if(WEBHOOK_INTEGRATION):
            try:
                data = {"notice": [{
                    "title": title,
                    "link": url,
                    "tab": tab
                }]}
                xhash = sign_request(json.dumps(
                    data, separators=(',', ':')))
                send_webhook_alert(xhash, json.dumps(
                    data, separators=(',', ':')))
            except Exception as e:
                logging.error(e)
        else:
            logging.info("Webhook not configured. Skipping webhook event.")
    except:
        await client.send_message(
            chat_id=AUTH_CHANNEL,
            text="Format:\n/send|notice_url|notice_title|notice_tab",
        )
        return

@Client.on_message(
    filters.command("rwasend", COMMM_AND_PRE_FIX) & filters.chat(AUTH_CHANNEL)
)
async def wa_missed_notif(client: Client, message: Message):
    inputm = message.text
    try:
        comm, tab_index, link_index, tab = inputm.split("|")
        print(inputm)
        notice = request_time(client, {"tab_index": str(tab_index), "link_index": str(link_index), "tab": str(tab)})
        
        if(WEBHOOK_INTEGRATION):
            try:
                data = {
                    "notice": [notice]
                }
                xhash = sign_request(json.dumps(
                    data, separators=(',', ':')))
                send_webhook_alert(xhash, json.dumps(
                    data, separators=(',', ':')))
            except Exception as e:
                logging.error(e)
        else:
            logging.info("Webhook not configured. Skipping webhook event.")
    except Exception as e:
        await client.send_message(
            chat_id=AUTH_CHANNEL,
            text="Format:\n/send|tab_index|notice_index|tab_name",
        )
        print(e)
        return

def send(url, title, tab, file_id):
    broadcast_list = user_list()
    total = len(broadcast_list)
    alerts = 1
    failed_users = []
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
                    logging.info(
                        "[*] Alert Sent to {}/{} people.".format(i, total))
                    time.sleep(0.3)
                elif send_status == 403:
                    failed += 1
                    i += 1
                    failed_users.append(broadcast_list[i])
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
    time.sleep(20)
    print("exiting")
    sys.exit()

def sign_request(body):

    key = bytes(SHA_SECRET, 'UTF-8')
    body = bytes(str(body), 'UTF-8')

    digester = hmac.new(key, body, hashlib.sha1)
    signature1 = digester.hexdigest()
    return str(signature1)


def send_webhook_alert(xhash, body):
    Headers = {"X-Hub-Signature": xhash, "Content-Type": "application/json"}
    r = requests.post(url=WEBHOOK_ADDRESS, data=body, headers=Headers)
    print(r)
    logging.info("Webhook configured.\nBody - ." +
                 body + "\nURL - " + WEBHOOK_ADDRESS)
