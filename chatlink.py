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

    def _relay(self, message: Message):
        for sink in self.chatDestinations:
            sink.send(message=message)

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
    id: int | str | None = None
    color: str = "#FFFFFF"
    display: TextComponent | None = None


class TextComponent(BaseModel):
    content: str
    color: None | str = "#FFFFFF"
    bold: bool = False
    italics: bool = False
    underline: bool = False
    spoiler: bool = False
    code: bool = False


class Message(BaseModel):
    author: MessageAuthor
    content: list[TextComponent]
    reply: Message | None = None
    platform: Literal["Console", "Discord", "IRC", "Minecraft"]
