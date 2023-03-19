from rest_framework import serializers
from .models import DailyReportModel


class DailyReportSerializer(serializers.ModelSerializer):
    amount_of_study = serializers.CharField(max_length=5)

    def amount_of_study_validators(self, study: str) -> str:
        if not study.isnumeric():
            raise serializers.ValidationError("Please Enter a Valid Amount")
        return study

    class Meta:
        model = DailyReportModel
        fields = ["number_of_report", "report_time", "explain_report", "amount_of_study"]
