#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

if __name__ == '__main__':
    __import__("sys").path.append("./../")

from tginviter.storage import BaseStorage, MemoryStorage  # noqa: E402


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


if __name__ == '__main__':
    unittest.main(verbosity=2)
