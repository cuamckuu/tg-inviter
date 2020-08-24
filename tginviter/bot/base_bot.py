import abc


class BaseBot(abc.ABC):
    @abc.abstractmethod
    def __init__(self, *, token, deeplink_callback, joinchat_handler):
        """Abstract class for bot libraries that should use given handlers"""
        pass

    @abc.abstractmethod
    def start(self):
        """Start blocking bot thread"""
        pass

    @abc.abstractmethod
    def get_name(self):
        """Return bot's username from API's getMe()"""
        pass
