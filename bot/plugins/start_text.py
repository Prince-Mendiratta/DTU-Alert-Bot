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

import threading
from pyrogram import Client, filters
from pyrogram.types import Message
from bot import (
    AUTH_CHANNEL,
    COMMM_AND_PRE_FIX,
    ONLINE_CHECK_START_TEXT,
    START_COMMAND,
    START_OTHER_USERS_TEXT,
    LOG_FILE_ZZGEVC,
    REQUEST_INTERVAL,
    HELP_MEHH,
)
from bot.mongodb.users import add_client_to_db
from .broadcast import get_mod, check_status
from bot import logging
from bot.__banner.banner import bannerTop

banner = bannerTop()
logging.info("\n{}".format(banner))

get_mod(Client)


@Client.on_message(
    filters.command(START_COMMAND, COMMM_AND_PRE_FIX) & ~filters.chat(AUTH_CHANNEL)
)
async def num_start_message(client: Client, message: Message):
    with open("bot/plugins/check.txt", "r") as f:
        last_check = f.read()
    await message.reply_text(START_OTHER_USERS_TEXT.format(last_check), quote=True)
    add_status, total_users = add_client_to_db(
        message.from_user.id, message.from_user.first_name, message.from_user.username
    )
    if add_status == 1:
        await client.send_message(
            chat_id=AUTH_CHANNEL,
            text="🆕 New User!\nTotal: {}\nName: {}\nUsername: @{}".format(
                total_users, message.from_user.first_name, message.from_user.username
            ),
            disable_notification=True,
        )


@Client.on_message(
    filters.command(START_COMMAND, COMMM_AND_PRE_FIX) & filters.chat(AUTH_CHANNEL)
)
async def nimda_start_message(client: Client, message: Message):
    with open("bot/plugins/check.txt", "r") as f:
        last_check = f.read()
    add_status, total_users = add_client_to_db(
        message.from_user.id, message.from_user.first_name, message.from_user.username
    )
    await message.reply_text(
        ONLINE_CHECK_START_TEXT.format(total_users, last_check), quote=True
    )
