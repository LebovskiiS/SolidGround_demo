from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Connect method for users. Establish connection and send connection event
        to admin group.
        """
        try:
            # Retrieve session ID or user ID from URL
            self.session_id = self.scope.get('url_route', {}).get('kwargs', {}).get('session_id')
            self.user_id = self.scope.get('url_route', {}).get('kwargs', {}).get('user_id')

            # Use either session_id or user_id as the identifier
            self.identifier = self.session_id or str(self.user_id)

            if not self.identifier:
                raise ValueError("Identifier (session_id or user_id) is missing in URL.")

            self.room_group_name = f"chat_{self.identifier}"

            # Add user to their specific WebSocket group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            # Notify admins about a new user connection
            await self.channel_layer.group_send(
                "admins_group",
                {
                    'type': 'user_connected',
                    'identifier': self.identifier,
                    'user_id': self.user_id
                }
            )

            # Accept WebSocket connection
            await self.accept()
        except Exception as e:
            print(f"[ChatConsumer Error] Connection error: {e}")
            await self.close()

    async def disconnect(self, close_code):
        """
        Disconnect method. Remove user from their WebSocket group and notify
        admins about the disconnection.
        """
        try:
            # Remove user from their WebSocket group
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

            # Notify admins about user disconnection
            await self.channel_layer.group_send(
                "admins_group",
                {
                    'type': 'user_disconnected',
                    'identifier': self.identifier,
                    'user_id': self.user_id
                }
            )
        except Exception as e:
            print(f"[ChatConsumer Error] Disconnection error: {e}")

    async def receive(self, text_data):
        """
        Receive method used to handle messages sent from the client
        and forward them to the admin group.
        """
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json.get('message')

            if not message:
                raise ValueError("Field 'message' is missing or empty.")

            # Forward message to the admin group
            await self.channel_layer.group_send(
                "admins_group",
                {
                    'type': 'chat_message',
                    'identifier': self.identifier,
                    'user_id': self.user_id,
                    'message': message
                }
            )
        except (ValueError, json.JSONDecodeError) as e:
            print(f"[ChatConsumer Error] Invalid data: {e}")
        except Exception as e:
            print(f"[ChatConsumer Error] Error receiving message: {e}")

    async def chat_message(self, event):
        """
        Handle chat messages and echo them back to the sender.
        Also handle messages from admins.
        """
        try:
            # Check if the message is from an admin
            from_admin = event.get('from_admin', False)

            await self.send(text_data=json.dumps({
                'event': 'chat_message',
                'message': event.get('message', ''),
                'identifier': event.get('identifier', ''),
                'user_id': event.get('user_id', ''),
                'from_admin': from_admin
            }))

            # If this is a message from a user (not an admin), store it in the database
            if not from_admin and self.user_id:
                # This would be done asynchronously in a real application
                # For simplicity, we're not implementing the database storage here
                pass

        except Exception as e:
            print(f"[ChatConsumer Error] Error sending message to client: {e}")


class AdminConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Connect method for admins. Add them to the admin group.
        Authentication verification is disabled - anyone can connect as admin.
        """
        try:
            # Add admin to the "admins_group" without any verification
            await self.channel_layer.group_add(
                "admins_group",
                self.channel_name
            )
            await self.accept()
            print("[AdminConsumer] Admin connection accepted without verification")
        except Exception as e:
            print(f"[AdminConsumer Error] Admin connection error: {e}")
            await self.close()

    async def disconnect(self, close_code):
        """
        Disconnect method for admins. Remove them from the admin group.
        """
        try:
            await self.channel_layer.group_discard(
                "admins_group",
                self.channel_name
            )
        except Exception as e:
            print(f"[AdminConsumer Error] Admin disconnection error: {e}")

    async def user_connected(self, event):
        """
        Notify admin about a user connection.
        """
        try:
            identifier = event.get('identifier', '')
            user_id = event.get('user_id', '')
            await self.send(text_data=json.dumps({
                'event': 'user_connected',
                'identifier': identifier,
                'user_id': user_id
            }))
        except Exception as e:
            print(f"[AdminConsumer Error] Error processing user_connected: {e}")

    async def user_disconnected(self, event):
        """
        Notify admin about a user disconnection.
        """
        try:
            identifier = event.get('identifier', '')
            user_id = event.get('user_id', '')
            await self.send(text_data=json.dumps({
                'event': 'user_disconnected',
                'identifier': identifier,
                'user_id': user_id
            }))
        except Exception as e:
            print(f"[AdminConsumer Error] Error processing user_disconnected: {e}")

    async def chat_message(self, event):

        try:
            await self.send(text_data=json.dumps({
                'event': 'chat_message',
                'identifier': event.get('identifier', ''),
                'user_id': event.get('user_id', ''),
                'message': event.get('message', '')
            }))
        except Exception as e:
            print(f"[AdminConsumer Error] Error processing message: {e}")

    async def receive(self, text_data):
        """
        Receive method for admins to respond to specific users.
        """
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json.get('message')
            user_id = text_data_json.get('user_id')

            if not message:
                raise ValueError("Field 'message' is missing or empty.")
            if not user_id:
                raise ValueError("Field 'user_id' is missing or empty.")

            # Forward message to the specific user's group
            await self.channel_layer.group_send(
                f"chat_{user_id}",
                {
                    'type': 'chat_message',
                    'identifier': user_id,
                    'user_id': user_id,
                    'message': message,
                    'from_admin': True
                }
            )
        except (ValueError, json.JSONDecodeError) as e:
            print(f"[AdminConsumer Error] Invalid data: {e}")
        except Exception as e:
            print(f"[AdminConsumer Error] Error sending message to user: {e}")
