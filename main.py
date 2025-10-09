import dotenv
import os

dotenv.load_dotenv()

#minecraft
RconHost = os.getenv('RconHost')
RconPort = int(os.getenv('RconPort'))
RconPassword = os.getenv('RconPassword')

#discord
webhookURL = os.getenv('webhookURL')
DiscordToken = os.getenv('DiscordToken')
DiscordChannelID = int(os.getenv('DiscordChannelID'))
DiscordGuildID = int(os.getenv('DiscordGuildID'))

#irc
IRCAddress = os.getenv('IRCAddress')
IRCBotNick = os.getenv('IRCBotNick')
IRCBotPass = os.getenv('IRCBotPass')
IRCBotChannel = os.getenv('IRCBotChannel')


from chat_services.console import consoleService
from chat_services.Discord import DiscordService
from chat_services.IRC import IRCService
from chat_services.Minecraft import minecraftService

def main():

    services = [
        consoleService(),
        DiscordService(webhookURL, DiscordToken, DiscordChannelID, DiscordGuildID),
        IRCService(IRCAddress, IRCBotNick, IRCBotPass, IRCBotChannel),
        minecraftService(RconHost, RconPort, RconPassword), 
    ]

    for service1 in services:
        for service2 in services:
            if service1 != service2:
                service1.register(service2)


if __name__ == "__main__":
    main()
