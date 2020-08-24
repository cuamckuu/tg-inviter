import json

from tginviter.storage.base_storage import BaseStorage


class MemoryStorage(BaseStorage):
    """Store invite tokens inside in-memory dictionary"""

    def __init__(self):
        """Create in-memory dict to store invite tokens"""

        self.storage = {}
        self.whitelist = {}

    def insert(self, token, *, payload, max_uses=1):
        super().insert(token, payload=payload, max_uses=max_uses)

        payload_str = None
        if payload:
            payload_str = json.dumps(payload)

        self.storage[str(token)] = [0, max_uses, payload_str]
        self.whitelist[payload["channel_id"]] = []

    def uses_left(self, token):
        t = self.storage.get(str(token), [0, 0, None])

        return max(0, t[1] - t[0])

    def count_new_use(self, token):
        self.storage[str(token)][0] += 1

    def get_payload(self, token):
        payload = self.storage.get(str(token), [0, 0, None])[2]

        if payload:
            return json.loads(payload)

        return None

    def get_channel_ids(self):
        return set(self.whitelist.keys())

    def is_subscribed(self, channel_id, user_id):
        return (user_id in self.whitelist.get(channel_id, []))

    def add_subscription(self, channel_id, user_id):
        if channel_id not in self.whitelist:
            self.whitelist[channel_id] = []

        return self.whitelist[channel_id].append(user_id)
