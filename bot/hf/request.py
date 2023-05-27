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


import requests
from requests.exceptions import Timeout
from requests.adapters import HTTPAdapter, Retry
from pyrogram import (
    Client
)
from bot import (
    SHA_SECRET,
    WEBHOOK_INTEGRATION,
    WEBHOOK_ADDRESS,
    AUTH_CHANNEL,
    logging,
    TG_BOT_TOKEN
)
from os import path
from datetime import datetime
from lxml import html
from lxml.etree import tostring
import hashlib
import hmac
import json


def request_time(client: Client, get_tree={}):
    print("[*] Checking DTU Website for notices now....")
    try:
        s = requests.Session()
        retries = Retry(total=500,
                        backoff_factor=0.1,)
        s.mount('http://', HTTPAdapter(max_retries=retries))
        r = s.get(('http://dtu.ac.in/'))
    except Timeout:
        print("[{}]: The request timed out.".format(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        return [403]

    tree = html.fromstring(r.content)
    if get_tree:
        title = notice_title(get_tree["tab_index"], get_tree["link_index"], tree)
        rest = notice_link(get_tree["tab_index"], get_tree["link_index"], tree)
        notice = {
            "title": title,
            "link": rest[0],
            "children": {
                "titles": rest[2],
                "links": rest[1]
            },
            "tab": get_tree["tab"]
        }
        return notice
    try:
        top_notice = tree.xpath(
            '//*[@id="tab4"]/div[1]/ul/li[1]/h6/a')[0].text_content().strip().replace("\u201c", "").replace("\u201d", "")
    except Exception as e:
        top_notice = '-Please check yourself-'
        print('TOP NOTICE TITLE ERROR ' + str(e))
    
    try:
        top_link = tree.xpath(
            '//*[@id="tab4"]/div[1]/ul/li[1]/h6/a')[0]
        top_link = top_link.attrib.get('href', None)
        if top_link is not None:
            top_link = ('http://dtu.ac.in' + top_link.split('.', 1)[1])
    except IndexError:
        top_link = ''

    tabs = [1, 2, 3, 4, 5]
    tab_titles = ['Notices', 'Jobs', 'Tenders',
                  'Latest News', 'Forthcoming Events']
    y = 0
    records = {}
    titles = []
    for tab_iterator in tabs:
        tab = tab_titles[y]
        full_list = tree.xpath('//*[@id="tab{}"]/div[1]/ul'.format(tab_iterator))[0]
        max_range = 1
        for ele in full_list:
            if ele.tag == 'li' and ele.get('class', None) is None:
                max_range += 1
        max_range = min(max_range, 15)
        for notice_iterator in range(1, max_range):
            try:
                title = notice_title(tab_iterator, notice_iterator, tree)
                rest = notice_link(tab_iterator, notice_iterator, tree)
                notice = {
                    "title": title,
                    "link": rest[0],
                    "children": {
                        "titles": rest[2],
                        "links": rest[1]
                    },
                    "tab": tab
                }
                if title != "":
                    titles.append(notice)
            except Exception as e:
                print("No title - " + str(e))
                pass
        records[tab] = titles
        titles = []
        y += 1
        max_range = 2

    previous_records = records
    if not path.exists("bot/hf/recorded_status.json"):
        data = json.dumps(previous_records)
        with open("bot/hf/recorded_status.json", "w+") as f:
            f.write(data)
            print("[*] Recorded Current Status.\n[*] Latest dates: {}".format(data))
            return_values = [404, top_notice, top_link, ' ', ' ']
            return return_values
    else:
        with open("bot/hf/recorded_status.json", "r") as f:
            data = f.read()
        previous_records = json.loads(data)
        modified_keys = dict_compare(records, previous_records)
        if modified_keys != []:
            logging.info(modified_keys)
            if(WEBHOOK_INTEGRATION):
                try:
                    data = {"notice": modified_keys}
                    xhash = sign_request(json.dumps(data, separators=(',', ':')))
                    send_webhook_alert(xhash, json.dumps(data, separators=(',', ':')))
                except Exception as e:
                    logging.error(e)
            else:
                logging.info("Webhook not configured. Skipping webhook event.")
            # return_values = [200, top_notice,
            #                  top_link, modified_keys["title"], modified_keys["link"], modified_keys["tab"]]
            return_values = [200, top_notice,
                             top_link, modified_keys]
            return return_values
        else:
            return_values = [404, top_notice, top_link, ' ', ' ']
            return return_values


def notice_title(tab_iterator, notice_iterator, tree):
    try:
        top_notice = tree.xpath(
            '//*[@id="tab{}"]/div[1]/ul/li[{}]/h6/a'.format(tab_iterator, notice_iterator))[0].text_content().strip().replace("\u201c", "").replace("\u201d", "")
        return top_notice
    except Exception as e:
        print('TITLE ERROR ' + str(e))
        sendtelegram(2, AUTH_CHANNEL, '_', 'Got an error finding the notice title.')


def notice_link(tab_iterator, notice_iterator, tree):
    try:
        links= []
        children = []
        notice_self_link = tree.xpath(
            '//*[@id="tab{}"]/div[1]/ul/li[{}]/h6/a'.format(tab_iterator, notice_iterator))[0]
        notice_self_link = notice_self_link.attrib.get('href', None)
        if notice_self_link is not None:
            notice_self_link = ('http://dtu.ac.in' + notice_self_link.split('.', 1)[1])
        
        separators = tree.xpath('//*[@id="tab{}"]/div[1]/ul/li[{}]/h6'.format(tab_iterator, notice_iterator))[0]
        if "#160".encode() in tostring(separators):
            # contains child links
            if "maroon".encode() in tostring(separators):
                # red link, contains all in h6
                for x in range(2,len(separators)):
                    if '<!--'.encode() in tostring(separators[x]):
                        pass
                    link = separators[x].attrib.get('href', None)
                    child = separators[x].text_content().replace('\xa0', '').replace('||', '')
                    if link is not None:
                        links.append('http://dtu.ac.in' + link.split('.', 1)[1])
                    if child != '' and 'Date' not in child:
                        children.append(child)
            else:
                ele = tree.xpath('//*[@id="tab{}"]/div[1]/ul/li[{}]/h6'.format(tab_iterator, notice_iterator))[0]
                for x in range(1,len(ele)):
                    if '<!--'.encode() in tostring(ele[x]):
                        continue
                    link = ele[x].attrib.get('href', None)
                    child = ele[x].text_content().replace('\xa0', '').replace('||', '')
                    if link is not None:
                        links.append('http://dtu.ac.in' + link.split('.', 1)[1])
                    if child != '' and 'Date' not in child:
                        children.append(child)
        return [notice_self_link, links, children]
    except Exception as e:
        print(str(tab_iterator), str(notice_iterator))
        print('LINK ERROR ' + str(e))
        # sendtelegram(2, AUTH_CHANNEL, '_', 'Got an error finding the notice link.')


def dict_compare(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    shared_keys = d1_keys.intersection(d2_keys)
    out = []
    for o in shared_keys:
        for i in d1[o]:
            if i not in d2[o]:
                out.append(i)

    return out


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
