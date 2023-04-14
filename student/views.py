from django.db.models import Sum
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
