import unittest
from unittest.mock import MagicMock, patch
import uuid

from tginviter import Inviter
from tginviter.bot import BaseBot


class TestInviter(unittest.TestCase):

    def setUp(self):
        bot = MagicMock(spec=BaseBot)
        bot.get_bot_name = MagicMock(return_value="test_bot")

        client = MagicMock()

        self.inviter = Inviter(
            bot=bot,
            client=client
        )

        self.inviter.get_random_token = MagicMock(return_value=uuid.uuid4())

        self.bot_name = bot.get_bot_name()
        self.token = self.inviter.get_random_token()

    def test_keywords_param_only(self):
        with self.assertRaises(TypeError):
            self.inviter.generate_invite_link(self.token, 2)

        self.inviter.generate_invite_link(self.token, max_uses=2)

    def test_proto_exist(self):
        with self.assertRaises(ValueError):
            self.inviter.generate_invite_link(self.token, proto="qwe")

        self.inviter.generate_invite_link(self.token, proto="tg")
        self.inviter.generate_invite_link(self.token, proto="http")
        self.inviter.generate_invite_link(self.token, proto="https")

    def test_generate_full_link(self):
        http = f"http://telegram.me/{self.bot_name}?start={self.token}"
        https = f"https://telegram.me/{self.bot_name}?start={self.token}"

        link = self.inviter.generate_invite_link(short=False)
        self.assertEqual(link, https)

        link = self.inviter.generate_invite_link(short=False, proto="https")
        self.assertEqual(link, https)

        link = self.inviter.generate_invite_link(short=False, proto="http")
        self.assertEqual(link, http)

    def test_generate_short_link(self):
        http = f"http://t.me/{self.bot_name}?start={self.token}"
        https = f"https://t.me/{self.bot_name}?start={self.token}"

        link = self.inviter.generate_invite_link()
        self.assertEqual(link, https)

        link = self.inviter.generate_invite_link(short=True)
        self.assertEqual(link, https)

        link = self.inviter.generate_invite_link(proto="http")
        self.assertEqual(link, http)

        link = self.inviter.generate_invite_link(proto="https")
        self.assertEqual(link, https)

    def test_custom_token(self):
        https = f"https://t.me/{self.bot_name}?start=123"

        link = self.inviter.generate_invite_link("123")
        self.assertEqual(link, https)

    def test_generate_tg_proto_link(self):
        tg = f"tg://resolve?domain={self.bot_name}&start={self.token}"

        link = self.inviter.generate_invite_link(proto="tg")
        self.assertEqual(link, tg)

        link = self.inviter.generate_invite_link(proto="tg", short=True)
        self.assertEqual(link, tg)

        link = self.inviter.generate_invite_link(proto="tg", short=False)
        self.assertEqual(link, tg)
