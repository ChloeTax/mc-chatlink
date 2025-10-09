from websockets.sync.client import connect
import chatlink



class IRCService(chatlink.chatService):

    def __init__(self, IRCAddress, IRCBotNick, IRCBotPass, IRCBotChannel):
        self.IRCAddress = IRCAddress 
        self.IRCBotNick = IRCBotNick 
        self.IRCBotPass = IRCBotPass 
        self.IRCBotChannel = IRCBotChannel
        self.websocket = None
        super().__init__()

    def _poll(self):
        while True:
            if not self.websocket:
                self._IRCConnect()
            message = self.websocket.recv()
            if message[:4] == "PING":
                self.websocket.send("PONG" + message[4:])
            else:
                parts = message.split(" ")
                if parts[1] == "PRIVMSG":
                    ircnick = parts[0][1:].split("!")[0]
                    ircmsg = " ".join(parts[3:])[1:]
                    if parts[2] == self.IRCBotChannel:
                        self._relay(f"{ircnick}: {ircmsg}")

    def _IRCConnect(self):
        if self.websocket:
            self.websocket.close()
        websocket = connect(self.IRCAddress)
        websocket.send(f"USER {self.IRCBotNick} 0 * :An irc bot linking minecraft and irc chat")
        websocket.send(f"NICK {self.IRCBotNick}")
        msg = websocket.recv()
        websocket.send("PONG" + msg[4:])
        websocket.send(f"ns identify {self.IRCBotPass}")
        websocket.send(f"MODE +B")
        websocket.send(f"PART #general")
        websocket.send(f"JOIN {self.IRCBotChannel}")
        self.websocket = websocket

    def send(self, message):
        if not self.websocket:
            self.websocket = connect(self.IRCAddress)
            
        self.websocket.send(f"privmsg {self.IRCBotChannel} :{self.fromCommonFormat(message)}")
