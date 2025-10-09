from typing import Literal
import threading

class chatService:

    def __init__(self):
        self.chatDestinations = list()
        poll_messages(self)

    def _poll(self):
        pass

    def _relay(self, message: str):
        for sink in self.chatDestinations:
            sink.send(message)

    def fromCommonFormat(self, message: dict) -> any:
        return str(message)

    def toCommonFormat(self, message: any) -> dict:
        return {"message": message}

    def send(self, message: str):
        pass

    def register(self, chatDestination):
        self.chatDestinations.append(chatDestination)


class poll_messages(threading.Thread):
    def __init__(self, chatService: chatService):
        super().__init__(daemon=False)
        self.chatService = chatService
        self.run = chatService._poll
        self.start()



class MessageAuthor:
    def __init__(self, name: str, id: str|int):
        self.name = name
        pass

class MessageContent:
    def __init__(self, content: dict):
        pass

class Message:
    def __init__(self, author: MessageAuthor, content: MessageContent, platform: Literal["Console", "Discord", "IRC", "Minecraft"]):
        self.author = author

