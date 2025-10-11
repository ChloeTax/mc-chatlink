import json
import time

from mcrcon import MCRcon  # pyright: ignore[reportMissingTypeStubs]

import chatlink


class MinecraftService(chatlink.ChatService):
    def __init__(self, rcon_host: str, rcon_port: int, rcon_password: str):
        self.mcr = MCRcon(host=rcon_host, port=rcon_port, password=rcon_password)
        self.mcr.connect()
        super().__init__()

    def _poll(self):
        while True:
            for message in json.loads(self.mcr.command("queryMessages")[:-59]):  # pyright: ignore[reportUnknownMemberType]
                self._relay(
                    message=chatlink.Message(
                        author=chatlink.MessageAuthor(name=message[2], id=message[1]),
                        content=chatlink.MessageContent(content=message[3]),
                        platform="Minecraft",
                    )
                )
            time.sleep(1)

    def send(self, message: chatlink.Message):
        self.mcr.command(f"tellraw @a {self.from_common_format(message)}")  # pyright: ignore[reportUnknownMemberType]

    def from_common_format(self, message: chatlink.Message):
        tellraw_command: list[dict[str, str | dict[str, str | list[str]]]] = []
        tellraw_command.append({"text": "[@"})
        tellraw_command.append({
            "text": message.author.name,
            "clickEvent": {
                "action": "suggest_command",
                "value": f"<@{message.author.id}>",
            },
            "hoverEvent": {
                "action": "show_text",
                "contents": [f"Mention {message.author.name}"],
            },
            "color": message.author.color,
        })
        tellraw_command.append({"text": "] "})
        tellraw_command.append({"text": message.content.content})

        return json.dumps(tellraw_command)
