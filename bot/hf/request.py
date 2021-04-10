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
    AUTH_CHANNEL,
    TG_BOT_TOKEN
)
from os import path
from datetime import datetime
from bs4 import BeautifulSoup
from requests.exceptions import Timeout
from lxml import html
from bot import logging


def request_time(client: Client):
    print("[*] Checking DTU Website for notices now....")
    try:
        r = requests.get(('http://dtu.ac.in/'), timeout=25)
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
    top_link = tree.xpath('//*[@id="tab4"]/div[1]/ul/li[3]/h6/a/@href')[0]
    top_link = top_link.split('.', 1)[1]
    top_link = 'dtu.ac.in' + top_link
    dates = {}
    recorded_dates = {}
    tabs = 1
    while tabs < 9:
        for i in range(1, 8):
            try:
                date_text = tree.xpath(
                    '//*[@id="tab{}"]/div[1]/ul/li[{}]/small/em/i/text()'.format(tabs, i))
                if date_text != []:
                    dates["Date.{}.{}".format(tabs, i)] = date_text
                    if not os.path.exists("recorded_status.json"):
                        recorded_dates["Date.{}.{}".format(
                            tabs, i)] = date_text
                    i = i + 1
                else:
                    i = i + 1
            except Exception as e:
                print(e)
                i = i + 1
        tabs += 1
    if not path.exists("bot/hf/recorded_status.json"):
        data = json.dumps(recorded_dates)
        with open("bot/hf/recorded_status.json", "w+") as f:
            f.write(data)
            print("[*] Recorded Current Status.\n[*] Latest dates: {}".format(data))
            return_values = [404, top_notice, top_link, ' ', ' ']
            return return_values
    else:
        with open("bot/hf/recorded_status.json", "r") as f:
            data = f.read()
        recorded_dates = json.loads(data)
        modified_key = dict_compare(recorded_dates, dates)
        if modified_key != []:
            Tabb = ['.', 'Notices', 'Jobs', 'Tenders', 'Latest News',
                    'Forthcoming Events', 'Press Release', '-', '1st Year Notices']
            temp, tab, link = modified_key[0].split('.')
            try:
                new_notice = tree.xpath(
                    '//*[@id="tab{}"]/div[1]/ul/li[1]/h6/a/text()'.format(tab))[0]
            except IndexError:
                new_notice = tree.xpath(
                    '//*[@id="tab{}"]/div[1]/ul/li[1]/h6/a/font/text()'.format(tab))[0]
            if tab == 2:
                context = tree.xpath(
                    '//*[@id="tab2"]/div[1]/ul/li[1]/h6/a/text()')
                try:
                    vacancy = tree.xpath(
                        '//*[@id="tab2"]/div[1]/ul/li[1]/h6/a/font/text()')
                    new_notice = context[0] + vacancy[0] + context[1]
                except IndexError:
                    new_notice = context[0]
            new_link = tree.xpath(
                '//*[@id="tab{}"]/div[1]/ul/li[1]/h6/a/@href'.format(tab))[0]
            new_link = new_link.split('.', 1)[1]
            new_link = 'dtu.ac.in' + new_link
            Tabb = Tabb[int(tab)]
            return_values = [200, top_notice,
                             top_link, new_notice, new_link, Tabb]
            return return_values
        else:
            return_values = [404, top_notice, top_link, ' ', ' ']
            return return_values


def dict_compare(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    shared_keys = d1_keys.intersection(d2_keys)
    modified = {o: (d1[o], d2[o]) for o in shared_keys if d1[o] != d2[o]}
    return (sorted(list(modified.keys())))
