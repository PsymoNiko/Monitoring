from rest_framework import serializers

from .models import MentorReportSubmission
from .models import StudentReport


class ReportSubmissionMentorSerializer(serializers.ModelSerializer):
    delay = serializers.SerializerMethodField()
    detail_url = serializers.SerializerMethodField()

    class Meta:
        model = MentorReportSubmission
        fields = ('id', 'report_number', 'date', 'student_name', 'total_hours', 'delay', 'detail_url')

    def get_delay(self, obj):
        deadline = obj.date.replace(hour=22, minute=0, second=0, microsecond=0)
        if obj.date > deadline:
            return (obj.date - deadline).seconds // 60
        else:
            return None

    def get_detail_url(self, obj):
        return f"/exercises/{obj.id}/"

class ReportSubmissionDetailMentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorReportSubmission
        fields = ('id', 'report_number', 'date', 'student_name', 'total_hours', 'comment')

class ReportSubmissionCreateMentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorReportSubmission
        fields = ('report_number', 'date', 'student_name', 'total_hours')

class ReportSubmissionUpdateMentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorReportSubmission
        fields = ('comment',)


#panel student
class ReportStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentReport
        fields = ('id', 'date', 'report_number', 'caption', 'hours', 'sent','minute')
