from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from .serializers import MentorSerializer, MyTokenObtainPairSerializer, LoginViewAsMentorSerializer, \
    ChangeMentorPasswordSerializer
from .models import Mentor

from rest_framework_simplejwt.views import TokenObtainPairView


class LoginViewAsMentor(generics.CreateAPIView):
    serializer_class = LoginViewAsMentorSerializer

    def create(self, request, *args, **kwargs):
        # Get the username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')

        mentor = authenticate(request, username=username, password=password)

        if mentor is not None:

            login(request, mentor)
            return Response(self.get_serializer(mentor).data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid username  or password"}, status=status.HTTP_401_UNAUTHORIZED)


class MentorDetailView(generics.RetrieveUpdateAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer

    def get_object(self):
        user_id = self.request.user.id
        return Mentor.objects.get(user=user_id)


class MyTokenObtainPairView(TokenObtainPairView):
    # Set the serializer class used for token generation
    serializer_class = MyTokenObtainPairSerializer


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'refresh_token': token.get_refresh_token(),
        }, status=status.HTTP_200_OK)


class ChangeMentorPasswordView(generics.UpdateAPIView):
    serializer_class = ChangeMentorPasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get("old_password")
            new_password = serializer.data.get("new_password")
            confirm_password = serializer.data.get("confirm_password")

            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            if new_password != confirm_password:
                return Response({"new_password": ["Passwords don't match."]}, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(new_password)
            self.object.save()
            return Response({"status": "password changed"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
