from django.utils import timezone
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import authentication, permissions, generics, viewsets

from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth import authenticate, login

from .models import Student, Payment, Report
from .serializers import StudentSerializer, StudentTokenObtainPairSerializer, \
    LoginViewAsStudentSerializer, PaymentSerializer, ReportSerializer
from rest_framework.response import Response
from rest_framework import status


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

    # class ReportListCreateView(generics.ListCreateAPIView):
    #     # permission_classes = [IsAuthenticated]
    #     queryset = Report.objects.all()
    #     serializer_class = ReportSerializer


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
        # Get the student instance associated with the use
        student = Student.objects.get(user=self.request.user)
        # Create a report instance with the student field set to the student instance
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
        # Get the current date and time
        current_time = timezone.now()

        # Get all students
        students = Student.objects.all()

        # Get the report numbers of all reports submitted by each student for today
        submitted_reports = Report.objects.filter(
            time_of_submit__date=current_time.date()
        ).values_list('student', 'report_number')

        # Find students who have not submitted their report for today
        missing_reports = []
        for student in students:
            # Check if the student has already submitted a report for today
            if (student.id, current_time.date().strftime('%Y%m%d')) not in submitted_reports:
                missing_reports.append(student)

        # Return the missing reports
        return missing_reports

    def post(self, request, *args, **kwargs):
        # Get the list of missing reports
        missing_reports = self.get_queryset()

        # Create a new report for each missing report
        for student in missing_reports:
            report_number = Report.objects.filter(student=student).count() + 1
            report_data = {
                'student': student.id,
                'report_text': '',
                'study_amount': 0,
                'report_number': report_number,
                'is_submitted': False,
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

