from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.db import IntegrityError
from django.db import transaction

from django.contrib.auth.models import User
from .models import Course, DailyNote
from mentor.models import Mentor
from student.serializers import StudentSerializer
from student.models import AdminPayment
from monitoring.utils import *


class LoginViewAsAdminSerializer(serializers.ModelSerializer):
    username = serializers.CharField(allow_blank=True)
    password = serializers.CharField(allow_blank=True, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['user_id'] = user.id
        token['username'] = user.username

        return token


class CourseSerializers(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='course-detail')
    name = serializers.CharField(required=True)
    mentor = serializers.PrimaryKeyRelatedField(queryset=Mentor.objects.all())
    students = StudentSerializer(many=True, read_only=True)
    # start_at = serializers.DateField(required=True)
    start_at = JalaliDateField()
    jalali_start_at = serializers.CharField(required=False, allow_blank=True, max_length=10)
    days_of_week = serializers.MultipleChoiceField(choices=Course.DAYS_OF_WEEK_CHOICES)
    duration = serializers.IntegerField(default=6, min_value=0)
    class_time = serializers.TimeField()  # format=['%H']
    how_to_hold = serializers.ChoiceField(choices=Course.HOLDING, required=True)
    short_brief = serializers.CharField(max_length=70)

    def create(self, validated_data):
        try:
            with transaction.atomic():
                jalali_date = validated_data.pop('jalali_start_at', None)
                if not jalali_date:
                    raise serializers.ValidationError({
                        "jalali_start_at": "This field must not be empty."
                    })
                validated_data['start_at'] = convert_jalali_to_gregorian(jalali_date)

                course = Course.objects.create(**validated_data)
                return course
        except IntegrityError:
            raise serializers.ValidationError('please a start_at date')


    class Meta:
        model = Course
        fields = ('id', 'name', 'mentor', 'students', 'jalali_start_at', 'start_at', 'days_of_week', 'duration', 'class_time',
                  'how_to_hold', 'short_brief', 'url')
        read_only_fields = ['id', 'jalali_start_at', 'start_at', 'students']


    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.mentor = validated_data.get("mentor", instance.mentor)
        instance.start_at = validated_data.get("start_at", instance.start_at)
        instance.duration = validated_data.get("duration", instance.duration)
        instance.class_time = validated_data.get("class_time", instance.class_time)
        instance.how_to_hold = validated_data.get("how_to_hold", instance.how_to_hold)
        instance.short_brief = validated_data.get("short_brief", instance.short_brief)
        instance.save()
        return instance


class DailyNoteSerializers(serializers.ModelSerializer):
    daily_note = serializers.CharField()
    # created_at = JDateField(format='%Y-%m-%d')
    class Meta:
        model = DailyNote
        fields = ('daily_note', 'created_at',)



class AdminPaymentSerializer(serializers.ModelSerializer):
    student = serializers.ReadOnlyField(source='student.id')

    class Meta:
        model = AdminPayment
        fields = ['student', 'amount_of_receipt', 'receipt_count', 'date']