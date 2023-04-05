
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
        read_only_fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'identity_code'
                                                                              'personality']

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

    def update(self, instance, validated_data):
        # Remove the fields from the validated data
        validated_data.pop('id')
        validated_data.pop('first_name')
        validated_data.pop('last_name')
        validated_data.pop('date_of_birth')
        validated_data.pop('identity_code')
        validated_data.pop('personality')

        if 'phone_number' in validated_data:
            instance.phone_number = validated_data['phone_number']
            validated_data.pop('phone_number')

        if 'avatar' in validated_data:
            instance.avatar = validated_data['avatar']
            validated_data.pop('avatar')

        return super().update(instance, validated_data)


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
        fields = ('username', 'password')



