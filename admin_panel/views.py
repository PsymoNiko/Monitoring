from .serializers import DefineMentorSerializer, DefineStudentSerializer, AdminCommentAndOrganizationalCultureSerializer
from .models import DefineMentorModel, DefineStudentModel
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class DefineMentor(APIView):

    def post(self, request, *args, **kwargs):
        define_mentor_serializer = DefineMentorSerializer(data=request.data)
        define_mentor_serializer.is_valid(raise_exception=True)
        define_mentor_serializer.save()
        return Response(define_mentor_serializer.data, status=status.HTTP_201_CREATED)


class RetrieveMentorInfo(APIView):

    def get(self, request, *args, **kwargs):
        mentor_info = DefineMentorModel.objects.all()
        read_mentor_info_serializer = DefineMentorSerializer(instance=mentor_info, many=True)
        return Response(read_mentor_info_serializer.data, status=status.HTTP_200_OK)


class UpdateMentorInfo(APIView):

    def patch(self, request, mentor_code, *args, **kwargs):
        mentor_info = DefineMentorModel.objects.get(mentor_code=mentor_code)
        update_mentor_info_serializer = DefineMentorSerializer(data=request.data, instance=mentor_info)
        update_mentor_info_serializer.is_valid(raise_exception=True)
        mentor_info.save()
        return Response(update_mentor_info_serializer.data, status=status.HTTP_200_OK)


class DeleteMentorInfo(APIView):

    def delete(self, request, mentor_code, *args, **kwargs):
        mentor_info = DefineMentorModel.objects.get(mentor_code=mentor_code)
        mentor_info.save()
        return Response({"massage": "Mentor Deleted Successfully"}, status=status.HTTP_200_OK)


class DefineStudent(APIView):

    def post(self, request, *args, **kwargs):
        define_student_serializer = DefineStudentSerializer(data=request.data)
        define_student_serializer.is_valid(raise_exception=True)
        define_student_serializer.save()
        return Response(define_student_serializer.data, status=status.HTTP_201_CREATED)


class RetrieveStudentInfo(APIView):

    def get(self, request, *args, **kwargs):
        student_info = DefineStudentModel.objects.all()
        read_student_info_serializer = DefineStudentSerializer(instance=student_info, many=True)
        return Response(read_student_info_serializer.data, status=status.HTTP_200_OK)


class UpdateStudentInfo(APIView):

    def patch(self, request, student_code, *args, **kwargs):
        student_info = DefineStudentModel.objects.get(student_code=student_code)
        update_student_info_serializer = DefineStudentSerializer(data=request.data, instance=student_info)
        update_student_info_serializer.is_valid(raise_exception=True)
        student_info.save()
        return Response(update_student_info_serializer.data, status=status.HTTP_200_OK)


class DeleteStudentInfo(APIView):

    def delete(self, request, mentor_code, *args, **kwargs):
        student_info = DefineMentorModel.objects.get(mentor_code=mentor_code)
        student_info.save()
        return Response({"massage": "Mentor Deleted Successfully"}, status=status.HTTP_200_OK)


class CommentOnReport(APIView):

    def post(self, request, student_code, *args, **kwargs):
        student_info = DefineStudentModel.objects.get(student_code=student_code)
        comment_serializer = AdminCommentAndOrganizationalCultureSerializer(data=request.data, instance=student_info)
        comment_serializer.is_valid(raise_exception=True)
        return Response({"massage": f"comment set successfully {student_info.first_name} {student_info.last_name}"}, status=status.HTTP_200_OK)


