import os

import dotenv

from chat_services.console import ConsoleService
from chat_services.Discord import DiscordService
from chat_services.IRC import IRCService
from chat_services.Minecraft import MinecraftService

dotenv.load_dotenv()

# minecraft
rcon_host: str = os.getenv("rcon_host")  # pyright: ignore[reportAssignmentType]
rcon_port: int = int(os.getenv("rcon_port"))  # pyright: ignore[reportArgumentType, reportAssignmentType]
rcon_password: str = os.getenv("rcon_password")  # pyright: ignore[reportAssignmentType]

# discord
webhook_url: str = os.getenv("webhook_url")  # pyright: ignore[reportAssignmentType]
discord_token: str = os.getenv("discord_token")  # pyright: ignore[reportAssignmentType]
discord_channel_id: int = int(os.getenv("discord_channel_id"))  # pyright: ignore[reportArgumentType, reportAssignmentType]
discord_guild_id: int = int(os.getenv("discord_guild_id"))  # pyright: ignore[reportArgumentType, reportAssignmentType]

# irc
irc_address: str = os.getenv("irc_address")  # pyright: ignore[reportAssignmentType]
irc_bot_nickname: str = os.getenv("irc_bot_nickname")  # pyright: ignore[reportAssignmentType]
irc_bot_password: str = os.getenv("irc_bot_password")  # pyright: ignore[reportAssignmentType]
irc_bot_channel: str = os.getenv("irc_bot_channel")  # pyright: ignore[reportAssignmentType]


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
