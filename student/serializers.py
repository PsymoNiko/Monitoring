from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.db import transaction
from django.contrib.auth.models import User

from datetime import datetime

from .models import Student, Report, Payment
from mentor.models import Mentor
from ceo.models import Course


class StudentSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
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
        fields = ('course', 'first_name', 'last_name', 'date_of_birth', 'phone_number', 'identity_code',
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

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get("phone_number", instance.phone_number)
        instance.avatar = validated_data.get("avatar", instance.avatar)
        instance.save()
        return instance

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