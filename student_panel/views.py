from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework import status, authentication, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate, login
from .models import Payment
from .serializers import StudentTokenObtainPairSerializer, \
    LoginViewAsStudentSerializer, PaymentSerializer
from rest_framework import generics
from .serializers import ReportSummarySerializer
from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Student, Report
from .serializers import StudentSerializer, ReportSerializer
from monitoring.settings import MINIMUM_AMOUNT_OF_STUDY, COST_OF_PUNISHMENT_PER_HOUR


class StudentLoginView(TokenObtainPairView):
    serializer_class = StudentTokenObtainPairSerializer


class LoginViewAsStudent(generics.CreateAPIView):
    serializer_class = LoginViewAsStudentSerializer

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user using Django's built-in function
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


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class ReportListCreateView(generics.ListCreateAPIView):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            student = Student.objects.get(user=self.request.user.id)
        except Student.DoesNotExist:
            raise NotFound('Student not found')  # or return an empty queryset, depending on your desired behavior
        queryset = Report.objects.filter(student=student, student__user=self.request.user.id)
        return queryset

    def post(self, request, *args, **kwargs):
        # Get the student instance associated with the user
        student = Student.objects.get(user=self.request.user)

        # Create a report instance with the student field set to the student instance
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(student=student)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        report_count = queryset.count()
        total_amount_of_study = queryset.aggregate(total_study=Sum('amount_of_study'))['total_study'] or 0
        expected_hour = report_count * MINIMUM_AMOUNT_OF_STUDY
        punishment_for_fraction_of_hour = [0 if not total_amount_of_study < expected_hour else
                                           (expected_hour - total_amount_of_study) * COST_OF_PUNISHMENT_PER_HOUR]
        average_of_amount_of_report = total_amount_of_study / report_count
        summary_serializer = ReportSummarySerializer(
            data={'report_count': report_count,
                  'total_amount_of_study': total_amount_of_study,
                  'expected_hour': expected_hour,
                  'punishment_for_fraction_of_hour': punishment_for_fraction_of_hour,
                  'average_of_amount_of_report': round(average_of_amount_of_report, 2)
                  }
        )
        amount_of_study_list = [report.amount_of_study for report in queryset]
        summary_serializer.is_valid()
        response_data = {'reports': serializer.data, 'summary': summary_serializer.data,
                         'max_amount_of_study': max(amount_of_study_list),
                         'min_amount_of_study': min(amount_of_study_list)
                         }
        return Response(response_data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReportRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
