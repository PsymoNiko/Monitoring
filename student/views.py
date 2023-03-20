from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from ceo.models import Admin
from .serializers import StudentSerializer

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
