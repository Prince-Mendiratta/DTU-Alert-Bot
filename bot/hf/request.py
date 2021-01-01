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
from dotenv import load_dotenv
from lxml import html


def request_time(client: Client):
    print("[*] Checking DTU Website for notices now....")
    try:
        r = requests.get(('http://dtu.ac.in/'), timeout=25)
    except Timeout:
        print("[{}]: The request timed out.".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        sys.exit(1)
    tree = html.fromstring(r.content)
    top_notice = tree.xpath('//*[@id="tab4"]/div[1]/ul/li[1]/h6/a/text()')
    top_link = tree.xpath('//*[@id="tab4"]/div[1]/ul/li[1]/h6/a/@href')[0]
    top_link = top_link.split('.',1)[1]
    top_link = 'dtu.ac.in' + top_link
    dates = {}
    recorded_dates = {}
    for i in range(1,8):
        try:
            date_text = tree.xpath('//*[@id="tab4"]/div[1]/ul/li[{}]/small/em/i/text()'.format(i))
            if date_text != []:
                dates["Date%s" %i] = date_text
                if not path.exists("bot/hf/recorded_status.json"):
                    recorded_dates["Date%s" %i] = date_text
                i = i + 1
            else:
                i = i + 1
        except Exception as e:
            print(e)
            i = i + 1
    if not path.exists("bot/hf/recorded_status.json"):
        data = json.dumps(recorded_dates)
        with open("bot/hf/recorded_status.json", "w+") as f:
            f.write(data)
            print("[*] Recorded Current Status.\n[*] Latest dates: {}".format(data))
    else:
        with open("bot/hf/recorded_status.json", "r") as f:
            data = f.read()
        recorded_dates = json.loads(data)
    
    if recorded_dates != dates:
        return 200, top_notice[0], top_link
    else:
        return 404, top_notice[0], top_link
