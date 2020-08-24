from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.contacts import AddContactRequest
from telethon import TelegramClient, events

class TelethonClient:
    """Telethon based class to ban 'bad' users due to subscription whitelist"""

    def __init__(self, *, session, api_id, api_hash):
        """Construct BaseClient with telethon TelegramClient"""

        self._session = session
        self._api_id = api_id
        self._api_hash = api_hash

        self.telethon = TelegramClient(session, api_id, api_hash)

    def ban_extra_users(self, channel_id, storage):
        with self.telethon as client:
            return client.loop.run_until_complete(
                self.__ban_extra_users(channel_id, storage)
            )

    async def __ban_extra_users(self, channel_id, storage):
        channel = await self.telethon.get_entity(int(channel_id))

        for user in await self.telethon.get_participants(channel):
            if user.bot or user.is_self:
                continue

            is_subscribed = storage.is_subscribed(channel_id, user.id)
            if not is_subscribed:
                await self.telethon.edit_permissions(channel, user, view_messages=False)
                print("Banned: ", user)

    def subscribe_everyone(self, channel_id, storage):
        with self.telethon as client:
            return client.loop.run_until_complete(
                self.__subscribe_everyone(channel_id, storage)
            )

    async def __subscribe_everyone(self, channel_id, storage):
        channel = await self.telethon.get_entity(int(channel_id))

        for user in await self.telethon.get_participants(channel):
            storage.add_subscription(channel_id, user.id)
