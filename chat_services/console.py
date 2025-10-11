import chatlink


class ConsoleService(chatlink.ChatService):
    def __init__(self):
        super().__init__()

    def send(self, message: chatlink.Message):
        print("sunk", message)
