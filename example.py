#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from tginviter import generate_invite_link, generate_joinchat_link
from tginviter.storage import MemoryStorage
from tginviter.client import TelethonClient
from tginviter.bot import PythonTelegramBot


# Text to use in bot's messages
TEXT_ERROR = (
    "*Ошибка*\n\n"
    "Ссылка активации недействительна."
)
TEXT_SUCCESS = (
    "*Подписка активирована*\n\n"
    "Для перехода на канал используйте кнопку ниже."
)
TEXT_JOINCHAT_BUTTON = "Перейти на канал"

TEXT_ERROR = (
    "*Error*\n\n"
    "Invite token has been already used."
)
TEXT_SUCCESS = (
    "*Succes*\n\n"
    "Use button below to join secret channel."
)
TEXT_JOINCHAT_BUTTON = "Join channel"


# Secrets from .env file
TELETHON_API_ID = int(os.environ.get("TELETHON_API_ID"))
TELETHON_API_HASH = os.environ.get("TELETHON_API_HASH")
TELETHON_SESSION_NAME = os.environ.get("TELETHON_SESSION_NAME")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TEST_CHANNEL_ID = int(os.environ.get("TEST_CHANNEL_ID"))
TEST_JOINCHAT_KEY = os.environ.get("TEST_JOINCHAT_KEY")


def create_callbacks(storage, client):
    def deeplink_handler(update, context):
        if not context.args:
            return

        token = context.args[0]
        if storage.uses_left(token) <= 0:
            if update.message:
                update.message.reply_text(TEXT_ERROR, parse_mode="Markdown")
            return

        payload = storage.get_payload(token)

        joinchat_key = payload["joinchat_key"]
        keyboard = InlineKeyboardMarkup.from_button(
            InlineKeyboardButton(
                text=TEXT_JOINCHAT_BUTTON,
                url=generate_joinchat_link(joinchat_key)
            )
        )

        channel_id = payload["channel_id"]
        user_id = update.effective_user.id

        storage.add_subscription(channel_id, user_id)
        storage.count_new_use(token)

        time.sleep(2)

        if update.message:
            update.message.reply_text(
                TEXT_SUCCESS,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )

    job_num = 0
    def job_handler(context):
        nonlocal job_num
        job_num += 1

        if job_num == 1:
            for channel_id in storage.get_channel_ids():
                client.subscribe_everyone(channel_id, storage)
        else:
            for channel_id in storage.get_channel_ids():
                client.ban_extra_users(channel_id, storage)

    return deeplink_handler, job_handler


def main():
    storage = MemoryStorage()

    client = TelethonClient(
        api_id=TELETHON_API_ID,
        api_hash=TELETHON_API_HASH,
        session=TELETHON_SESSION_NAME
    )

    deeplink_handler, job_handler = create_callbacks(storage, client)
    bot = PythonTelegramBot(
        token=TELEGRAM_BOT_TOKEN,
        deeplink_handler=deeplink_handler,
        job_handler=job_handler,
        interval=4
    )
    bot_name = bot.get_name()

    payload = {
        "channel_id": TEST_CHANNEL_ID,
        "joinchat_key": TEST_JOINCHAT_KEY,
    }

    link, token = generate_invite_link(bot_name)
    storage.insert(token, max_uses=1, payload=payload)
    print(link)

    link, token = generate_invite_link(bot_name, short=False)
    storage.insert(token, max_uses=1, payload=payload)
    print(link)

    link, token = generate_invite_link(bot_name, proto="tg")
    storage.insert(token, max_uses=1, payload=payload)
    print(link)

    bot.start()


if __name__ == '__main__':
    main()

