from django.db import models
from django.contrib.auth.models import User
from student.models import Student
from mentor.models import Mentor


class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def create_student_account(self, student_firstname, student_lastname,
                               student_phone_number, student_date_of_birth,
                               student_identity_code,
                               student_personality,
                               student_avatar):
        # Create a new User object with a unique username
        username = User.objects.create_user(username=f"student_{student_phone_number}")

        # Set password for the user
        user = User.objects.get(username=username.username)
        user.set_password(student_identity_code)
        user.save()

        # Create a new Student object with the created user and associate it with the admin
        student = Student.objects.create(user=username, mentor=self.user, first_name=student_firstname,
                                         last_name=student_lastname, phone_number=student_phone_number,
                                         date_of_birth=student_date_of_birth, identity_code=student_identity_code,
                                         personality=student_personality, avatar=student_avatar)
        return student

    def create_mentor_account(self, mentor_firstname, mentor_lastname, mentor_date_of_birth,
                             mentor_phone_number, mentor_identity_code, mentor_personality,
                             mentor_avatar):
        # Create a new User object with a unique username
        username = User.objects.create_user(username=f"mentor_{mentor_phone_number}")

        # Set password for the user
        user = User.objects.get(username=username.username)
        user.set_password(mentor_identity_code)
        user.save()

        # Create a new Mentor object with the created user and associate it with the admin
        mentor = Mentor.objects.create(user=username, first_name=mentor_firstname, last_name=mentor_lastname,
                                       date_of_birth=mentor_date_of_birth,
                                       phone_number=mentor_phone_number, identity_code=mentor_identity_code,
                                       personality=mentor_personality, avatar=mentor_avatar)
        return mentor
