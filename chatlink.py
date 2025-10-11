from __future__ import annotations

import threading
from typing import Literal

from pydantic import BaseModel


class ChatService:
    def __init__(self):
        self.chatDestinations: list[ChatService] = list()
        self.PollMessages(self)

    def _poll(self):
        pass

    def _relay(self, message: str):
        for sink in self.chatDestinations:
            sink.send(
                Message(
                    author=MessageAuthor(name="Test", id=0),
                    content=MessageContent(content=message),
                    platform="Console",
                )
            )

    def send(self, message: Message):
        pass

    def register(self, chat_destination: ChatService):
        self.chatDestinations.append(chat_destination)

    class PollMessages(threading.Thread):
        def __init__(self, chat_service: ChatService):
            super().__init__(daemon=False)
            self.ChatService = chat_service
            self.run = chat_service._poll
            self.start()


class MessageAuthor(BaseModel):
    name: str
    id: int
    color: str = "#FFFFFF"


class MessageContent(BaseModel):
    content: str


class Message(BaseModel):
    author: MessageAuthor
    content: MessageContent
    platform: Literal["Console", "Discord", "IRC", "Minecraft"]
