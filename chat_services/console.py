import chatlink

class consoleService(chatlink.chatService):

    def __init__(self):
        super().__init__()


    def send(self, message):
        print("sunk", message)




