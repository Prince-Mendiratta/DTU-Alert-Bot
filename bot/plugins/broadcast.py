import asyncio
from datetime import datetime, timedelta
import os.path
import os
import random
import string
import time
import traceback

import aiofiles
from pyrogram.errors import (
    FloodWait,
    InputUserDeactivated,
    PeerIdInvalid,
    UserIsBlocked,
)
from pyrogram import Client, filters
from pyrogram.types import Message

import requests
import threading
from bot import AUTH_CHANNEL, REQUEST_INTERVAL, TG_BOT_TOKEN, MONGO_URL, COMMM_AND_PRE_FIX
from bot.hf.request import request_time
from bot.mongodb.users import user_list, remove_client_from_db
from bot import logging
from pyrogram.errors.exceptions import UserIsBlocked, ChatWriteForbidden
from requests.adapters import HTTPAdapter, Retry
from requests.exceptions import Timeout

broadcast_ids = {}

@Client.on_message(
    filters.command("init", COMMM_AND_PRE_FIX) & filters.chat(AUTH_CHANNEL)
)
def get_mod(client: Client, message: Message):
    try:
        req_result = request_time(client)
        if req_result[0] == 404:
            mes2 = "[{}]: DTU Website has not been Updated.\nLast Notice - \n{}".format(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"), req_result[1]
            )
            logging.info("[*] DTU Website has not been Updated.")
            with open("bot/plugins/check.txt", "w+") as f:
                f.write(mes2)
                f.close()
        elif req_result[0] == 403:
            sendtelegram(2, AUTH_CHANNEL, "_", "Request Timed Out.")
            mes2 = "[{}]: DTU Website has not been Updated.".format(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        elif req_result[0] == 200:
            mes2 = "[{}]: DTU Website has not been Updated.\nLast Notice - \n{}".format(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"), req_result[1]
            )
            new_notices = req_result[3]
            for notice in new_notices:
                logging.info(
                    "Beginning broadcast for {}.\n".format(notice["title"]))
                t1 = threading.Thread(target=intitateBroadcast,
                                      args=(notice, client,))
                t1.start()
            os.remove("bot/hf/recorded_status.json")
        with open("bot/plugins/check.txt", "w+") as f:
            f.write(mes2)
            f.close()
        try:
            looped = threading.Timer(
                int(REQUEST_INTERVAL), lambda: get_mod(client, message))
            looped.daemon = True
            looped.start()
        except Exception as e:
            logging.critical(e)
            sendtelegram(2, AUTH_CHANNEL, "_", e)
        return mes2
    except Exception as e:
        logging.error(e)
        os.remove("bot/hf/recorded_status.json")
        client.send_message(AUTH_CHANNEL, "Got fatal error - " + str(e))

# Use local file to send alert
async def getDocId(notice, client: Client):
    filename = os.path.basename(notice)
    try:
        s = requests.Session()
        retries = Retry(total=500,
                        backoff_factor=0.1,)
        s.mount('http://', HTTPAdapter(max_retries=retries))
        res = s.get((notice), timeout=25)
    except Timeout:
        print("[{}]: The request timed out.".format(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        return 0
    res = requests.get(notice)
    with open(filename, 'wb') as f:
        f.write(res.content)
    filepath = os.getcwd() + '/' + filename
    bruh = await client.send_document(
        chat_id=AUTH_CHANNEL,
        document=filepath,
    )
    try:
        fileId = bruh.document.file_id
        os.remove(filepath)
        return fileId
    except Exception as e:
        logging.error(e)


def sendtelegram(tipe, user_id, notice, caption):
    if tipe == 1:
        handler = "Document"
        pramas = {"chat_id": user_id, "document": notice, "caption": caption}
    elif tipe == 2:
        handler = "Message"
        pramas = {
            "chat_id": user_id,
            "text": caption,
        }
    elif tipe == 3:
        handler = "Animation"
        pramas = {"chat_id": user_id, "animation": notice, "caption": caption}
    try:
        token = TG_BOT_TOKEN
        r = requests.get(
            "https://api.telegram.org/bot{}/send{}".format(token, handler),
            params=pramas,
        )
        logging.info(r.status_code)
        if r.status_code == 200 and r.json()["ok"]:
            return 200
        elif r.status_code == 403:
            logging.info(
                "[*] Alert was not sent to {} due to being blocked. ".format(user_id))
            return 403
        else:
            logging.info(
                "[*] Alert was not sent to {}. Request - {} ".format(user_id, r.json()))
            raise Exception
    except Exception as e:
        logging.error(e)
        logging.info("[*] Could not send telegram message.")
        return 69


def check_status(user_id, usname):
    print("Checking status")
    sendtelegram(
        2,
        user_id,
        "_",
        "Sending an alert in 5 seconds!\nPlease minimize the app if you want to check notification settings.",
    )
    req_result = request_time(Client)
    time.sleep(4)
    sendtelegram(
        2,
        user_id,
        "_",
        "[*] Last Check - [{}]\nLast Notice - \n{}\nHave a Look! {}".format(
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"), req_result[1], req_result[2]
        ),
    )
    logging.info("[*] {} requested for a status update!".format(usname))


async def getDocIdAsync(req_result, client: Client):
    if req_result["link"] is None:
        return None
    file_id = await getDocId(req_result["link"], client)
    return file_id


def intitateBroadcast(req_result, client: Client):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    file_id = loop.run_until_complete(getDocIdAsync(req_result, client))
    loop.close()
    startBroadcast(req_result, file_id, client)

def startBroadcast(req_result, file_id, client):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(broadcast(req_result, file_id, client))
    loop.close()

async def send_msg(user_id, message, client):
    try:
        await client.send_message(chat_id=user_id, text=message)
        return 200, None
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        return 400, f"{user_id} : deactivated\n"
    except UserIsBlocked:
        return 400, f"{user_id} : blocked the bot\n"
    except PeerIdInvalid:
        return 400, f"{user_id} : user id invalid\n"
    except Exception:
        return 500, f"{user_id} : {traceback.format_exc()}\n"


async def broadcast(req_result, file_id, client: Client):
    all_users = user_list()
    children = ''
    if req_result['children']['titles'] != []:
        children += '🖇 With Sub Links as:\n'
        for i in range(len(req_result['children']['titles'])):
            try:
                children += '🐼 {} : {}\n'.format(
                    req_result['children']['titles'][i], req_result['children']['links'][i])
            except Exception as e:
                print('CHILDREN ERROR - ', str(e))
                children = ''
    broadcast_msg = "📬 __[{}]: DTU Site has been Updated!__\n\n🌀 __Latest Notice Title__ - \n**{}**\n\n{}📍__Under Tab__ --> {}\n\n🔮 Cheers from @DTUAlertBot!".format(
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        req_result["title"],
        children,
        req_result["tab"],
    )
    while True:
        broadcast_id = "".join([random.choice(string.ascii_letters) for i in range(3)])
        if not broadcast_ids.get(broadcast_id):
            break
    out = await client.send_message(AUTH_CHANNEL,
        text=f"Broadcast Started! You will be notified with log file when all the users are notified."
    )
    out = await client.send_message(AUTH_CHANNEL,
        text=broadcast_msg
    )
    start_time = time.time()
    total_users = len(all_users)
    done = 0
    failed = 0
    success = 0
    broadcast_ids[broadcast_id] = dict(
        total=total_users, current=done, failed=failed, success=success
    )
    async with aiofiles.open("broadcast.txt", "w") as broadcast_log_file:
        for user in all_users:
            if file_id is not None:
                try:
                    await client.send_document(int(user), file_id)
                except Exception as e:
                    #ignore, handled by message
                    continue
            sts, msg = await send_msg(user_id=int(user), message=broadcast_msg, client=client)
            if msg is not None:
                await broadcast_log_file.write(msg)
            if sts == 200:
                success += 1
                logging.info(
                    "[*] Alert Sent to {}/{} people.".format(done, total_users))
            else:
                failed += 1
            # if sts == 400:
            #     await db.delete_user(user)
            done += 1
            if broadcast_ids.get(broadcast_id) is None:
                break
            else:
                broadcast_ids[broadcast_id].update(
                    dict(current=done, failed=failed, success=success)
                )
    if broadcast_ids.get(broadcast_id):
        broadcast_ids.pop(broadcast_id)
    completed_in = timedelta(seconds=int(time.time() - start_time))
    await asyncio.sleep(3)
    await out.delete()
    if failed == 0:
        await client.send_message(
            AUTH_CHANNEL,
            text=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed."
        )
    else:
        await client.send_document(
            AUTH_CHANNEL,
            document="broadcast.txt",
            caption=f"broadcast completed in `{completed_in}`\n\nTotal users {total_users}.\nTotal done {done}, {success} success and {failed} failed."
        )
    os.remove("broadcast.txt")
