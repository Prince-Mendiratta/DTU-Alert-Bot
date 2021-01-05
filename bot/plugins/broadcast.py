#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Prince Mendiratta
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import time
import os
import os.path
import requests
import threading
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
    MONGO_URL
)
from os import path
from bot.hf.flifi import uszkhvis_chats_ahndler
from bot.hf.request import request_time
from bot.mongodb.users import user_list, remove_client_from_db
from datetime import datetime
from pyrogram.errors.exceptions import UserIsBlocked, ChatWriteForbidden
from bot import logging


def get_mod(client: Client):
    req_result = request_time(Client)
    mes2 = "[{}]: DTU Website has not been Updated.\nLast Notice - \n{}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),req_result[1])
    if req_result[0] == 404:
        logging.info("[*] DTU Website has not been Updated.")
    elif req_result[0] == 200:
        file_id = getDocId(req_result[4])
        broadcast_list = user_list()
        total = len(broadcast_list)
        mongo_url, db1 = MONGO_URL.split("net/")
        mongo_url = mongo_url + 'net/dtu'
        backup_file = "bot/hf/users_{}".format(datetime.now().strftime("%Y_%m_%d_%H:%M:%S"))
        backup_cmd = "mongoexport --uri={} -c=users --type json --out {}".format(mongo_url,backup_file)
        subprocess.Popen(backup_cmd.split(), stdout=subprocess.PIPE)
        time.sleep(10)
        alerts = 0
        while alerts < 2:
            failed = 0
            for i in range(0,(total)):
                try:
                    pp = "[{}]: DTU Site has been Updated!\n\nLatest Notice Title - \n{}\n\nUnder Tab --> {}\n\nCheers!".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"),req_result[3],req_result[5])
                    send_status = sendtelegram(1, broadcast_list[i], files_id, pp)
                    if send_status == 200:
                        i += 1
                        logging.info("[*] Alert Sent to {}/{} people.".format(i,total))
                        time.sleep(0.3)
                    elif send_status == 404:
                        failed += 1
                        i += 1
                        remove_client_from_db(broadcast_list[i])
                        time.sleep(0.3)
                except Exception as e:
                    logging.error("[*] {}".format(e))
            alerts += 1
            time.sleep(1)
        os.remove("bot/hf/recorded_status.json")
        time.sleep(2)
        done="[*] Notice Alert Sent to {}/{} people.\n {} user(s) were removed from database.".format((int(total-failed)),total,failed)
        logging.critical(done)
        sendtelegram(3 ,AUTH_CHANNEL, "https://telegra.ph/file/d88f31ee50c8362e86aa8.mp4", done)
    with open("bot/plugins/check.txt", "w+") as f:
        f.write(mes2)
        f.close()
    try:
        looped = threading.Timer(int(REQUEST_INTERVAL),lambda: get_mod(Client))
        looped.daemon = True
        looped.start()
    except Exception as e:
        logging.critical(e)
        sendtelegram(2 ,AUTH_CHANNEL, "_", e)
    return mes2


def getDocId(notice):
    try:
        token = TG_BOT_TOKEN
        r = requests.get(
            "https://api.telegram.org/bot{}/sendDocument".format(token),
            params={
                "chat_id": AUTH_CHANNEL,
                "document": notice,
                "caption" : "[Logs] New Notice."
            })
        if r.status_code == 200 and r.json()["ok"]:
            doc_file_id = r.json()['result']['document']['file_id']
            return doc_file_id
        else:
            raise Exception
    except Exception as e:
        logging.error(e)
        logging.info("[*] [{}]: Could not send telegram message.".format(datetime.now()))
        doc_file_id = 0
        return doc_file_id


def sendtelegram(tipe, user_id, notice, caption):
    if tipe == 1:
        handler = "Document"
        pramas={
            "chat_id": user_id,
            "document": notice,
            "caption" : caption
        }
    elif tipe == 2:
        handler = "Message"
        pramas={
            "chat_id": user_id,
            "text": caption,
        }
    elif tipe == 3:
        handler = "Animation"
        pramas={
            "chat_id": user_id,
            "animation": notice,
            "caption" : caption
        }
    try:
        token = TG_BOT_TOKEN
        r = requests.get(
            "https://api.telegram.org/bot{}/send{}".format(token,handler),
            params=pramas)
        if r.status_code == 200 and r.json()["ok"]:
            return 200
        else:
            raise Exception
    except Exception as e:
        print(e)
        logging.info("[*] Could not send telegram message.")
        return 404
    

def check_status(user_id, usname):
    sendtelegram(2, user_id, '_', "Sending an alert in 5 seconds!\nPlease minimize the app if you want to check notification settings.")
    time.sleep(6)
    req_result = request_time(Client)
    sendtelegram(2, user_id, '_', '[*] Last Check - [{}]\nLast Notice - \n{}\nHave a Look - {}'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), req_result[1], req_result[2]))
    logging.info("[*] {} requested for a status update!".format(usname))

