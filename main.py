import os

import dotenv

from chat_services.console import ConsoleService
from chat_services.Discord import DiscordService
from chat_services.IRC import IRCService
from chat_services.Minecraft import MinecraftService

dotenv.load_dotenv()

# minecraft
rcon_password: str = os.getenv("rcon_password", " rcon password")
rcon_host: str = os.getenv("rcon_host", "127.0.0.1")
rcon_port: int = int(os.getenv("rcon_port", "25575"))

# discord
webhook_url: str = os.getenv("webhook_url", "https://discord.com/api/webhooks/etc")
discord_token: str = os.getenv("discord_token", "token")
discord_channel_id: int = int(os.getenv("discord_channel_id", "123456"))
discord_guild_id: int = int(os.getenv("discord_guild_id", "654321"))

# irc
irc_address: str = os.getenv("irc_address", "wss://irc.example.com:8000")
irc_bot_nickname: str = os.getenv("irc_bot_nickname", "mcrelay")
irc_bot_password: str = os.getenv("irc_bot_password", "hunter1")
irc_bot_channel: str = os.getenv("irc_bot_channel", "mc-chatlink")


def main():
    services = [
        ConsoleService(),
        DiscordService(
            webhook_url, discord_token, discord_channel_id, discord_guild_id
        ),
        IRCService(irc_address, irc_bot_nickname, irc_bot_password, irc_bot_channel),
        MinecraftService(rcon_host, rcon_port, rcon_password),
    ]

    for service1 in services:
        for service2 in services:
            if service1 != service2:
                service1.register(service2)


if __name__ == "__main__":
    main()
