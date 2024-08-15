from django.urls import path
from . import  consumers
print('in routing')

websocket_urlpatterns=[
    path("ws/<str:room_name>/",consumers.ChatConsumer.as_asgi()),
] 