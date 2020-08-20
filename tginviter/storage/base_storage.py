import abc
import uuid


class BaseStorage(abc.ABC):
    """Abstract base class for storing invite link tokens"""

    def generate_token(self):
        """Generate random uuid token"""
        return uuid.uuid4()

    @abc.abstractmethod
    def insert(self, token, max_usages):
        """Insert new invite token to storage"""
        pass

    @abc.abstractmethod
    def uses_left(self, token) -> int:
        """Return amount of unused invitations for token"""
        pass

    @abc.abstractmethod
    def count_new_use(self, token):
        """Increase token usages count"""
        pass
