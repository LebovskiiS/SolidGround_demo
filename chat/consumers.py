from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import ChatSession, ChatMessage
from django.contrib.auth.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.group_name = f"chat_{self.session_id}"

        # Добавляем пользователя в группу
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Удаляем пользователя из группы
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_id = data['sender_id']

        sender = User.objects.get(id=sender_id)
        session = ChatSession.objects.get(id=self.session_id)

        # Сохраняем сообщение в базе данных
        ChatMessage.objects.create(session=session, sender=sender, text=message)

        # Отправляем сообщение всем членам группы
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender": sender.username
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # Отправляем сообщение обратно клиенту
        await self.send(text_data=json.dumps({
            "message": message,
            "sender": sender
        }))
