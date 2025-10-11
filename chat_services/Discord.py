import discord

import chatlink


class DiscordService(chatlink.ChatService):
    def __init__(
        self,
        webhook_url: str,
        discord_token: str,
        discord_channel_id: int,
        discord_guild_id: int,
    ):
        DiscordBot(discord_token, discord_channel_id, discord_guild_id)
        super().__init__()


class DiscordBot(discord.Client):
    def __init__(
        self, discord_token: str, discord_channel_id: int, discord_guild_id: int
    ):
        self.discord_token = discord_token
        self.discord_channel_id = discord_channel_id
        self.discord_guild_id = discord_guild_id

        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(intents=intents)
