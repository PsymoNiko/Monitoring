from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings

import requests

from .serializers import MentorSerializer
from ceo.models import Admin
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
