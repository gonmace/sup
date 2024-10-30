# consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json


class MensajeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'chat_mensajes'
        try:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        except Exception as e:
            print(f"Error connecting: {e}")

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        except Exception as e:
            print(f"Error disconnecting: {e}")

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        try:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )
        except Exception as e:
            print(f"Error sending message: {e}")

    async def chat_message(self, event):
        message = event['message']

        try:
            await self.send(text_data=json.dumps({
                'message': message
            }))
        except Exception as e:
            print(f"Error sending data to WebSocket: {e}")
