from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            # Получаем session_id из URL
            self.session_id = self.scope.get('url_route', {}).get('kwargs', {}).get('session_id')

            if not self.session_id:
                raise ValueError("Session ID отсутствует в URL.")

            self.room_group_name = f"chat_{self.session_id}"

            # Добавляем пользователя в группу через Redis
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            # Сообщаем администраторам о новом подключении
            await self.channel_layer.group_send(
                "admins_group",  # Группа для администраторов
                {
                    'type': 'user_connected',
                    'session_id': self.session_id
                }
            )

            # Принимаем соединение клиента
            await self.accept()

        except Exception as e:
            print(f"[ChatConsumer Error] Ошибка при подключении: {e}")
            await self.close()

    async def disconnect(self, close_code):
        try:
            # Удаляем пользователя из группы
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

            # Сообщаем администраторам о разрыве соединения
            await self.channel_layer.group_send(
                "admins_group",
                {
                    'type': 'user_disconnected',
                    'session_id': self.session_id
                }
            )
        except Exception as e:
            print(f"[ChatConsumer Error] Ошибка при отключении: {e}")

    async def receive(self, text_data):
        try:
            # Получаем сообщение пользователя
            text_data_json = json.loads(text_data)
            message = text_data_json.get('message')

            if not message:
                raise ValueError("Поле 'message' отсутствует или пусто.")

            # Отправляем сообщение в группу администраторов
            await self.channel_layer.group_send(
                "admins_group",
                {
                    'type': 'chat_message',
                    'session_id': self.session_id,
                    'message': message
                }
            )

        except (ValueError, json.JSONDecodeError) as e:
            print(f"[ChatConsumer Error] Некорректные данные: {e}")
        except Exception as e:
            print(f"[ChatConsumer Error] Ошибка при получении сообщения: {e}")

    async def chat_message(self, event):
        try:
            # Отправляем сообщение обратно клиенту WebSocket
            await self.send(text_data=json.dumps({
                'event': 'chat_message',
                'message': event.get('message', ''),
                'session_id': event.get('session_id', '')
            }))
        except Exception as e:
            print(f"[ChatConsumer Error] Ошибка при отправке сообщения клиенту: {e}")


class AdminConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            # Подключение администратора к группе
            await self.channel_layer.group_add(
                "admins_group",
                self.channel_name
            )
            await self.accept()

        except Exception as e:
            print(f"[AdminConsumer Error] Ошибка подключения администратора: {e}")
            await self.close()

    async def disconnect(self, close_code):
        try:
            # Удаляем администратора из группы
            await self.channel_layer.group_discard(
                "admins_group",
                self.channel_name
            )
        except Exception as e:
            print(f"[AdminConsumer Error] Ошибка отключения администратора: {e}")

    async def user_connected(self, event):
        try:
            session_id = event.get('session_id', '')
            await self.send(text_data=json.dumps({
                'event': 'user_connected',
                'session_id': session_id
            }))
        except Exception as e:
            print(f"[AdminConsumer Error] Ошибка обработки user_connected: {e}")

    async def user_disconnected(self, event):
        try:
            session_id = event.get('session_id', '')
            await self.send(text_data=json.dumps({
                'event': 'user_disconnected',
                'session_id': session_id
            }))
        except Exception as e:
            print(f"[AdminConsumer Error] Ошибка обработки user_disconnected: {e}")

    async def chat_message(self, event):
        try:
            session_id = event.get('session_id', '')
            message = event.get('message', '')
            await self.send(text_data=json.dumps({
                'event': 'chat_message',
                'session_id': session_id,
                'message': message
            }))
        except Exception as e:
            print(f"[AdminConsumer Error] Ошибка обработки сообщения: {e}")