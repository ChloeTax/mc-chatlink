import chatlink
from mcrcon import MCRcon
import threading
import time
import json


class minecraftService(chatlink.chatService):

    def __init__(self, RconHost, RconPort, RconPassword):
        self.mcr = MCRcon(host = RconHost, port = RconPort, password = RconPassword)
        self.mcr.connect()
        super().__init__()

    def _poll(self):
        while True:
            for message in json.loads(self.mcr.command("queryMessages")[:-59]):
                self._relay(message)
            time.sleep(1)
            

    def send(self, message):
        self.mcr.command(f"tellraw @a {self.fromCommonFormat()}")

    def fromCommonFormat(self, message: chatlink.Message):
         
        tellrawCommand = []
        tellrawCommand.append({"text": "[@"})
        tellrawCommand.append({"text": message.author.name,  # "color": color,
                                "clickEvent": {"action": "suggest_command", "value": f"<@{message.author.id}>"},
                                "hoverEvent": {"action": "show_text", "contents": [f"Mention {message.author.name}"]},
                                "color": message.author.color})
        tellrawCommand.append({"text": "] "})
        tellrawCommand.append({"text": message.content})
        fullCommand = "tellraw @a " + json.dumps(tellrawCommand)

        return fullCommand