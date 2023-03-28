from rest_framework import serializers
from .models import DailyReport

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyReport
        fields = ['id', 'hours', 'minutes', 'text']

