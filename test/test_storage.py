import unittest

from tginviter.storage import BaseStorage, MemoryStorage


class TestMemoryStorage(unittest.TestCase):

    def setUp(self):
        self.storage = MemoryStorage()
        self.token = "123"
        self.payload = {"A": 123, "channel_id": 123, "joinchat_key": "456"}

        self.assertIsInstance(self.storage, BaseStorage)

    def test_token_uses(self):
        uses_left = self.storage.uses_left(self.token)
        self.assertEqual(uses_left, 0)

        self.storage.insert(self.token, max_uses=5, payload=self.payload)

        uses_left = self.storage.uses_left(self.token)
        self.assertEqual(uses_left, 5)

        for _ in range(5):
            self.storage.count_new_use(self.token)

        self.assertEqual(self.storage.uses_left(self.token), 0)

    def test_wrong_dict_payload(self):
        payload = {"A": 123}

        with self.assertRaises(ValueError) as cm:
            self.storage.insert(self.token, max_uses=5, payload=payload)

        e = cm.exception

        self.assertEqual(str(e), "Payload requires channel_id and joinchat_key")

    def test_missing_channel_id_payload(self):
        payload = {"A": 123, "joinchat_key": 123}

        with self.assertRaises(ValueError) as cm:
            self.storage.insert(self.token, max_uses=5, payload=payload)

        e = cm.exception

        self.assertEqual(str(e), "Payload requires channel_id and joinchat_key")

    def test_channel_id_type(self):
        payload = self.payload.copy()
        payload["channel_id"] = "123"

        with self.assertRaises(TypeError) as cm:
            self.storage.insert(self.token, max_uses=5, payload=payload)

        e = cm.exception

        self.assertEqual(str(e), "Value of 'channel_id' should be int")

    def test_joinchat_key_type(self):
        payload = self.payload.copy()
        payload["joinchat_key"] = 123

        with self.assertRaises(TypeError) as cm:
            self.storage.insert(self.token, max_uses=5, payload=payload)

        e = cm.exception

        self.assertEqual(str(e), "Value of 'joinchat_key' should be str")

    def test_missing_joinchat_key_payload(self):
        payload = {"A": 123, "channel_id": 123}

        with self.assertRaises(ValueError) as cm:
            self.storage.insert(self.token, max_uses=5, payload=payload)

        e = cm.exception

        self.assertEqual(str(e), "Payload requires channel_id and joinchat_key")

    def test_dict_payload(self):
        self.storage.insert(self.token, max_uses=5, payload=self.payload)
        self.assertDictEqual(self.storage.get_payload(self.token), self.payload)

    def test_non_dict_payload(self):
        with self.assertRaises(TypeError):
            self.storage.insert(self.token, max_uses=5, payload=[])

        with self.assertRaises(TypeError):
            self.storage.insert(self.token, max_uses=5, payload="qwe")

        with self.assertRaises(TypeError):
            self.storage.insert(self.token, max_uses=5, payload=123)

