from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F
from django.db.models import Sum
import requests
from .serializers import ReportSerializer
from .tasks import (
    max_amount_of_study,
    min_amount_of_study,
    expected_hour,
    sum_of_report,
    punishment_for_fraction_of_hour,
    average_of_amount_of_report
)
from .models import Report

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime


class DailyReportView(APIView):
    def post(self, request):
        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UnsubmittedReportsView(APIView):
    def get(self, request):
        user = request.user
        report_count = Report.objects.filter(user=user).count()
        submitted_count = Report.objects.filter(user=user, created_at__lte=F('deadline')).count()
        unsubmitted_count = report_count - submitted_count
        return Response({'unsubmitted_count': unsubmitted_count, 'total_count': report_count})


class DelayedReportsView(APIView):
    def get(self, request):
        user = request.user
        delayed_reports = Report.objects.filter(user=user, delayed=True)
        serializer = ReportSerializer(delayed_reports, many=True)
        return Response(serializer.data)


class ReportSummaryView(APIView):
    def get(self, request):
        user = request.user
        amount = Report.objects.filter(user=user).values('report_number').annotate(
            total_study=Sum('study_amount'))
        return Response(amount)


class SomeOtherClass(APIView):
    def some_method(self, request):
        user = self.request.user
        report_summary_response = requests.get('http://localhost:8000/reports/summery/',
                                               auth=(user.username, user.password))
        report_summary = report_summary_response.json()
        # do something with the report_summary list here
        return report_summary


class ReportView(APIView):

    def get(self, request, *args, **kwargs):
        max_amount_of_study.apply_async(args="amount")
        min_amount_of_study.apply_async(args="amount")
        expected_hour.apply_async(args="amount")
        sum_of_report.apply_async(args="amount")
        punishment_for_fraction_of_hour.apply_async(args="amount")
        average_of_amount_of_report.apply_async(args="amount")
