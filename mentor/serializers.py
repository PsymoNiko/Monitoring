from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth.models import User
from .models import Mentor

class MentorSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    date_of_birth = serializers.DateField(required=True)
    phone_number = serializers.CharField(required=True)
    identity_code = serializers.CharField(required=True, write_only=True)
    personality = serializers.ChoiceField(choices=Mentor.PERSONALITIES, required=True)
    avatar = serializers.ImageField(required=False)
    # password = identity_code
    class Meta:
        model = Mentor
        fields = ('first_name', 'last_name', 'date_of_birth', 'phone_number', 'identity_code', 'personality', 'avatar')

    def create(self, validated_data):
        username = f"mentor_{validated_data['phone_number']}"
        user = User.objects.create(username=username)

        user.set_password(validated_data['identity_code'])
        user.save()

        mentor = Mentor.objects.create(user=user, **validated_data)
        return mentor

    def validate_phone_number(self, value):
        if Mentor.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("A mentor with this phone_number is exist")
        return value


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # Add any additional fields you want to include in the token
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser
        # ... any other fields you want to include
        return token


class LoginViewAsMentorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(allow_blank=True)
    password = serializers.CharField(allow_blank=True, write_only=True)

    class Meta:
        model = Mentor
        fields = ('username', 'password', 'first_name', 'last_name')