from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Message, Chat

User = get_user_model()


class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        messages = Message.objects.filter(chat=self.chat_id)
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        user = data['author']
        author = User.objects.filter(id=user)[0]
        chat = data['chat']
        chat_id = Chat.objects.get(id=chat)
        # if 'smileId' in data:
        #     message = Message.objects.create(
        #         author=author,
        #         chat_id=chat,
        #         smile_id=data['smileId']
        #     )
        # elif 'imgId' in data:
        #     message = Message.objects.create(
        #         author=author,
        #         chat_id=chat,
        #         content=data['message'],
        #         img_id=data['imgId']
        #     )
        # else:
        message = Message.objects.create(
            author=author,
            content=data['message'],
            chat_id=chat
        )
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        content_json = {
            'author': message.author.id,
            'author_image': message.author.image.url,
            'author_fname': message.author.first_name,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }
        if message.img:
            content_json['img'] = message.img.img.url
        if message.smile:
            content_json['smile'] = message.smile.img.url
        return content_json

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = 'chat_%s' % self.chat_id
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))
