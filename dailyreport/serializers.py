from rest_framework import serializers
from .models import ExerciseSubmission

class ExerciseSubmissionSerializer(serializers.ModelSerializer):
    delay = serializers.SerializerMethodField()
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = ExerciseSubmission
        fields = ('id', 'report_number', 'date', 'student_name', 'total_hours', 'delay', 'detail_url')

    def get_delay(self, obj):
        deadline = obj.date.replace(hour=22, minute=0, second=0, microsecond=0)
        if obj.date > deadline:
            return (obj.date - deadline).seconds // 60
        else:
            return None

    def get_detail_url(self, obj):
        return f"/exercises/{obj.id}/"

class ExerciseSubmissionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseSubmission
        fields = ('id', 'report_number', 'date', 'student_name', 'total_hours', 'comment')

class ExerciseSubmissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseSubmission
        fields = ('report_number', 'date', 'student_name', 'total_hours')

class ExerciseSubmissionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseSubmission
        fields = ('comment',)


#panel student

from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('id', 'date', 'report_number', 'caption', 'hours', 'sent')
