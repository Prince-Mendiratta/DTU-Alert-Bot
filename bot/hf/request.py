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


import os.path
import sys
import requests
import time
import json
from pyrogram import (
    Client
)
from bot import (
    SHA_SECRET,
    WEBHOOK_INTEGRATION,
    WEBHOOK_ADDRESS
)
from os import path
from datetime import datetime
from bs4 import BeautifulSoup
from requests.exceptions import Timeout
from lxml import html
from bot import logging
import hashlib
import hmac
import base64
import json
from requests.adapters import HTTPAdapter, Retry


def request_time(client: Client):
    print("[*] Checking DTU Website for notices now....")
    try:
        s = requests.Session()
        retries = Retry(total=500,
                        backoff_factor=0.1,)
        s.mount('http://', HTTPAdapter(max_retries=retries))
        r = s.get(('http://dtu.ac.in/'), timeout=25)
    except Timeout:
        print("[{}]: The request timed out.".format(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        return [403]

    tree = html.fromstring(r.content)
    try:
        top_notice = tree.xpath(
            '//*[@id="tab4"]/div[1]/ul/li[1]/h6/a/text()')[0]
        if top_notice == " ":
            raise IndexError
    except IndexError:
        try:
            top_noticee = tree.xpath(
                '//*[@id="tab4"]/div[1]/ul/li[1]/h6/a/font/text()')
            top_notice = top_noticee[0]
        except Exception as e:
            logging.error(e)
            top_notice = "-Please check yourself-"
    try:
        top_link = tree.xpath('//*[@id="tab4"]/div[1]/ul/li[1]/h6/a/@href')[0]
        top_link = top_link.split('.', 1)[1]
        top_link = 'dtu.ac.in' + top_link
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
        for notice_iterator in range(1, 15):
            try:
                title = notice_title(tab_iterator, notice_iterator, tree)
                link = notice_link(tab_iterator, notice_iterator, tree)
                notice = {
                    "title": title,
                    "link": link,
                    "tab": tab
                }
                if title != "" and link != "":
                    titles.append(notice)
            except Exception as e:
                print("No title - " + str(e))
                pass
        records[tab] = titles
        titles = []
        y += 1

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
        xpath = tree.xpath(
            '//*[@id="tab{}"]/div[1]/ul/li[{}]/h6/a/text()'.format(tab_iterator, notice_iterator))
        return xpath[0].strip().replace("\u201c", "").replace("\u201d", "")
        if top_notice == ' ':
            raise IndexError
    except IndexError:
        try:
            notice = tree.xpath(
                '//*[@id="tab{}"]/div[1]/ul/li[{}]/h6/a/font/text()'.format(tab_iterator, notice_iterator))
            return notice[0].strip().replace("\u201c", "").replace("\u201d", "")
        except Exception as e:
            print(e)
    return ""


def notice_link(tab_iterator, notice_iterator, tree):
    try:
        link = tree.xpath(
            '//*[@id="tab{}"]/div[1]/ul/li[{}]/h6/a/@href'.format(tab_iterator, notice_iterator))[0]
        link = link.split('.', 1)[1]
        link = 'http://dtu.ac.in' + link
        # No document attached
        if(link.endswith('/')):
            return ""
        return link
    except Exception as e:
        print(e)
        return ""


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
