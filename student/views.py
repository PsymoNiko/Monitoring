from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions, generics, viewsets

from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login

from .models import Student, Payment
# from ceo.models import Admin
from .serializers import StudentSerializer, StudentTokenObtainPairSerializer, \
    LoginViewAsStudentSerializer, ReportSerializer, PaymentSerializer


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


class DailyReportView(generics.CreateAPIView):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        report = serializer.create(serializer.validated_data)
        return Response({
            'message': "Report Created successfully",
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
