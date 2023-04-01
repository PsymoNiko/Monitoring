from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.reverse import reverse

from mentor_panel.serializers import MentorSerializer
from student_panel.serializers import StudentSerializer
from .serializers import LoginViewAsAdminSerializer, CourseSerializers

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.views import LogoutView

from .models import Course


class LoginViewAsAdmin(APIView):

    def post(self, request):
        # Get the username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user using Django's built-in function
        user = authenticate(request, username=username, password=password)

        # Check if authentication was using
        if user is not None:
            # Log the user in using Django's built-in function
            login(request, user)

            serializer = LoginViewAsAdminSerializer(user)

            # Return a success response with the user's information
            return Response(serializer.data, status=status.HTTP_200_OK)

            # return Response({
            #     'id': user.id,
            #     'username': user.username,
            #     'email': user.email,
            #     'first_name': user.first_name,
            #     'last_name': user.last_name,
            # }, status=status.HTTP_200_OK)
        else:
            # Return an error response if authentication failed
            return Response({"error": "Invalid username  or password"}, status=status.HTTP_401_UNAUTHORIZED)


class ApiRootView(APIView):
    def get(self, request):
        data = {
            'roots': reverse('roots', request=request),
            'login': reverse('login', request=request),
            'mentors': reverse('create-mentor', request=request),
            'students': reverse('create-student', request=request),
            'token': reverse('token-obtain-pair', request=request),
            'refresh': reverse('refresh-token', request=request),
            'logout': reverse('logout', request=request),
        }

        return Response(data)


class MentorCreateView(generics.CreateAPIView):
    serializer_class = MentorSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mentor = serializer.create(serializer.validated_data)

        return Response({
            'message': 'Mentor account created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)


class StudentCreateView(generics.CreateAPIView):
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student = serializer.create(serializer.validated_data)

        return Response({
            'message': 'Student account created successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)


class CustomRedirectView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super(CustomRedirectView, self).post(request, *args, **kwargs)
        token = response.data.get('access')
        if token:
            # Set the token in the session
            request.session['auth_token'] = token
            return HttpResponseRedirect('/ceo/roots/')  # Replace with the URL you want to redirect to
        return response


class LogoutAPIView(LogoutView):
    next_page = reverse_lazy('login')

    def get_redirect_url(self):
        url = self.request.GET.get('next', self.next_page)
        return url


class LoginViews(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)

            refresh = RefreshToken.for_user(user)

            request.session['access_token'] = str(refresh.access_token)

            return Response({'detail': 'Successfully logged in.'})
        else:
            return Response({'detail': 'Invalid credentials.'})


class CourseCreateView(generics.CreateAPIView):
    serializer_class = CourseSerializers
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Course.objects.all()


class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializers

class CourseUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializers
