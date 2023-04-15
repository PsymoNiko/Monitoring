from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Room, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class RoomSerializer(serializers.ModelSerializer):
    online = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'name', 'online']


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'user', 'room', 'content', 'timestamp']
