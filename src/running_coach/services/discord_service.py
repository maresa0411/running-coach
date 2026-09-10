import discord

from running_coach.services.communication_service import CommunicationService


class DiscordService(CommunicationService):

    def __init__(
        self,
        client: discord.Client,
    ) -> None:
        self.client = client

    async def send_message(
        self,
        recipient: str,
        message: str,
    ) -> None:
        channel_id = int(recipient)

        channel = self.client.get_channel(channel_id)

        if channel is None:
            raise ValueError(
                f"Discord channel not found: {channel_id}"
            )

        await channel.send(message)