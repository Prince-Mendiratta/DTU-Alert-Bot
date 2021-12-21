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
    try:
        top_link = tree.xpath('//*[@id="tab4"]/div[1]/ul/li[1]/h6/a/@href')[0]
        top_link = top_link.split('.', 1)[1]
        top_link = 'dtu.ac.in' + top_link
    except IndexError:
        top_link = 'http://dtu.ac.in/Web/notice/2021/april/file0428.pdf'
    # dates = {}
    # recorded_dates = {}
    # tabs = 1
    # while tabs < 9:
    #     for i in range(1, 8):
    #         try:
    #             date_text = tree.xpath(
    #                 '//*[@id="tab{}"]/div[1]/ul/li[{}]/small/em/i/text()'.format(tabs, i))
    #             if date_text != []:
    #                 dates["Date.{}.{}".format(tabs, i)] = date_text
    #                 if not os.path.exists("recorded_status.json"):
    #                     recorded_dates["Date.{}.{}".format(
    #                         tabs, i)] = date_text
    #                 i = i + 1
    #             else:
    #                 i = i + 1
    #         except Exception as e:
    #             print(e)
    #             i = i + 1
    #     tabs += 1

    tabs = [1,2,3,4,5,8]
    tab_titles = ['Notices', 'Jobs', 'Tenders', 'Latest News', 'Forthcoming Events', '1st Year Notices']
    y = 0
    records = {}
    titles = []
    for x in tabs:
        print("Checking tab - " + str(x))
        tab = tab_titles[y]
        for i in range(1,15):
            print("Checking index - " + str(i))
            try:
                title = notice_title(x,i, tree)
                link = notice_link(x, i, tree)
                notice = {
                    "title": title,
                    "link": link,
                    "tab": tab
                }
                if title != "":
                    titles.append(notice)
            except Exception as e:
                print("No title - " + str(e))
                pass
        records[tab] = titles
        titles = []
        y+=1
    
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
        modified_key = dict_compare(records, previous_records)
        print(modified_key)
        if modified_key != {}:
            # try:
            #     new_notice = tree.xpath(
            #         '//*[@id="tab{}"]/div[1]/ul/li[1]/h6/a/text()'.format(tab))[0]
            # except IndexError:
            #     new_notice = tree.xpath(
            #         '//*[@id="tab{}"]/div[1]/ul/li[1]/h6/a/font/text()'.format(tab))[0]
            # if tab == 2:
            #     context = tree.xpath(
            #         '//*[@id="tab2"]/div[1]/ul/li[1]/h6/a/text()')
            #     try:
            #         vacancy = tree.xpath(
            #             '//*[@id="tab2"]/div[1]/ul/li[1]/h6/a/font/text()')
            #         new_notice = context[0] + vacancy[0] + context[1]
            #     except IndexError:
            #         new_notice = context[0]
            # new_link = tree.xpath(
            #     '//*[@id="tab{}"]/div[1]/ul/li[1]/h6/a/@href'.format(tab))[0]
            # new_link = new_link.split('.', 1)[1]
            # new_link = 'dtu.ac.in' + new_link
            # Tabb = Tabb[int(tab)]
            return_values = [200, top_notice,
                             top_link, modified_key["title"], modified_key["link"], modified_key["tab"]]
            return return_values
        else:
            return_values = [404, top_notice, top_link, ' ', ' ']
            return return_values

def notice_title(x, i, tree):
    try:
        xpath = tree.xpath('//*[@id="tab{}"]/div[1]/ul/li[{}]/h6/a/text()'.format(x,i))
        return xpath[0]
        if top_notice == ' ':
            raise IndexError
    except IndexError:
        try:
            print("got error")
            notice = tree.xpath('//*[@id="tab{}"]/div[1]/ul/li[{}]/h6/a/font/text()'.format(x,i))
            return notice[0]
        except Exception as e:
            print(e)
            return ""
    print("returning 0")
    return ""

def notice_link(x, i, tree):
    try:
        link = tree.xpath('//*[@id="tab{}"]/div[1]/ul/li[{}]/h6/a/@href'.format(x,i))[0]
        link = link.split('.', 1)[1]
        link = 'dtu.ac.in' + link
        return link
    except Exception as e:
        print(e)
        return "http://dtu.ac.in/Web/notice/2021/april/file0428.pdf"


def dict_compare(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    shared_keys = d1_keys.intersection(d2_keys)
    out = {}
    for o in shared_keys:
        for i in d1[o]:
            if i not in d2[o]:
                return i

    return {}