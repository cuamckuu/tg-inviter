import unittest
import os
import time
import asyncio
import uuid
from dotenv import load_dotenv, find_dotenv

from tginviter.bot import PythonTelegramBot
from tginviter.client import TelegramClient
from tginviter.storage import MemoryStorage

load_dotenv(find_dotenv())


TELETHON_API_ID = int(os.environ.get("TELETHON_API_ID"))
TELETHON_API_HASH = os.environ.get("TELETHON_API_HASH")
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TEST_CHANNEL_ID = int(os.environ.get("TEST_CHANNEL_ID"))
TELETHON_SESSION_NAME = os.environ.get("TELETHON_SESSION_NAME")


@unittest.skip("Slow real tests")
class TestTelegramBot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.storage = MemoryStorage()

        cls.token = str(uuid.uuid4())
        payload = {
            "channel_id": -100123456,
            "joinchat_key": "QWERTY"
        }
        cls.storage.insert(cls.token, max_uses=2, payload=payload)

        cls.client = TelegramClient(
            api_id=TELETHON_API_ID,
            api_hash=TELETHON_API_HASH,
            session=TELETHON_SESSION_NAME
        )

        deeplink_handler, job_handler = cls.create_callbacks(
            cls.storage, cls.client
        )

        cls.interval = 0.5
        cls.bot = PythonTelegramBot(
            token=TELEGRAM_BOT_TOKEN,
            deeplink_handler=deeplink_handler,
            job_handler=job_handler,
            interval=cls.interval
        )
        cls.bot_name = cls.bot.get_name()

        cls.job_counter = 0
        cls.no_uses = False

        cls.bot.updater.start_polling()

    @classmethod
    def tearDownClass(cls):
        cls.bot.updater.job_queue.stop()
        cls.bot.updater.stop()

    @classmethod
    def create_callbacks(cls, storage, client):
        def deeplink_handler(update, context):
            if not context.args:
                return

            token = context.args[0]
            if storage.uses_left(token) <= 0:
                cls.no_uses = True
                return

            payload = storage.get_payload(token)

            channel_id = payload["channel_id"]
            user_id = update.effective_user.id

            storage.add_subscription(channel_id, user_id)
            storage.count_new_use(token)

        def job_handler(context):
            cls.job_counter += 1

        return deeplink_handler, job_handler

    def test_deeplink_handler(self):
        async def main():
            await client.send_message("@"+self.bot_name, f"/start {self.token}")
            await asyncio.sleep(0.5)
            await client.send_message("@"+self.bot_name, f"/start {self.token}")

        self.assertEqual(self.storage.storage[self.token][0], 0)

        with self.client.telethon as client:
            client.loop.run_until_complete(main())

        time.sleep(0.5)
        self.assertEqual(self.storage.storage[self.token][0], 2)

    def test_wrong_deeplink(self):
        async def main():
            await client.send_message("@"+self.bot_name, f"/start 12345")

        self.assertFalse(self.no_uses)

        with self.client.telethon as client:
            client.loop.run_until_complete(main())

        time.sleep(0.5)
        self.assertTrue(self.no_uses)


    def test_job_handler(self):
        self.assertTrue(self.job_counter > 0)
