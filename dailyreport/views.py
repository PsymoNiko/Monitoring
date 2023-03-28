from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import ExerciseSubmission
from .serializers import ExerciseSubmissionSerializer, ExerciseSubmissionDetailSerializer, ExerciseSubmissionCreateSerializer, ExerciseSubmissionUpdateSerializer

class ExerciseSubmissionList(APIView):
    def get(self, request):
        submissions = ExerciseSubmission.objects.all()
        serializer = ExerciseSubmissionSerializer(submissions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ExerciseSubmissionCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExerciseSubmissionDetail(APIView):
    def get(self, request, pk):
        submission = get_object_or_404(ExerciseSubmission, pk=pk)
        serializer = ExerciseSubmissionDetailSerializer(submission)
        return Response(serializer.data)

    def put(self, request, pk):
        submission = get_object_or_404(ExerciseSubmission, pk=pk)
        serializer = ExerciseSubmissionUpdateSerializer(submission, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#panel student
from datetime import date, datetime, time
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import Report
from .serializers import ReportSerializer

class ReportList(generics.ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

class ReportDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

class UnsentedReports(APIView):
    def get(self, request):
        unsent_reports = Report.objects.filter(sent=False, date=date.today()).count()
        return Response({'unsent_reports': unsent_reports})

class SentReports(APIView):
    def get(self, request):
        reports = Report.objects.filter(sent=True)
        serializer = ReportSerializer(reports, many=True)
        return Response({'reports': serializer.data})

class SearchReports(APIView):
    def get(self, request):
        report_number = request.query_params.get('report_number')
        date_str = request.query_params.get('date')
        if report_number:
            report = Report.objects.filter(report_number=report_number).first()
        elif date_str:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            report = Report.objects.filter(date=date_obj).first()
        else:
            report = None
        if report:
            serializer = ReportSerializer(report)
            return Response(serializer.data)
        else:
            return Response({'error': 'Report not found'}, status=404)
