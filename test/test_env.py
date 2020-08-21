import unittest
import os


class TestEnvVariables(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from dotenv import load_dotenv, find_dotenv
        load_dotenv(find_dotenv())

    def test_telethon_api_keys(self):
        TELETHON_API_ID = os.environ.get("TELETHON_API_ID")
        TELETHON_API_HASH = os.environ.get("TELETHON_API_HASH")

        self.assertIsNotNone(TELETHON_API_ID)
        self.assertIsNotNone(TELETHON_API_HASH)

    def test_telegram_bot_token(self):
        TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

        self.assertIsNotNone(TELEGRAM_BOT_TOKEN)
