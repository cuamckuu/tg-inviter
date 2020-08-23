import abc


class BaseStorage(abc.ABC):
    """Abstract base class for storing invite link tokens"""

    @abc.abstractmethod
    def insert(self, token, max_usages, *, payload=None):
        """Insert token to storage with optional amount of uses and payload"""
        pass

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
