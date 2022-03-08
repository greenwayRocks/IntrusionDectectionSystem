from channels.generic.websocket import WebsocketConsumer

from random import randint
import json

class attackNotify(WebsocketConsumer):
    def connect(self):
        self.accept()

        # compute and send data with "self.send()"
        for i in range(1000):
            self.send(json.dumps({ 'value': randint(-100, 100) }))
