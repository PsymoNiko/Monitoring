from django.db import models
from django.contrib.auth.models import User, Group, Permission
from student.models import Student
from mentor.models import Mentor

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# class MyUserManager(BaseUserManager):
#     def create_user(self, ):



class Admin(AbstractBaseUser, PermissionsMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name='admin_groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',

    )
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='admin_user_permissions',
        help_text='Specific permissions for this user',
        verbose_name='user_permissions',
    )



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
        user.save(using=self._db)

        # Create a new Student object with the created user and associate it with the admin
        student = Student.objects.create(user=user, mentor=self.user, first_name=student_firstname,
                                         last_name=student_lastname, phone_number=student_phone_number,
                                         date_of_birth=student_date_of_birth, identity_code=student_identity_code,
                                         personality=student_personality, avatar=student_avatar)
        return student



    def create_mentor_account(self, mentor_firstname, mentor_lastname, mentor_date_of_birth,
                             mentor_phone_number, mentor_identity_code, mentor_personality,
                             mentor_avatar):
        # Create a new User object with a unique username
        username = User.objects.create_user(username=f"mentor_{mentor_identity_code}")

        # Set password for the user
        user = User.objects.get(username=username.username)
        user.set_password('mentor_identity_code')
        user.save(using=self._db)

        # Create a new Mentor object with the created user and associate it with the admin
        mentor = Mentor.objects.create(user=user, first_name=mentor_firstname, last_name=mentor_lastname,
                                       date_of_birth=mentor_date_of_birth,
                                       phone_number=mentor_phone_number, identity_code=mentor_identity_code,
                                       personality=mentor_personality, avatar=mentor_avatar)
        return mentor