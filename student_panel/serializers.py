from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    delayed = serializers.BooleanField(read_only=True)

    class Meta:
        model = Report
        fields = '__all__'

