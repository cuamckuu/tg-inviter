from tginviter.storage.base_storage import BaseStorage


class MemoryStorage(BaseStorage):
    """Store invite tokens inside in-memory dictionary"""

    def __init__(self):
        """Create in-memory dict to store invite tokens"""

        self.storage = {}

    def insert(self, token, max_uses, *, channel=None):
        self.storage[token] = [0, max_uses, channel]

    def uses_left(self, token):
        t = self.storage.get(token, [0, 0, None])

        return max(0, t[1] - t[0])

    def count_new_use(self, token):
        self.storage[token][0] += 1

    def get_channel(self, token):
        return self.storage.get(token, [0, 0, None])[2]
