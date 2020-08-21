import uuid

from tginviter.bot import BaseBot
from tginviter.storage import MemoryStorage


class Inviter:
    """Class to generate and process invite links"""

    def __init__(self, *, bot, storage):
        """Create Inviter with customizable bot, client and srtorage"""

        if not isinstance(bot, BaseBot):
            raise TypeError

        self.__bot = bot
        self.__storage = storage

    def generate_invite_link(
        self,
        token=None,
        *,
        channel=None,
        max_uses=1,
        short=True,
        proto="https"
    ):
        """Generate customizable personal invite link"""

        if proto not in ["http", "https", "tg"]:
            raise ValueError("Use one of ['http', 'https', 'tg'] as proto")

        if not token:
            token = self.get_random_token()

        self.__storage.insert(token, max_uses, channel=channel)

        domain = "telegram.me/"
        if short:
            domain = "t.me/"

        bot_name = self.__bot.get_bot_name()

        params = f"{bot_name}?start={token}"
        if proto == "tg":
            domain = "resolve"
            params = f"?domain={bot_name}&start={token}"

        return f"{proto}://{domain}{params}"

    def generate_random_token(self):
        """Generate random uuid token"""

        return uuid.uuid4()
