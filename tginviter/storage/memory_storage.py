from tginviter.storage.base_storage import BaseStorage


class MemoryStorage(BaseStorage):
    """Store invite tokens inside in-memory dictionary"""

    def __init__(self):
        """Create in-memory dict to store invite tokens"""

        self.storage = {}

    def insert(self, token, max_uses, *, payload=None):
        if payload is not None and type(payload) != str:
            raise TypeError("Only string payloads supported")

        self.storage[str(token)] = [0, max_uses, payload]

    def uses_left(self, token):
        t = self.storage.get(str(token), [0, 0, None])

        return max(0, t[1] - t[0])

    def count_new_use(self, token):
        self.storage[str(token)][0] += 1

    def get_payload(self, token):
        return self.storage.get(str(token), [0, 0, None])[2]
