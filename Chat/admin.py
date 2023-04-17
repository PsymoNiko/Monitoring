from django.contrib import admin

from Chat.models import Room, Message, Mentorship

admin.site.register(Room)
admin.site.register(Message)
admin.site.register(Mentorship)
