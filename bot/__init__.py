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

""" credentials """

import logging
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
from bot.get_env import get_env

load_dotenv("config.env")

# The Telegram API things.
# Get these values from my.telegram.org.
API_HASH = get_env("API_HASH", should_prompt=True)
API_ID = get_env("API_ID", should_prompt=True)
# get a token from @BotFather.
TG_BOT_TOKEN = get_env("TG_BOT_TOKEN", should_prompt=True)
# array to store the channel ID of the admin.
AUTH_CHANNEL = int(get_env("AUTH_CHANNEL", "-100", should_prompt=True))
# MongoDB Database for the bot to operate
MONGO_URL = get_env("MONGO_URL", should_prompt=True)
TG_BOT_WORKERS = int(get_env("TG_BOT_WORKERS", "4"))
# SHA Secret for Webhook event
SHA_SECRET = get_env("SHA_SECRET", "mysecret")
# Webhook address
WEBHOOK_ADDRESS = get_env("WEBHOOK_ADDRESS", "https://google.com")
# Use Webhooks
WEBHOOK_INTEGRATION = bool(get_env("WEBHOOK_INTEGRATION", False))
#
COMMM_AND_PRE_FIX = get_env("COMMM_AND_PRE_FIX", "/")
# start command
START_COMMAND = get_env("START_COMMAND", "start")
# /start message when other users start your bot
START_OTHER_USERS_TEXT = get_env(
    "START_OTHER_USERS_TEXT",
    (
        "👋 Hey! Welcome to <i>DTU Alert Bot</i>.\n\n"
        "🔔 You are <b>subscribed for notifications</b>. In case of any new notice on DTU Website, you'll recieve an alert and the notice here itself. <i>Send</i> /help <i>for more info.</i>\n\n"
        "⚠️ Please make sure the bot is <b>unmuted</b> and notifications are allowed for the app.\n\n"
        "😌 DTU Notice Alert Bot is now available on <b>WhatsApp</b> as well! You can join the group using this link - https://bit.ly/DTUAlertBotWhatsApp .\n\n"
        "😄 This bot was developed and hosted by <b>Prince Mendiratta</b> (@anubisxx). This is an open source project available on https://bit.ly/32snhEw.\n\n"
        "🔱 <b>Last check status-</b>\n{}"
    ),
)
# /help message
HELP_MEHH = get_env(
    "HELP_MEHH",
    (
        "⭕️ This project had been developed as a personal utility bot, which was later modified to be used by all and then submitted as part of <i>Innovative Project Work</i>, whose report can be found on <a href='https://github.com/Prince-Mendiratta/DTU-Alert-Bot/blob/master/Project_Report.pdf'>Github</a>.\n\n"
        "😲 This bot creates a full record of the notices on the website and cross-checks with previous records to determine if the site has been updated and <b>instantly</b> sends you a notification to alert you.\n\n"
        "⚠️ <b>Please unmute the bot and allow notifications for the app.</b>\n"
        "Send /status to check if the alerts work properly!\n\n"
        "😢 If you want to unsubscribe, simple block the bot\n\n."
        "🫂 To <b>reach out to me</b> for feedbacks / complaints / suggestions, you can find my profiles and contact details using the /creator command."
    ),
)
# check online status of your bot
ONLINE_CHECK_START_TEXT = get_env(
    "ONLINE_CHECK_START_TEXT",
    (
        "👾 I am online, <b>master</b>\n\n"
        "<b>Current Users</b> - {}\n\n"
        "<b>Last check status</b> - \n{}"
    ),
)
# creator text
CREATOR = get_env(
    'CREATOR',
    (
        "🌀 Hello, this bot has been developed and maintained by <b>Prince Mendiratta</b>, a sophomore at <i>Delhi Technological University</i>.\n\n"
        "♣️ A zestful learner with an upcoming Bachelors Degree in <i>Computer Engineering</i>, being particularly adept at working with Python, NodeJS, JavaScript, C++ , full stack web development, I love automating things.\n\n"
        "💠 Do bots fascinate you as well? Check out my recent project, <a href='https://mybotsapp.com'>BotsApp</a>, where you can create your <b>personal userbot on WhatsApp</b>, absolutely free of cost and with <i>zero technical knowledge</i> required!\n\n"
        "⭕️ Want to get premium apps for free? Check out my <a href='https://t.me/allapkforfree'>Telegram Channel</a> and <a href='https://moddingunited.xyz'>website</a>, dedicated to providing <b>safe and trusted modded application</b>, used by tens of thousands of people daily! \n\n"
        "🔅 Have any suggestions / feedback / complaints or just wanna hangout? Don't hesitate to <b>reach out</b> to me on any of these platforms.\n"
        "🔗 <a href='https://t.me/anubisxx'>Telegram</a> | <a href='https://www.linkedin.com/in/prince-mendiratta'>LinkedIn</a> | <a href='https://api.whatsapp.com/send/?phone=%2B917838204238&text=Hello+There!&app_absent=0'>WhatsApp</a> | <a href='https://github.com/Prince-Mendiratta'>Github</a>"
    )
)
# Interval between each check
REQUEST_INTERVAL = get_env("REQUEST_INTERVAL", 20)
# path to store LOG files
LOG_FILE_ZZGEVC = get_env("LOG_FILE_ZZGEVC", "bot/DTUAlertBot.log")
# Ensure Timezone is IST
TZ = get_env("TZ", "Asia/Kolkata")

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        RotatingFileHandler(
            LOG_FILE_ZZGEVC, maxBytes=50000000, backupCount=10),
        logging.StreamHandler(),
    ],
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    """ get a Logger object """
    return logging.getLogger(name)
