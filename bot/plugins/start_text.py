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
from pyrogram import (
    Client,
    filters
)
from pyrogram.types import (
    Message
)
from bot import (
    AUTH_CHANNEL,
    COMMM_AND_PRE_FIX,
    ONLINE_CHECK_START_TEXT,
    START_COMMAND,
    START_OTHER_USERS_TEXT,
    HELP_MEHH
)
from bot.hf.flifi import uszkhvis_chats_ahndler
from bot.mongodb.users import add_client_to_db
from .broadcast import get_mod, check_status
from bot import logging


last_check = get_mod(Client)

@Client.on_message(
    filters.command(START_COMMAND, COMMM_AND_PRE_FIX) &
    ~uszkhvis_chats_ahndler([AUTH_CHANNEL])
)
async def num_start_message(_, message: Message):
    await message.reply_text(
        START_OTHER_USERS_TEXT.format(last_check),
        quote=True
    )
    add_client_to_db(
        message.from_user.id,
        message.from_user.first_name,
        message.from_user.username
    )


@Client.on_message(
    filters.command(START_COMMAND, COMMM_AND_PRE_FIX) &
    uszkhvis_chats_ahndler([AUTH_CHANNEL])
)
async def nimda_start_message(_, message: Message):
    total_users = add_client_to_db(
        message.from_user.id,
        message.from_user.first_name,
        message.from_user.username
    )
    await message.reply_text(
        ONLINE_CHECK_START_TEXT.format(total_users,last_check),
        quote=True
    )

@Client.on_message(filters.command("help", COMMM_AND_PRE_FIX))
async def get_this_man_some_help(_, message: Message):
    await message.reply_text(
        HELP_MEHH,
        quote=True
    )

@Client.on_message(filters.command("status", COMMM_AND_PRE_FIX))
async def tu_ruk_baba_me_dekhta_na(_, message:Message):
    check_status(message.from_user.id, message.from_user.username)

@Client.on_message(
    filters.command('logs', COMMM_AND_PRE_FIX) &
    uszkhvis_chats_ahndler([AUTH_CHANNEL])
)
async def ye_dekh_kya_hogaya(_, message: Message):
    await message.reply_document(
        "DTU-Alert-Bot.log"
    )