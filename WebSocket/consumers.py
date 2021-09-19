# chat/consumers.py
from asyncio.windows_events import NULL
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from rest_framework.authtoken.models import Token
from chat_app.models import *


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        # self.room_group_name = 'chat_%s' % self.room_name

        self.token_key = (dict((x.split(
            '=') for x in self.scope['query_string'].decode().split("&")))).get('token', None)

        # Join room group
        # self.room_group_name = 'echo'
        # async_to_sync(self.channel_layer.group_add)(
        #     self.room_group_name,
        #     self.channel_name
        # )
        async_to_sync(self.channel_layer.group_add)(
            self.scope["user"].username,
            self.channel_name
        )

        print('\n\n connected to group: ', self.scope["user"].username, "\n\n")

        # print('\n\n\n connection established \n\n\n')
        # print('\n\n\n', self.scope["user"], '\n\n\n')
        # print('\n\n\n', self.token_key, '\n', self.scope["user"], '\n\n\n')
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        # async_to_sync(self.channel_layer.group_discard)(
        #     self.room_group_name,
        #     self.channel_name
        # )
        async_to_sync(self.channel_layer.group_discard)(
            self.scope["user"].username,
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
        roomId = 'N/A'
        room = None
        room_members = []
        # print(message, text_data_json['is_new_chat'])
        # check if the user is still logged in
        try:
            token = Token.objects.get(key=self.token_key)
        except Token.DoesNotExist:
            print("\n\n\n token does not exist \n\n\n")
            self.disconnect(close_code=None)
            print('disconnected')
            return

        if 'is_new chat' in text_data_json.keys():
            if text_data_json['is_new_chat'] == 'true':
                members = text_data_json['members']
                group_name = text_data_json['group name']
                pass

        # message = text_data_json['message']

        if 'room_id' in text_data_json.keys():
            try:
                room = Room.objects.get(id=text_data_json['room_id'])
                room_members = room.members.all()
                if token.user in room_members:
                    # room = room.serialize(user=token.user, mode='brief')
                    roomId = room.id
                    # print(room)
                else:
                    print("\n\nthe user does not belong in the room\n\n")
                    roomId = 'N/A'
            except:
                print("\n the room does not exist \n")
                roomId = 'N/A'

        for room_member in room_members:
            try:
                print("\n\n\ngroup name:", self.scope["user"].username,
                      ", username: ", Token.objects.get(user=room_member).user.username)
                saved_message = token.user.send_message(
                    room=room, content=message)
                async_to_sync(self.channel_layer.group_send)(
                    Token.objects.get(user=room_member).user.username,
                    {
                        'type': 'chat_message',
                        'message': saved_message.serialize(),
                        # 'username': self.scope["user"].username,
                        'sender': token.user.username,
                        'roomId': roomId
                    }
                )
                print('sent to: ', Token.objects.get(
                    user=room_member).user.username, "\n\n\n")
            except Exception as e:
                print("\n\nError in line 94: ", e, "\n")
                pass

    # Send message to room group
        # async_to_sync(self.channel_layer.group_send)(
        #     self.room_group_name,
        #     {
        #         'type': 'chat_message',
        #         'message': message,
        #         # 'username': self.scope["user"].username,
        #         'sender': token.user.username,
        #         'room': room
        #     }
        # )

    # Receive message from room group

    def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        room = event['roomId']
        # token = event['token']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'roomId': room,
            # 'token': token,
        }))

    # a new message from a new chat room
    def new_room_message(self, event):
        self.send(text_data=json.dumps({
            # if the client is sender and the room_id is new, redirect to the Room
            'type': 'new chat',
            # 'sender': sender,
            # 'message': message,
            # 'room-id': room_id,
        }))

# def login_check(token_key):
