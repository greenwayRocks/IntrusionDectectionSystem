from channels.generic.websocket import WebsocketConsumer

from random import randint

class GraphConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        # compute and send data with "self.send()"
        self.send()
