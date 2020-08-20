from collections import defaultdict

from tginviter.storage.base_storage import BaseStorage


class MemoryStorage(BaseStorage):
    """Store invite tokens inside in-memory dictionary"""

    def __init__(self):
        """Create in-memory dict to store invite tokens"""

        self.storage = defaultdict(lambda: [0, 0])

    def insert(self, token, max_uses):
        self.storage[token][1] = max_uses

    def uses_left(self, token):
        return max(0, self.storage[token][1] - self.storage[token][0])

    def count_new_use(self, token):
        self.storage[token][0] += 1
