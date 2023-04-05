from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions, generics, viewsets

from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate, login

from .models import Student, Payment
from .serializers import StudentSerializer, StudentTokenObtainPairSerializer, \
    LoginViewAsStudentSerializer, ReportSerializer, PaymentSerializer
from rest_framework import generics
from rest_framework.response import Response
from .models import Report
from .serializers import ReportSerializer, ReportSummarySerializer
from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.response import Response
from django.utils import timezone
from .models import Student, Report
from .serializers import StudentSerializer, ReportSerializer


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

    def get_queryset(self):
        try:
            student = Student.objects.get(user=self.request.user)
        except Student.DoesNotExist:
            raise NotFound('Student not found')  # or return an empty queryset, depending on your desired behavior
        queryset = Report.objects.filter(student=student)
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
        summary_serializer = ReportSummarySerializer(
            data={'report_count': report_count, 'total_amount_of_study': total_amount_of_study})
        summary_serializer.is_valid()
        response_data = {'reports': serializer.data, 'summary': summary_serializer.data}
        return Response(response_data)


class ReportRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
