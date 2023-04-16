from django.utils import timezone
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import authentication, permissions, generics, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.db.models import Sum
from .models import Student, Payment, Report
from .serializers import StudentSerializer, StudentTokenObtainPairSerializer, \
    LoginViewAsStudentSerializer, PaymentSerializer, ReportSerializer, ReportSummarySerializer, ReportCardSerializer
from rest_framework.response import Response
from rest_framework import status
from monitoring.settings import MINIMUM_AMOUNT_OF_STUDY, COST_OF_PUNISHMENT_PER_HOUR
from dateutil.relativedelta import relativedelta


class StudentLoginView(TokenObtainPairView):
    serializer_class = StudentTokenObtainPairSerializer


class LoginViewAsStudent(generics.CreateAPIView):
    serializer_class = LoginViewAsStudentSerializer

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        student = authenticate(request, username=username, password=password)

        if student is not None:
            login(request, student)
            return Response(self.get_serializer(student).data, status=status.HTTP_200_OK)

        else:
            return Response({"error": "Invalid username  or password"}, status=status.HTTP_401_UNAUTHORIZED)


class StudentDetails(APIView):
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = StudentSerializer(request.user)
        return Response(serializer.data)


class StudentDetailView(generics.RetrieveDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_object(self):
        user_id = self.request.user.id
        return Student.objects.get(user=user_id)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class ReportListCreateView(generics.ListCreateAPIView):
    serializer_class = ReportSerializer
    queryset = Report.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            student = Student.objects.get(user=self.request.user.id)
        except Student.DoesNotExist:
            raise NotFound('Student not found')  # or return an empty queryset, depending on your desired behavior
        queryset = Report.objects.filter(student=student, student__user=self.request.user.id)
        return queryset

    def post(self, request, *args, **kwargs):
        student = Student.objects.get(user=self.request.user)
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(student=student)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReportRetrieveView(generics.RetrieveAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    lookup_field = 'report_number'

    def get_queryset(self):
        try:
            student = Student.objects.get(user=self.request.user.id)
        except Student.DoesNotExist:
            raise NotFound('Student not found')
        queryset = Report.objects.filter(student=student, student__user=self.request.user.id)
        return queryset


class DailyReportView(generics.ListCreateAPIView):
    serializer_class = ReportSerializer

    def get_queryset(self):
        current_time = timezone.now()

        students = Student.objects.all()

        submitted_reports = Report.objects.filter(
            time_of_submit__date=current_time.date()
        ).values_list('student', 'report_number')

        missing_reports = []
        for student in students:
            if (student.id, current_time.date().strftime('%Y%m%d')) not in submitted_reports:
                missing_reports.append(student)

        return missing_reports

    def post(self, request, *args, **kwargs):
        missing_reports = self.get_queryset()

        for student in missing_reports:
            report_number = Report.objects.filter(student=student).count() + 1
            report_data = {
                'student': student.id,
                'report_text': '',
                'study_amount': 0,
                'report_number': report_number,
                'create_through_command': True,
            }
            serializer = ReportSerializer(data=report_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(status=status.HTTP_201_CREATED)


class ListOfUnSubmittedReportsAPIView(generics.ListAPIView):
    serializer_class = ReportSerializer

    def get_queryset(self):
        student = Student.objects.get(user=self.request.user.id)
        queryset = Report.objects.filter(student=student, created_through_command=True)
        return queryset


class UpdateUnSubmittedReportAPIView(generics.UpdateAPIView):
    serializer_class = ReportSerializer
    lookup_field = 'report_number'

    def get_queryset(self):
        student = Student.objects.get(user=self.request.user.id)
        queryset = Report.objects.filter(student=student, created_through_command=True)
        return queryset


class MonthlyReportCardView(generics.ListAPIView):
    serializer_class = ReportCardSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        try:
            student = Student.objects.get(
                first_name=self.kwargs.get('student_first_name'),
                last_name=self.kwargs.get('student_last_name')
            )
        except Student.DoesNotExist:
            raise NotFound('Student not found')

        month = self.kwargs.get('month')
        year = self.kwargs.get('year')

        start_date = datetime(year=year, month=month, day=1)
        end_date = start_date + relativedelta(months=1) - relativedelta(days=1)

        queryset = Report.objects.filter(
            student=student,
            time_of_submit__gte=start_date,
            time_of_submit__lte=end_date,
        )

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, context={'request': request}, many=True)
        report_count = queryset.count()
        total_amount_of_study = queryset.aggregate(total_study=Sum('study_amount'))['total_study'] or 0
        expected_hour = report_count * MINIMUM_AMOUNT_OF_STUDY
        punishment_for_fraction_of_hour = [0 if not total_amount_of_study < expected_hour else
                                           (expected_hour - total_amount_of_study) * COST_OF_PUNISHMENT_PER_HOUR]
        average_of_amount_of_report = [0 if report_count == 0 else round((total_amount_of_study / report_count), 2)]
        print(total_amount_of_study)
        summary_serializer = ReportSummarySerializer(
            data={'report_count': report_count,
                  'total_amount_of_study': total_amount_of_study,
                  'expected_hour': expected_hour,
                  'punishment_for_fraction_of_hour': punishment_for_fraction_of_hour,
                  'average_of_amount_of_report': average_of_amount_of_report
                  }
        )
        amount_of_study_list = [0 if not queryset else report.study_amount for report in queryset]
        max_amount_of_study = [max(amount_of_study_list) if amount_of_study_list else 0]
        min_amount_of_study = [min(amount_of_study_list) if amount_of_study_list else 0]
        summary_serializer.is_valid()
        response_data = {'reports': serializer.data, 'summary': summary_serializer.data,
                         'max_amount_of_study': max_amount_of_study,
                         'min_amount_of_study': min_amount_of_study
                         }
        return Response(response_data)
