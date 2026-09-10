from abc import ABC, abstractmethod


class CommunicationService(ABC):

    @abstractmethod
    async def send_message(
        self,
        recipient: str,
        message: str,
    ) -> None:
        pass