# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from rest_framework.authtoken.models import Token
from chat_app.models import *

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        # self.room_group_name = 'chat_%s' % self.room_name

        self.room_group_name = 'echo'
        self.token_key = (dict((x.split('=') for x in self.scope['query_string'].decode().split("&")))).get('token', None)

        # # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        async_to_sync(self.channel_layer.group_add)(
            self.scope["user"].username,
            self.channel_name
        )


        # print('\n\n\n connection established \n\n\n')
        # print('\n\n\n', self.scope["user"], '\n\n\n')
        print('\n\n\n', self.token_key, '\n', self.scope["user"], '\n\n\n')
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        self.send(text_data=json.dumps({
            'disconnected': 'disconnected',
        }))
        print('\n\n\n', 'disconnected', '\n\n\n')
        self.close()

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        try:
            token = Token.objects.get(key=self.token_key)
        except Token.DoesNotExist:
            self.disconnect(close_code=None)
            print('disconnected')
            return
     
    # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                # 'username': self.scope["user"].username,
                'username': token.user.username
            }
        )
  

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        username = event['username']
        # token = event['token']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            # 'token': token,
        }))

# def login_check(token_key):
