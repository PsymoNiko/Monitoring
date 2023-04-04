import re

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.db import IntegrityError
from django.db import transaction
from django.contrib.auth.models import User
from django_jalali.serializers.serializerfield import JDateField

from datetime import datetime

from .models import Student, Report, Payment

from ceo.models import Course


class StudentSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    date_of_birth = JDateField(format='%Y-%m-%d')
    phone_number = serializers.CharField(required=True)
    identity_code = serializers.CharField(required=True, write_only=True)
    personality = serializers.ChoiceField(choices=Student.PERSONALITIES, required=True)
    avatar = serializers.ImageField(required=False)

    class Meta:
        model = Student
        fields = ('course', 'first_name', 'last_name', 'date_of_birth', 'phone_number', 'identity_code',
                  'personality', 'avatar')
        read_only_fields = ['id', 'first_name', 'last_name', 'identity_code', 'date_of_birth'
                                                                              'personality']

    def create(self, validated_data: dict) -> Student:
        try:
            with transaction.atomic():
                username = f"student_{validated_data['phone_number']}"
                user = User.objects.create(username=username)

                user.set_password(validated_data['identity_code'])
                user.save()
                student = Student.objects.create(user=user, **validated_data)
                return student
        except IntegrityError:
            raise serializers.ValidationError('Phone number already exists')

    def validate_phone_number(self, value: int or str) -> int:

        if value.startswith('+98') and len(value) == 13 and str(value[1:]).isnumeric():
            value = '0' + str(value[3:])
            return value

        elif value.startswith('09') and len(value) == 11:
            return value

        elif not value.startswith('+98') or not value.startswith('0'):
            raise serializers.ValidationError('Invalid phone number format')
        elif Student.objects.filter(username=value).exists():
            raise serializers.ValidationError("A student with this phone_number is exist")
        return value

    def validate_first_name(self, value: str) -> str:
        persian_regex = '^[\u0600-\u06FF\s]+$'
        if not re.match(persian_regex, value):
            raise serializers.ValidationError("First name must be written in Persian.")
        elif not re.search('[^a-zA-Z]', value):
            raise serializers.ValidationError('First name must not contain signs or numbers.')
        if re.search('[\u06F0-\u06F9]', value):
            raise serializers.ValidationError('First name must not contain Persian numbers.')
        return value

    def validate_last_name(self, value: str) -> str:
        persian_regex = '^[\u0600-\u06FF\s]+$'
        if not re.match(persian_regex, value):
            raise serializers.ValidationError("Last name must be written in Persian.")
        elif not re.search('[^a-zA-Z]', value):
            raise serializers.ValidationError('Last name must not contain signs or numbers.')
        if re.search('[\u06F0-\u06F9]', value):
            raise serializers.ValidationError('Last name must not contain Persian numbers.')
        return value

    def validate_identity_code(self, value: int) -> int:
        if not value.isnumeric():
            raise serializers.ValidationError('Identity code must be numeric.')
        if re.search('[^0-9]', value):
            raise serializers.ValidationError('Identity code must not contain letters or signs.')
        return value

    def validate_avatar(self, value):
        max_size = 11 * 1024 * 1024  # Maximum allowed size in bytes (11 MB)
        if value.size > max_size:
            raise serializers.ValidationError('Avatar size must be less than 11 MB.')
        if not value.name.lower().endswith('.jpeg') and not value.name.lower().endswith('.jpg'):
            raise serializers.ValidationError('Avatar must be in JPEG/JPG format.')
        return value

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get("phone_number", instance.phone_number)
        instance.avatar = validated_data.get("avatar", instance.avatar)
        instance.save()
        return instance


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
        fields = ('username', 'password')


class ReportSerializer(serializers.ModelSerializer):
    report_number = serializers.IntegerField(default=0)
    report_text = serializers.CharField(required=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    created_at = serializers.DateTimeField(read_only=True)
    deadline = serializers.DateTimeField(required=True)
    delayed = serializers.BooleanField(read_only=True)
    study_amount = serializers.CharField(max_length=4, required=True)

    class Meta:
        model = Report
        fields = ('report_number', 'report_text', 'user',
                  'created_at', 'deadline', 'delayed',
                  'study_amount')
        read_only_fields = ['id', 'delayed', 'created_at', 'user']

    def create(self, validated_data):
        user = self.context['request'].user
        student = Student.objects.get(user=user)
        validated_data['user'] = student
        validated_data['created_at'] = datetime.now()
        report = super().create(validated_data)
        return report


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
