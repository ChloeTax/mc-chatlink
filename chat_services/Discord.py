import chatlink
import discord


class DiscordService(chatlink.chatService):
    def __init__(self, webhookURL, DiscordToken, DiscordChannelID, DiscordGuildID):
        DiscordBot(DiscordToken, DiscordChannelID, DiscordGuildID)
        super().__init__()


class DiscordBot(discord.Client):
    def __init__(self, DiscordToken, DiscordChannelID, DiscordGuildID):
        self.DiscordToken = DiscordToken
        self.DiscordChannelID = DiscordChannelID
        self.DiscordGuildID = DiscordGuildID

        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(intents=intents)
