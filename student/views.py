from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions, generics

from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login

from .models import Student
from ceo.models import Admin
from .serializers import StudentSerializer, StudentTokenObtainPairSerializer, LoginViewAsStudentSerializer


from django.shortcuts import redirect
from rest_framework.authtoken.models import Token

class CreateStudentView(APIView):
    @method_decorator(login_required)
    def post(self, request):
        # Check if the user is an admin
        if not request.user.is_staff:
            return Response({'error': 'You do not have permission to create a student account.'},
                            status=status.HTTP_403_FORBIDDEN)

        # Get the request data and create the new student account
        try:
            admin = Admin.objects.get(user=request.user)
            student_firstname = request.data['first_name']
            student_lastname = request.data['last_name']
            student_phone_number = request.data['phone_number']
            student_birthday = request.data['date_of_birth']
            student_identity_code = request.data['identity_code']
            student_personality = request.data['personality']
            student_avatar = request.data['avatar']
            student = admin.create_student_account(student_firstname, student_lastname, student_phone_number,
                                                   student_birthday, student_identity_code, student_personality,
                                                   student_avatar)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Return the new student object
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StudentLoginView(TokenObtainPairView):
    serializer_class = StudentTokenObtainPairSerializer



class LoginViewAsStudent(APIView):

    def post(self, request):
        # Get the username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user using Django's built-in function
        student = authenticate(request, username=username, password=password)

        # Check if authentication was using
        if student is not None:
            # Log the user in using Django's built-in function
            login(request, student)

            serializer = LoginViewAsStudentSerializer(student)
            # token, _ = Token.objects.get_or_create(user=student)

            # return redirect('detail', pk=student.pk)
        # else:
        #     return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            # Return a success response with the user's information
            return Response(serializer.data, status=status.HTTP_200_OK)



        else:
            # Return an error response if authentication failed
            return Response({"error": "Invalid username  or password"}, status=status.HTTP_401_UNAUTHORIZED)


class StudentDetails(APIView):
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = StudentSerializer(request.user)
        return Response(serializer.data)

class StudentDetailView(generics.RetrieveAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_object(self):
        user_id = self.request.user.id
        return Student.objects.get(user=user_id)



# {"username": "student_09109232094", "password": "0020064586"}