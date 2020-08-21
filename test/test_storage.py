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

        self.storage.insert(self.token, 5, channel=None)

        uses_left = self.storage.uses_left(self.token)
        self.assertEqual(uses_left, 5)

        for _ in range(5):
            self.storage.count_new_use(self.token)

        self.assertEqual(self.storage.uses_left(self.token), 0)

    def test_channel(self):
        self.storage.insert(self.token, 5, channel=None)
        self.assertIsNone(self.storage.get_channel(self.token))

        self.storage.insert(self.token, 5, channel="qwe")
        self.assertEqual(self.storage.get_channel(self.token), "qwe")
