import re
from datetime import datetime, timedelta
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db import IntegrityError
from django.db import transaction
from django.contrib.auth.models import User

from .models import Student, Report, Payment, \
    ReportComment, AdminReportComment
from django.core.validators import MinValueValidator
from ceo.models import Course


class StudentSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    date_of_birth = serializers.DateField(format='%Y-%m-%d')
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

    def validate_phone_number(self, value: int or str) -> str:

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

    # def validate_first_name(self, value: str) -> str:
    #     persian_regex = '^[\u0600-\u06FF\s]+$'
    #     if not re.match(persian_regex, value):
    #         raise serializers.ValidationError("First name must be written in Persian.")
    #     elif not re.search('[^a-zA-Z]', value):
    #         raise serializers.ValidationError('First name must not contain signs or numbers.')
    #     if re.search('[\u06F0-\u06F9]', value):
    #         raise serializers.ValidationError('First name must not contain Persian numbers.')
    #     return value
    #
    # def validate_last_name(self, value: str) -> str:
    #     persian_regex = '^[\u0600-\u06FF\s]+$'
    #     if not re.match(persian_regex, value):
    #         raise serializers.ValidationError("Last name must be written in Persian.")
    #     elif not re.search('[^a-zA-Z]', value):
    #         raise serializers.ValidationError('Last name must not contain signs or numbers.')
    #     if re.search('[\u06F0-\u06F9]', value):
    #         raise serializers.ValidationError('Last name must not contain Persian numbers.')
    #     return value

    def validate_identity_code(self, value: str) -> str:
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


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class ReportCommentSerializer(serializers.ModelSerializer):
    mentor_first_name = serializers.CharField(source='mentor.first_name', read_only=True)
    mentor_last_name = serializers.CharField(source='mentor.last_name', read_only=True)

    class Meta:
        model = ReportComment
        fields = (
            'mentor', 'mentor_first_name', 'mentor_last_name',
            'comment', 'created_at'
        )

    def create(self, validated_data, mentor=None, report=None):
        mentor = mentor or validated_data['mentor']
        report = report or validated_data['report']
        if ReportComment.objects.filter(mentor=mentor, report=report).exists():
            raise serializers.ValidationError('Comment already exists for this report.')
        comment = ReportComment.objects.create(
            mentor=mentor,
            report=report,
            comment=validated_data['comment']
        )
        return comment


class AdminReportCommentSerializer(serializers.ModelSerializer):
    admin = serializers.CharField()

    class Meta:
        model = AdminReportComment
        fields = ('admin', 'comment', 'created_at')

    def create(self, validated_data):
        admin_username = validated_data['admin']
        admin = User.objects.get(username=admin_username, is_staff=True)
        report = validated_data['report']
        if AdminReportComment.objects.filter(admin=admin, report=report).exists():
            raise serializers.ValidationError('Comment already exists for this report.')
        comment = AdminReportComment.objects.create(
            admin=admin,
            report=report,
            comment=validated_data['comment']
        )
        return comment


class ReportSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        student_first_name = obj.student.first_name.lower().replace(' ', '-')
        student_last_name = obj.student.last_name.lower().replace(' ', '-')
        report_number = obj.report_number
        return f'http://127.0.0.1:8000/student/reports/{student_first_name}-{student_last_name}/{report_number}/'

    student_first_name = serializers.CharField(source='student.first_name', read_only=True)
    student_last_name = serializers.CharField(source='student.last_name', read_only=True)
    student_course = serializers.CharField(source='student.course', read_only=True)
    course_start_date = serializers.DateField(source='course.start_at', read_only=True, allow_null=True)
    course_duration = serializers.IntegerField(source='course.duration', read_only=True, allow_null=True)
    report_number = serializers.IntegerField(read_only=True, validators=[MinValueValidator(1)])
    created_through_command = serializers.BooleanField(default=False, read_only=True)
    time_of_submit = serializers.DateTimeField(default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), read_only=True)
    create_at = serializers.DateTimeField(read_only=True)
    modified_at = serializers.DateTimeField(read_only=True)
    is_deleted = serializers.BooleanField(default=False, read_only=True)
    delay = serializers.SerializerMethodField()
    mentor_comments = ReportCommentSerializer(many=True, read_only=True)
    admin_comments = AdminReportCommentSerializer(many=True, read_only=True)

    def get_delay(self, obj):
        time_of_submit = obj.time_of_submit
        modified_at = obj.modified_at
        time_difference = modified_at - time_of_submit
        delay = time_difference - timedelta(microseconds=time_difference.microseconds)
        return str(delay)

    class Meta:
        model = Report
        fields = (
            'student_first_name', 'student_last_name', 'student_course', 'course_start_date', 'course_duration',
            'report_text', 'study_amount', 'report_number', 'created_through_command', 'time_of_submit',
            'create_at', 'modified_at', 'is_deleted', 'url', 'delay', 'mentor_comments', "admin_comments"
        )

    def create(self, validated_data):
        student = validated_data['student']
        existing_report_count = Report.objects.filter(student=student).count()
        report = Report.objects.create(report_number=existing_report_count + 1, **validated_data)
        return report


class ReportCardSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        student_first_name = obj.student.first_name.lower().replace(' ', '-')
        student_last_name = obj.student.last_name.lower().replace(' ', '-')
        report_number = obj.report_number
        return f'http://127.0.0.1:8000/student/reports/{student_first_name}-{student_last_name}/{report_number}/'

    report_number = serializers.IntegerField(read_only=True, validators=[MinValueValidator(1)])

    class Meta:
        model = Report
        fields = ('study_amount', 'report_number', 'url')


class ReportSummarySerializer(serializers.Serializer):
    report_count = serializers.IntegerField()
    total_amount_of_study = serializers.FloatField()
    expected_hour = serializers.IntegerField()
    punishment_for_fraction_of_hour = serializers.IntegerField()
    average_of_amount_of_report = serializers.FloatField()
