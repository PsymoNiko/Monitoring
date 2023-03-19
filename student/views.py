from rest_framework.views import APIView
from rest_framework.response import Response

from Monitoring.mentor.serializers import MentorCommentSerializer
from Monitoring.ceo.serializers import AdminCommentSerializer


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

        admin_comment_serializer = AdminCommentSerializer()














