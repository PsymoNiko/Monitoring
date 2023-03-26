from rest_framework import serializers
from .models import DailyReport


class DailyReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyReport
        fields = "__all__"

    def amount_of_study_report_validator(self, amount_of_study_report: str) -> str:
        if not amount_of_study_report[:1].isnumeric():
            raise serializers.ValidationError("Please Enter a Valid Amount")
        elif not amount_of_study_report[3:].isnumeric():
            raise serializers.ValidationError("Please Enter a Valid Amount")
        return amount_of_study_report



