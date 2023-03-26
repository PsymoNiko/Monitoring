from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import MentorCommentSerializer
from Monitoring.admin_panel.models import DefineStudentModel


class CommentOnReport(APIView):
    def post(self, request, last_name, *args, **kwargs):

        student_info = DefineStudentModel.objects.get(last_name=last_name)
        comment_serializer = MentorCommentSerializer(data=request.data, instance=student_info)
        comment_serializer.is_valid(raise_exception=True)
        return Response({"massage": f"comment on {student_info.first_name} {student_info.last_name} set successfully"}
                        , status=status.HTTP_200_OK)





















