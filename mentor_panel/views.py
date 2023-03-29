from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import MentorCommentSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from django.conf import settings

import requests

from .serializers import MentorSerializer, MyTokenObtainPairSerializer, LoginViewAsMentorSerializer
from .models import Mentor
from Monitoring.admin_panel.models import Admin

from rest_framework_simplejwt.views import TokenObtainPairView


class LoginViewAsMentor(APIView):

    def post(self, request):
        # Get the username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user using Django's built-in function
        mentor = authenticate(request, username=username, password=password)

        # Check if authentication was using
        if mentor is not None:
            # Log the user in using Django's built-in function
            login(request, mentor)

            serializer = LoginViewAsMentorSerializer(mentor)

            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            # Return an error response if authentication failed
            return Response({"error": "Invalid username  or password"}, status=status.HTTP_401_UNAUTHORIZED)


class MentorDetailView(generics.RetrieveAPIView):
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


class CreateMentorView(APIView):
    """
    View to create a new mentor
    """

    @method_decorator(login_required)
    def post(self, request):

        # Check if the user making the request is an admin
        if not request.user.is_superuser:
            return Response({'error': 'Only admin can create mentor.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Get the request data and create a new mentor account
        try:
            admin = Admin.objects.get(user=request.user)
            mentor_firstname = request.data['first_name']
            mentor_lastname = request.data['last_name']
            mentor_birthday = request.data['data_of_birth']
            mentor_phone_number = request.data['phone_number']
            mentor_identity_code = request.data['identity_code']
            mentor_personality = request.data['personality']
            mentor_avatar = request.data['avatar']
            mentor = admin.create_mentor_account(mentor_firstname, mentor_lastname, mentor_birthday,
                                                 mentor_phone_number, mentor_identity_code, mentor_personality,
                                                 mentor_avatar)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Return the new mentor object
        serializer = MentorSerializer(mentor)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

        # # Get the data from the request
        # data = request.data
        #
        # # Validate the data
        # serializer = MentorSerializer(data=data)
        # if not serializer.is_valid():
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Create the mentor account
