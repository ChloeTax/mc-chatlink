import json
import threading
import time

import requests
from discord_webhook import DiscordWebhook  # pyright: ignore[reportMissingTypeStubs]
from websockets.sync.client import connect as ws_connect
from websockets.sync.connection import Connection as ws_connection  # noqa: N813
import chatlink


class DiscordService(chatlink.ChatService):
    def __init__(
        self,
        webhook_url: str,
        discord_token: str,
        discord_channel_id: int,
        discord_guild_id: int,
    ):
        self.webhook_url = webhook_url

        discordbot = DiscordBot(discord_token, discord_channel_id, discord_guild_id)
        discordbot.relay = self._relay
        discordbot.start()
        super().__init__()

    def send(self, message: chatlink.Message):
        if message.author.id == 0 or message.platform != "Minecraft":
            avatar_url = "https://cdn.discordapp.com/avatars/582679756072550410/b1b6bb3577b28fb16e0fe5001e139d4d.webp"
        else:
            avatar_url = f"https://vzge.me/face/256/{message.author.id}"

        DiscordWebhook(
            url=self.webhook_url,
            content=message.content.content,
            username=message.author.name,
            avatar_url=avatar_url,
        ).execute()


class DiscordBot(threading.Thread):
    def __init__(
        self, discord_token: str, discord_channel_id: int, discord_guild_id: int
    ):
        self.discord_token = discord_token
        self.discord_channel_id = discord_channel_id
        self.discord_guild_id = discord_guild_id

        self.ws = ws_connect(
            requests.get(
                "https://discord.com/api/v10/gateway/bot",
                headers={"Authorization": f"Bot {self.discord_token}"},
            ).json()["url"],
            max_size=2147483648,
        )

        self.ws.send(
            json.dumps({
                "op": 2,
                "d": {
                    "token": self.discord_token,
                    "intents": 512,
                    "properties": {},
                },
            })
        )

        self.Heartbeat(
            self.ws, json.loads(self.ws.recv())["d"]["heartbeat_interval"]
        ).start()
        super().__init__()

    def relay(self, message: chatlink.Message):
        pass

    def run(self):
        while True:
            data = json.loads(self.ws.recv())
            if (
                data["t"] == "MESSAGE_CREATE"
                and data["d"]["channel_id"] == str(self.discord_channel_id)
                and "member" in data["d"]
            ):
                if name := data["d"]["member"]["nick"]:
                    pass  # noqa: E701
                elif name := data["d"]["author"]["global_name"]:
                    pass  # noqa: E701
                else:
                    name = data["d"]["author"]["username"]  # noqa: E701

                self.relay(
                    message=chatlink.Message(
                        author=chatlink.MessageAuthor(
                            name=name,
                            id=data["d"]["author"]["id"],
                        ),
                        content=chatlink.MessageContent(content=data["d"]["content"]),
                        platform="Minecraft",
                    )
                )

    class Heartbeat(threading.Thread):
        def __init__(self, ws: ws_connection, interval: int):
            self.ws = ws
            self.interval = interval
            super().__init__()

        def run(self):
            while True:
                time.sleep(self.interval / 1000)
                self.ws.send(json.dumps({"op": 1, "d": None}))
