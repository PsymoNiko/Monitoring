from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    delayed = serializers.BooleanField(read_only=True)

    class Meta:
        model = Report
        fields = '__all__'


from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.db import transaction

from django.contrib.auth.models import User

from .models import Student
from mentor.models import Mentor


class StudentSerializer(serializers.ModelSerializer):
    mentor = serializers.PrimaryKeyRelatedField(queryset=Mentor.objects.all())
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    date_of_birth = serializers.DateField(required=True)
    phone_number = serializers.CharField(required=True)
    identity_code = serializers.CharField(required=True, write_only=True)
    personality = serializers.ChoiceField(choices=Student.PERSONALITIES, required=True)
    avatar = serializers.ImageField(required=False)

    # password = identity_code
    # password = identity_code
    class Meta:
        model = Student
        fields = ('mentor', 'first_name', 'last_name', 'date_of_birth', 'phone_number', 'identity_code',
                  'personality', 'avatar')

    @transaction.atomic()
    def create(self, validated_data):
        username = f"student_{validated_data['phone_number']}"
        user = User.objects.create(username=username)

        user.set_password(validated_data['identity_code'])
        # user.set_password('password')
        user.save()
        student = Student.objects.create(user=user, **validated_data)

        return student

    def validate_phone_number(self, value):
        if Student.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("A student with this phone_number is exist")
        return value


class StudentTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name

        # Add related mentor's name to the token
        token['mentor'] = user.student_profile.mentor.first_name

        return token


class LoginViewAsStudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(allow_blank=True)
    password = serializers.CharField(allow_blank=True, write_only=True)

    class Meta:
        model = Student
        fields = ('username', 'password', 'first_name', 'last_name')
