from rest_framework.views import APIView
from rest_framework.response import Response

from Monitoring.mentor.serializers import MentorCommentSerializer
from Monitoring.ceo.serializers import AdminCommentSerializer
from Monitoring.mentor.models import MentorCommentModel
from Monitoring.ceo.models import AdminCommentModel


from .serializers import DailyReportSerializer
from .tasks import (
    max_amount_of_study,
    min_amount_of_study,
    expected_hour,
    sum_of_report,
    punishment_for_fraction_of_hour,
    average_of_amount_of_report
)


class ReportView(APIView):

    def get(self, request, *args, **kwargs):
        max_amount_of_study.apply_async(args="amount")
        min_amount_of_study.apply_async(args="amount")
        expected_hour.apply_async(args="amount")
        sum_of_report.apply_async(args="amount")
        punishment_for_fraction_of_hour.apply_async(args="amount")
        average_of_amount_of_report.apply_async(args="amount")

















