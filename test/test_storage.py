import unittest

from tginviter.storage import BaseStorage, MemoryStorage


class TestMemoryStorage(unittest.TestCase):

    def setUp(self):
        self.storage = MemoryStorage()
        self.token = "123"

        self.assertIsInstance(self.storage, BaseStorage)

    def test_storage(self):
        uses_left = self.storage.uses_left(self.token)
        self.assertEqual(uses_left, 0)

        self.storage.insert(self.token, 5, payload=None)

        uses_left = self.storage.uses_left(self.token)
        self.assertEqual(uses_left, 5)

        for _ in range(5):
            self.storage.count_new_use(self.token)

        self.assertEqual(self.storage.uses_left(self.token), 0)

    def test_default_payload(self):
        self.storage.insert(self.token, 5)
        self.assertIsNone(self.storage.get_payload(self.token))

    def test_null_payload(self):
        self.storage.insert(self.token, 5, payload=None)
        self.assertIsNone(self.storage.get_payload(self.token))

    def test_string_payload(self):
        self.storage.insert(self.token, 5, payload="qwe")
        self.assertEqual(self.storage.get_payload(self.token), "qwe")

    def test_non_string_payload(self):
        with self.assertRaises(TypeError):
            self.storage.insert(self.token, 5, payload=[])

        with self.assertRaises(TypeError):
            self.storage.insert(self.token, 5, payload={})

        with self.assertRaises(TypeError):
            self.storage.insert(self.token, 5, payload=123)
