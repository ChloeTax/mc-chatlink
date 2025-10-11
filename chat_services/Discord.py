import discord
from discord_webhook import DiscordWebhook  # pyright: ignore[reportMissingTypeStubs]

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
        # DiscordBot(discord_token, discord_channel_id, discord_guild_id)
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


class DiscordBot(discord.Client):
    def __init__(
        self, discord_token: str, discord_channel_id: int, discord_guild_id: int
    ):
        raise NotImplementedError
        self.discord_token = discord_token
        self.discord_channel_id = discord_channel_id
        self.discord_guild_id = discord_guild_id

        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(intents=intents)
