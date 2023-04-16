import re
from datetime import datetime, timedelta

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.shortcuts import reverse
from django.db import IntegrityError
from django.db import transaction
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

from .models import Student, Report, Payment, AdminPayment
from ceo.models import Course
from monitoring.utils import *


class StudentSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='admin-students-details',
        lookup_field='pk'
    )

    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    course_name = serializers.ReadOnlyField(source='course.name')
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    date_of_birth = JalaliDateField()
    jalali_date_of_birth = serializers.CharField(required=False, allow_blank=True, max_length=10)
    phone_number = serializers.CharField(required=True)
    identity_code = serializers.CharField(required=True, write_only=True)
    personality = serializers.ChoiceField(choices=Student.PERSONALITIES, required=True)
    avatar = serializers.ImageField(required=False)

    def create(self, validated_data: dict) -> Student:
        try:
            with transaction.atomic():
                username = f"student_{validated_data['phone_number']}"
                user = User.objects.create(username=username)

                user.set_password(validated_data['identity_code'])
                user.save()
                jalali_date = validated_data.pop('jalali_date_of_birth', None)
                if not jalali_date:
                    raise serializers.ValidationError({
                        "jalali_date_of_birth": "This field is required."
                    })
                validated_data['date_of_birth'] = convert_jalali_to_gregorian(jalali_date)

                student = Student.objects.create(user=user, **validated_data)
                return student
        except IntegrityError:
            raise serializers.ValidationError('Phone number already exists')

    class Meta:
        model = Student
        fields = (
            'id', 'course', 'course_name', 'url', 'first_name', 'last_name', 'jalali_date_of_birth', 'date_of_birth',
            'phone_number', 'identity_code', 'personality', 'avatar')
        read_only_fields = ['id', 'first_name', 'url', 'last_name', 'identity_code', 'jalali_date_of_birth',
                            'date_of_birth',
                            'personality']

    def validate_phone_number(self, value: str) -> str:

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

    def validate_identity_code(self, value: str) -> str:
        if not value.isnumeric():
            raise serializers.ValidationError('Identity code must be numeric.')
        if re.search('[^0-9]', value):
            raise serializers.ValidationError('Identity code must not contain letters or signs.')
        return value

    def validate_avatar(self, value):
        max_size = 11 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError('Avatar size must be less than 11 MB.')
        if not value.name.lower().endswith('.jpeg') and not value.name.lower().endswith('.jpg'):
            raise serializers.ValidationError('Avatar must be in JPEG/JPG format.')
        return value

    # def update(self, instance, validated_data):
    #     instance.phone_number = validated_data.get("phone_number", instance.phone_number)
    #     instance.avatar = validated_data.get("avatar", instance.avatar)
    #     instance.save()
    #     return instance
    def update(self, instance, validated_data):
        # Exclude 'identity_code' field from updates
        validated_data.pop('identity_code', None)
        return super().update(instance, validated_data)


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
    url = serializers.HyperlinkedIdentityField(view_name='report-detail', lookup_field='report_number')
    student_first_name = serializers.CharField(source='student.first_name', read_only=True)
    student_last_name = serializers.CharField(source='student.last_name', read_only=True)
    student_course = serializers.CharField(source='student.course', read_only=True)
    report_number = serializers.IntegerField(read_only=True, validators=[MinValueValidator(1)])
    created_through_command = serializers.BooleanField(default=False, read_only=True)
    time_of_submit = serializers.DateTimeField(default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), read_only=True)
    create_at = serializers.DateTimeField(read_only=True)
    modified_at = serializers.DateTimeField(read_only=True)
    is_deleted = serializers.BooleanField(default=False, read_only=True)
    delay = serializers.SerializerMethodField()

    def get_delay(self, obj):
        time_of_submit = obj.time_of_submit
        modified_at = obj.modified_at
        time_difference = modified_at - time_of_submit
        delay = time_difference - timedelta(microseconds=time_difference.microseconds)
        return str(delay)

    class Meta:
        model = Report
        fields = (
            'student_first_name', 'student_last_name', 'student_course', 'report_text', 'study_amount', 'report_number',
            'created_through_command', 'time_of_submit', 'create_at', 'modified_at', 'is_deleted', 'url', 'delay'
        )

    def create(self, validated_data):
        student = validated_data['student']
        existing_report_count = Report.objects.filter(student=student).count()
        report = Report.objects.create(report_number=existing_report_count + 1, **validated_data)
        return report


class AdminPaymentSerializer(serializers.ModelSerializer):
    # student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    student = serializers.SlugRelatedField(queryset=Student.objects.all(), slug_field='first_name')
    amount_of_receipt = serializers.CharField(max_length=9)
    receipt_count = serializers.IntegerField()
    date = JalaliDateField()
    jalali_date = serializers.CharField(required=False, allow_blank=True, max_length=10)

    def create(self, validated_data):
        j_date = validated_data.pop('jalali_date', None)
        if not j_date:
            raise serializers.ValidationError({'jalali_date_of_birth': 'This field is required.'})
        validated_data['date'] = convert_jalali_to_gregorian(j_date)
        admin_payment = AdminPayment.objects.create(**validated_data)
        return admin_payment

    class Meta:
        model = AdminPayment
        fields = ('student', 'amount_of_receipt', 'receipt_count', 'date', 'jalali_date')


# class PaymentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Payment
#         fields = '__all__'



class StudentPaymentSerializer(serializers.ModelSerializer):
    amount_of_receipt_of_each_month = serializers.SerializerMethodField()
    receipt_count_during_course_length = serializers.SerializerMethodField()
    total_payment = serializers.CharField(max_length=9)

    def get_amount_of_receipt_of_each_month(self, obj):
        pass