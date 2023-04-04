from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Course, StudentLeaveModel
from mentor_panel.models import Mentor


class LoginViewAsAdminSerializer(serializers.ModelSerializer):
    username = serializers.CharField(allow_blank=True)
    password = serializers.CharField(allow_blank=True, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')


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
    start_at = serializers.DateField(required=True)
    duration = serializers.IntegerField(default=6, min_value=0)
    class_time = serializers.TimeField()  # format=['%H']
    how_to_hold = serializers.ChoiceField(choices=Course.HOLDING, required=True)
    short_brief = serializers.CharField(max_length=70)

    class Meta:
        model = Course
        fields = ('id', 'name', 'mentor', 'start_at', 'duration', 'class_time',
                  'how_to_hold', 'short_brief', 'url')

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


class StudentLeaveSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=StudentLeaveModel.objects.all())
    date_of_leave = serializers.DateField()
    leave_period = serializers.IntegerField()
    reason = serializers.ChoiceField(choices=StudentLeaveModel.JUSTIFICATION)
    leave_time = serializers.CharField()
    created_at = serializers.DateField(read_only=True)
    modified_at = serializers.DateField(read_only=True)
    is_deleted = serializers.BooleanField(default=False, read_only=True)

    class Meta:
        model = StudentLeaveModel
        fields = [
            'student', 'date_of_leave', 'leave_period', 'reason', 'leave_time', 'created_at',
            'modified_at', 'is_deleted'
        ]
        read_only = ['created_at', 'modified_at', 'is_deleted']

    def leave_time_validation(self, leave_time: str) -> str:
        if not leave_time.isnumeric():
            raise serializers.ValidationError("Please Enter a Valid amount")
        return leave_time


