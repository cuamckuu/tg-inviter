#!/usr/bin/env python
#-*- coding: utf-8 -*-

import unittest
import uuid

if __name__ == '__main__':
    __import__("sys").path.append("./../")

from tginviter.storage import BaseStorage, MemoryStorage


class TestMemoryStorage(unittest.TestCase):

    def setUp(self):
        self.storage = MemoryStorage()

    def test_storage(self):
        token = self.storage.generate_token()

        self.assertEqual(self.storage.uses_left(token), 0)

        self.storage.insert(token, 5)

        self.assertEqual(self.storage.uses_left(token), 5)

        for _ in range(5):
            self.storage.count_new_use(token)

        self.assertEqual(self.storage.uses_left(token), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
