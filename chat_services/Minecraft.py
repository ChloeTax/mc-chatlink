import json
import time
from typing import Any

from mcrcon import MCRcon  # pyright: ignore[reportMissingTypeStubs]

import chatlink


class MinecraftService(chatlink.ChatService):
    def __init__(self, rcon_host: str, rcon_port: int, rcon_password: str):
        self.mcr = MCRcon(host=rcon_host, port=rcon_port, password=rcon_password)
        self.mcr.connect()
        super().__init__()

    def _poll(self):
        while True:
            try:
                for message in json.loads(self.mcr.command("queryMessages")[:-59]):  # pyright: ignore[reportUnknownMemberType]
                    print(message)
                    if message[0] == "CHAT":
                        text = self.to_common_format(message[4])

                        print(text)

                        self._relay(
                            message=chatlink.Message(
                                author=chatlink.MessageAuthor(
                                    name=message[2], id=message[1]
                                ),
                                content=text,
                                platform="Minecraft",
                            )
                        )
                    elif message[0] == "JOIN":
                        self._relay(
                            message=chatlink.Message(
                                author=chatlink.MessageAuthor(name=""),
                                content=[
                                    chatlink.TextComponent(
                                        content=f"{message[2]} Joined the game",
                                        color="#ffff00",
                                    )
                                ],
                                platform="Minecraft",
                            )
                        )
                    if message[0] == "LEAVE":
                        self._relay(
                            message=chatlink.Message(
                                author=chatlink.MessageAuthor(name=""),
                                content=[
                                    chatlink.TextComponent(
                                        content=f"{message[2]} Left the game",
                                        color="#ffff00",
                                    )
                                ],
                                platform="Minecraft",
                            )
                        )
            except json.decoder.JSONDecodeError:
                pass
            time.sleep(1)

    def send(self, message: chatlink.Message):
        self.mcr.command(f"tellraw @a {self.from_common_format(message)}")  # pyright: ignore[reportUnknownMemberType]

    def to_common_format(self, message: str):
        def parse(
            component: dict[str, Any], spoiler: bool = False
        ) -> list[chatlink.TextComponent]:
            output: list[chatlink.TextComponent] = []

            if "text" in component:
                output.append(
                    chatlink.TextComponent(
                        content=component["text"],
                        bold="bold" in component,
                        italics="italic" in component,
                        underline="underlined" in component,
                        spoiler=spoiler,
                    ),
                )

            if "hoverEvent" in component:
                output.extend(parse(component["hoverEvent"]["contents"], spoiler=True))
                spoiler = True

            elif "extra" in component:
                for segment in component["extra"]:
                    output.extend(parse(segment, spoiler=spoiler))

            return output

        return parse(json.loads(message))

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
        tellraw_command.append({"text": message.content[0].content})

        return json.dumps(tellraw_command)
