from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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

            # Return a success response with the user's information
            return Response({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }, status=status.HTTP_200_OK)
        else:
            # Return an error response if authentication failed
            return Response({"error": "Invalid username  or password"}, status=status.HTTP_401_UNAUTHORIZED)