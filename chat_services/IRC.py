from websockets.sync.client import connect

import chatlink


class IRCService(chatlink.ChatService):
    def __init__(
        self,
        irc_address: str,
        irc_bot_nickname: str,
        irc_bot_password: str,
        irc_bot_channel: str,
    ):
        self.irc_address = irc_address
        self.irc_bot_nickname = irc_bot_nickname
        self.irc_bot_password = irc_bot_password
        self.irc_bot_channel = irc_bot_channel
        self.websocket = None
        super().__init__()

    def _poll(self):
        while True:
            if self.websocket:
                message = str(self.websocket.recv())
                if message[:4] == "PING":
                    self.websocket.send("PONG" + message[4:])
                else:
                    parts = message.split(" ")
                    if parts[1] == "PRIVMSG":
                        ircnick = parts[0][1:].split("!")[0]
                        ircmsg = " ".join(parts[3:])[1:]
                        if parts[2] == self.irc_bot_channel:
                            self._relay(
                                message=chatlink.Message(
                                    author=chatlink.MessageAuthor(
                                        name=ircnick, id=ircnick
                                    ),
                                    content=chatlink.MessageContent(content=ircmsg),
                                    platform="IRC",
                                )
                            )
            else:
                self._irc_connect()

    def _irc_connect(self):
        if self.websocket:
            self.websocket.close()
        websocket = connect(self.irc_address)
        websocket.send(
            f"USER {self.irc_bot_nickname} 0 * :An irc bot linking minecraft and irc chat"
        )
        websocket.send(f"NICK {self.irc_bot_nickname}")
        msg = str(websocket.recv())
        websocket.send("PONG" + msg[4:])
        websocket.send(f"ns identify {self.irc_bot_password}")
        websocket.send("MODE +B")
        websocket.send("PART #general")
        websocket.send(f"JOIN {self.irc_bot_channel}")
        self.websocket = websocket

    def send(self, message: chatlink.Message):
        if not self.websocket:
            self.websocket = connect(self.irc_address)

        self.websocket.send(
            f"privmsg {self.irc_bot_channel} :{{{message.author.name}}} {message.content.content}"
        )
