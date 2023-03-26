from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import DailyReportSerializer
from .tasks import (
    max_amount_of_study,
    min_amount_of_study,
    expected_hour,
    sum_of_report,
    punishment_for_fraction_of_hour,
    average_of_amount_of_report
)
from .models import DailyReport


class DailyReportView(APIView):

    def post(self, request, *args, **kwargs):
        report_serializer = DailyReportSerializer(data=request.data)
        report_serializer.is_valid(raise_exception=True)
        return Response({"massage": "ok"}, status=status.HTTP_201_CREATED)


class RetrieveReport(APIView):

    def get(self, request, report_number, *args, **kwargs):
        report_info = DailyReport.objects.get(report_number)
        get_report_serializer = DailyReportSerializer(instance=report_info)
        get_report_serializer.is_valid(raise_exception=True)
        deadline = get_report_serializer.validated_data.get("date_field")
        time_of_sending_report = get_report_serializer.validated_data.get("day_of_report")
        if deadline < time_of_sending_report:
            delay = deadline - time_of_sending_report
            return Response(delay, )


class ReportView(APIView):

    def get(self, request, *args, **kwargs):
        max_amount_of_study.apply_async(args="amount")
        min_amount_of_study.apply_async(args="amount")
        expected_hour.apply_async(args="amount")
        sum_of_report.apply_async(args="amount")
        punishment_for_fraction_of_hour.apply_async(args="amount")
        average_of_amount_of_report.apply_async(args="amount")
