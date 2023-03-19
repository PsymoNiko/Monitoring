from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import StudentInformationSerializer, AdminCommentSerializer


class DefineStudentForClass(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        student_info_serializer = StudentInformationSerializer(data=request.data)
        student_info_serializer.is_valid(raise_exception=True)
        student_info_serializer.save()
        return Response(student_info_serializer.data, status=status.HTTP_201_CREATED)


class DefineMentorForClass(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        mentor_info_serializer = ""


class CommentForReportCart(APIView):

    def post(self, request, *args, **kwargs):
        comment_serializer = AdminCommentSerializer(data=request.data)
        comment_serializer.is_valid(raise_exception=True)
        comment = comment_serializer.validated_data.get("comment")
        return Response({"massage": f"{comment} has been successfully registered"})
