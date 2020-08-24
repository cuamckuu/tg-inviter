import abc


class BaseStorage(abc.ABC):
    """Abstract base class for storing invite link tokens"""

    def insert(self, token: str, *, payload: dict, max_uses=1):
        """Insert token to storage. Shoud call super().insert(...)"""

        if type(payload) != dict:
            raise TypeError("Only dict payloads supported")

        if any([x not in payload for x in ["joinchat_key", "channel_id"]]):
            raise ValueError("Payload requires channel_id and joinchat_key")

        if type(payload["channel_id"]) != int:
            raise TypeError("Value of 'channel_id' should be int")

        if type(payload["joinchat_key"]) != str:
            raise TypeError("Value of 'joinchat_key' should be str")

    @abc.abstractmethod
    def uses_left(self, token) -> int:
        """Return amount of unused invitations for token"""
        pass

    @abc.abstractmethod
    def count_new_use(self, token):
        """Increase token usages count"""
        pass

    @abc.abstractmethod
    def get_payload(self, token):
        """Return payload assosciated with given token"""
        pass
