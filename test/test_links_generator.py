import unittest

from tginviter import generate_invite_link, get_random_token


class TestLinksGeneration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.bot_name = "test_bot"
        cls.token = get_random_token()

    def test_keywords_param_only(self):
        with self.assertRaises(TypeError):
            generate_invite_link(self.bot_name, self.token, 2)

        generate_invite_link(self.bot_name, max_uses=2)

    def test_proto_exist(self):
        with self.assertRaises(ValueError):
            generate_invite_link(self.bot_name, proto="qwe")

        generate_invite_link(self.bot_name, self.token, proto="tg")
        generate_invite_link(self.bot_name, self.token, proto="http")
        generate_invite_link(self.bot_name, self.token, proto="https")

    def test_return_token(self):
        link, token = generate_invite_link(self.bot_name)

        self.assertTrue(link.endswith(token))

    def test_generate_full_link(self):
        http = f"http://telegram.me/{self.bot_name}?start={self.token}"
        https = f"https://telegram.me/{self.bot_name}?start={self.token}"

        link, _ = generate_invite_link(self.bot_name, self.token, short=False)
        self.assertEqual(link, https)

        link, _ = generate_invite_link(
            self.bot_name, self.token, short=False, proto="https"
        )
        self.assertEqual(link, https)

        link, _ = generate_invite_link(
            self.bot_name, self.token, short=False, proto="http"
        )
        self.assertEqual(link, http)

    def test_generate_short_link(self):
        http = f"http://t.me/{self.bot_name}?start={self.token}"
        https = f"https://t.me/{self.bot_name}?start={self.token}"

        link, _ = generate_invite_link(self.bot_name, self.token)
        self.assertEqual(link, https)

        link, _ = generate_invite_link(self.bot_name, self.token, short=True)
        self.assertEqual(link, https)

        link, _ = generate_invite_link(self.bot_name, self.token, proto="http")
        self.assertEqual(link, http)

        link, _ = generate_invite_link(
            self.bot_name, self.token, proto="https"
        )
        self.assertEqual(link, https)

    def test_random_tokens(self):
        token1 = get_random_token()
        token2 = get_random_token()

        self.assertNotEqual(token1, token2)

    def test_random_links(self):
        https = f"https://t.me/{self.bot_name}?start="

        link1, token1 = generate_invite_link(self.bot_name)
        self.assertTrue(link1.startswith(https))

        link2, token2 = generate_invite_link(self.bot_name)
        self.assertTrue(link1.startswith(https))

        self.assertNotEqual(token1, token2)
        self.assertNotEqual(link1, link2)

    def test_generate_tg_proto_link(self):
        tg = f"tg://resolve?domain={self.bot_name}&start={self.token}"

        link, _ = generate_invite_link(self.bot_name, self.token, proto="tg")
        self.assertEqual(link, tg)

        link, _ = generate_invite_link(
            self.bot_name, self.token, proto="tg", short=True
        )
        self.assertEqual(link, tg)

        link, _ = generate_invite_link(
            self.bot_name, self.token, proto="tg", short=False
        )
        self.assertEqual(link, tg)
