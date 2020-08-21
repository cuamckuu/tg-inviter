import abc


class BaseStorage(abc.ABC):
    """Abstract base class for storing invite link tokens"""

    @abc.abstractmethod
    def insert(self, token, max_usages, *, channel=None):
        """Insert new channel's invite token to storage"""
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
    def get_channel(self, token):
        """Return channel assosciated with given token"""
        pass
