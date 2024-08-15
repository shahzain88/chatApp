import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from .models import Room , Message 




class ChatConsumer(AsyncWebsocketConsumer):
    print('in consumer') 

    async def connect(self):
        print('in connect')
        self.room_name=self.scope['url_route']['kwargs']['room_name']
        self.room_group_name= 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()


    async def disconnect(self,code="message sent"):
        print('in dicconnect')

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print('in receive')

        data=json.loads(text_data)
        message = str(data["message"])
        username = str(data["username"])
        room = str(data["room"])

        await self.save_message(username,room,message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type":"chat_message",
                "message":message,
                "username":username,
                "room":room,

            }
        )
    async def chat_message(self, event):
        print('in chat message')
    
        message = str(event["message"])
        username = str(event["username"])
        room = str(event["room"])


        await self.send(text_data=json.dumps({
            
                "message":message,
                "username":username,
                "room":room,
        }))

    @sync_to_async
    def save_message(self, username,room,message):
        user=User.objects.get(username=username)
        room=Room.objects.get(slug=room)

        Message.objects.create(user=user,room=room,content=message)
        print("msg saved")