from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics


from django.shortcuts import get_object_or_404
from datetime import date, datetime


from .models import MentorExerciseSubmission
from .models import StudentReport

from .serializers import ReportSubmissionMentorSerializer, ReportSubmissionDetailMentorSerializer, ReportSubmissionCreateMentorSerializer, ReportSubmissionUpdateMentorSerializer ,ReportStudentSerializer


class ReportSubmissionList(APIView):
    def get(self, request):
        submissions = MentorExerciseSubmission.objects.all()
        serializer = ReportSubmissionMentorSerializer(submissions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReportSubmissionCreateMentorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class ReportSubmissionDetail(APIView):
    def get(self, request, pk):
        submission = get_object_or_404(MentorExerciseSubmission, pk=pk)
        serializer = ReportSubmissionDetailMentorSerializer(submission)
        return Response(serializer.data)

    def put(self, request, pk):
        submission = get_object_or_404(MentorExerciseSubmission, pk=pk)
        serializer = ReportSubmissionUpdateMentorSerializer(submission, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
        
class SearchReports(APIView):
    def get(self, request):
        report_number = request.query_params.get('report_number')
        date_str = request.query_params.get('date')
        if report_number:
            report = StudentReport.objects.filter(report_number=report_number).first()
        elif date_str:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            report = StudentReport.objects.filter(date=date_obj).first()
        else:
            report = None
        if report:
            serializer = ReportStudentSerializer(report)
            return Response(serializer.data)
        else:
            return Response({'error': 'Report not found'}, status=404)


#panel student
class ReportListStudent(generics.ListCreateAPIView):
    queryset = StudentReport.objects.all()
    serializer_class = ReportStudentSerializer

class ReportDetailStudent(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentReport.objects.all()
    serializer_class = ReportStudentSerializer

class UnsentedReportsStudent(APIView):
    def get(self, request):
        unsent_reports = StudentReport.objects.filter(sent=False, date=date.today()).count()
        return Response({'unsent_reports': unsent_reports})

class SentReportsStudent(APIView):
    def get(self, request):
        reports = StudentReport.objects.filter(sent=True)
        serializer = ReportStudentSerializer(reports, many=True)
        return Response({'reports': serializer.data})


class SearchReportsStudent(APIView):
    def get(self, request):
        report_number = request.query_params.get('report_number')
        date_str = request.query_params.get('date')
        if report_number:
            report = StudentReport.objects.filter(report_number=report_number).first()
        elif date_str:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            report = StudentReport.objects.filter(date=date_obj).first()
        else:
            report = None
        if report:
            serializer = ReportStudentSerializer(report)
            return Response(serializer.data)
        else:
            return Response({'error': 'Report not found'}, status=404)
