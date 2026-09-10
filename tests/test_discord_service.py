from unittest.mock import AsyncMock, Mock

import pytest

from running_coach.services.discord_service import DiscordService


@pytest.mark.asyncio
async def test_send_message_sends_message_to_channel() -> None:
    channel = Mock()
    channel.send = AsyncMock()

    client = Mock()
    client.get_channel.return_value = channel

    service = DiscordService(client=client)

    await service.send_message(
        recipient="123456789",
        message="Test feedback",
    )

    client.get_channel.assert_called_once_with(123456789)
    channel.send.assert_awaited_once_with("Test feedback")

@pytest.mark.asyncio
async def test_send_message_raises_error_when_channel_not_found() -> None:
    client = Mock()
    client.get_channel.return_value = None

    service = DiscordService(client=client)

    with pytest.raises(
        ValueError,
        match="Discord channel not found: 123456789",
    ):
        await service.send_message(
            recipient="123456789",
            message="Test feedback",
        )

