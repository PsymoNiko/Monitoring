from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics


from django.shortcuts import get_object_or_404
from datetime import date, datetime
from django.http import Http404



from .models import MentorReportSubmission
from .models import StudentReport

# from .serializers import ReportSubmissionMentorSerializer, ReportSubmissionDetailMentorSerializer, ReportSubmissionCreateMentorSerializer,ReportSubmissionUpdateMentorSerializer ,ReportStudentSerializer
from .serializers import MentorReportSubmissionSerializer, ReportSubmissionUpdateMentorSerializer, MentorReportSubmissionSerializer,ReportStudentSerializer



class MentorReportSubmissionList(APIView):
    """
    List all report submissions 
    """
    def get(self, request):
        reports = MentorReportSubmission.objects.all()
        serializer = MentorReportSubmissionSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MentorReportSubmissionDetail(APIView):
    """
    Retrieve, update or delete a report submission instance.
    """
    def get_object(self, pk):
        try:
            return MentorReportSubmission.objects.get(pk=pk)
        except MentorReportSubmission.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        report = self.get_object(pk)
        serializer = MentorReportSubmissionSerializer(report)
        return Response(serializer.data)
    
# can send comment for student
    def put(self, request, pk):
        report = self.get_object(pk)
        serializer = ReportSubmissionUpdateMentorSerializer(report, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
        

    def delete(self, request, pk):
        report = self.get_object(pk)
        report.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MentorReportSubmissionSearch(APIView):
    """
    Search for a report submission based on the report number or the date
    """
    def get(self, request):
        report_number = request.query_params.get('report_number')
        date_str = request.query_params.get('date')
        if report_number:
            reports = MentorReportSubmission.objects.filter(report_number=report_number)
        elif date_str:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            reports = MentorReportSubmission.objects.filter(date=date_obj)
        else:
            reports = MentorReportSubmission.objects.none()
        serializer = MentorReportSubmissionSerializer(reports, many=True)
        return Response(serializer.data)


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
