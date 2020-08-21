from telethon import TelegramClient, events, sync
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.contacts import AddContactRequest
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())


class BaseClient:
    def __init__(self, *, session=None, api_id, api_hash):
        """Construct BaseClient with telethon TelegramClient"""

        self.telethon = TelegramClient(session, api_id, api_hash)

    def is_known_contact(self, user):
        """Return true if user's entity in contacts"""

        return user.contact

    def add_contact(self, user):
        """Add user's entity to contact list"""

        result = self.telethon(AddContactRequest(
            id=user.id,
            first_name="first",
            last_name="last",
            phone="123"
        ))

        return result

        pass

    def add_to_channel(self, user, channel):
        result = self.telethon(InviteToChannelRequest(
            channel,
            [user]
        ))

        return result


