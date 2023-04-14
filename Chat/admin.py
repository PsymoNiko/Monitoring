from django.contrib import admin

from Chat.models import Room, Message, Chat

admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Chat)
