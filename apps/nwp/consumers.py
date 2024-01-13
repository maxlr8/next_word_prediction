import json
from channels.generic.websocket import WebsocketConsumer
from .utils import predict_next_word
import json, datetime
from .views import nwp_socket

class NwpConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

        self.send(text_data=json.dumps({
            'type': 'Success',
            'message': 'You are now connected'
        }))

    
    def receive(self,text_data):
        username_str = None
        username = self.scope["user"]
        if(username.is_authenticated):
            username_str = username.username
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        resp = nwp_socket(message,username_str)
        predicted_words = resp.get('data')
        objectId = resp.get('objectId')
        self.send(text_data=json.dumps({
            'type':'chat',
            'message':predicted_words,
            'objectId':objectId
        }))

    def disconnect(self):
        pass
