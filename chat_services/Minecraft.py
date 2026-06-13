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
                for message in json.loads(self.mcr.command("queryMessages")[:-60]):  # pyright: ignore[reportUnknownMemberType]
                    if message[0] == "CHAT":
                        try:
                            text = self.to_common_format(message[4])
                        except Exception as e:
                            print("exception parsing in minecraft -> common: ", e)
                        else:
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
                                        content=f"{message[2]} joined the game",
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
                                        content=f"{message[2]} left the game",
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

            if isinstance(component, str):
                return [
                    chatlink.TextComponent(
                        content=component,
                        color="#FFFFFF",
                        bold=False,
                        italics=False,
                        underline=False,
                        spoiler=spoiler,
                    )
                ]

            if "text" in component:
                output.append(
                    chatlink.TextComponent(
                        content=component["text"],
                        color=component.get("color", "#FFFFFF"),
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

        if message.author.name:
            if message.platform == "Discord":
                tellraw_command.append({"text": "[@"})
            if message.platform == "Minecraft":
                tellraw_command.append({"text": "<"})
            if message.platform == "IRC":
                tellraw_command.append({"text": "("})

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

        if message.author.name:
            if message.platform == "Discord":
                tellraw_command.append({"text": "] "})
            if message.platform == "Minecraft":
                tellraw_command.append({"text": "> "})
            if message.platform == "IRC":
                tellraw_command.append({"text": ") "})

        for chunk in message.content:
            segment = {
                "text": chunk.content,
                "bold": chunk.bold,
                "italic": chunk.italics,
                "underlined": chunk.underline,
                "color": chunk.color,
            }

            if chunk.spoiler:
                tellraw_command.append({
                    "text": "▌" * len(segment["text"]),  # type: ignore
                    "color": "gray",
                    "hoverEvent": {"action": "show_text", "contents": [segment]},  # type: ignore
                })
            else:
                tellraw_command.append(segment)  # type: ignore

        print(tellraw_command)
        return json.dumps(tellraw_command)
