# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
#
#
# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('Email is required')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user
#
#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(email, password, **extra_fields)
#
#
# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(unique=True)
#     name = models.CharField(max_length=50)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#
#     objects = CustomUserManager()
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['name']
#
#     def __str__(self):
#         return self.email
#
#
# class CustomBackend:
#     def authenticate(self, request, email=None, password=None, **kwargs):
#         try:
#             user = CustomUser.objects.get(email=email)
#         except CustomUser.DoesNotExist:
#             return None
#
#         if user.check_password(password):
#             return user
#         else:
#             return None
#
#     def get_user(self, user_id):
#         try:
#             return CustomUser.objects.get(pk=user_id)
#         except CustomUser.DoesNotExist:
#             return None
import re

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, identity_number=None, **extra_fields):
        """
        Creates and saves a User with the given phone_number and identity_number.
        """
        if not phone_number:
            raise ValueError('The Phone number field must be set')
        phone_number = self.normalize_phone_number(phone_number)
        user = self.model(phone_number=phone_number, **extra_fields)
        if identity_number:
            user.set_password(identity_number)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, identity_number=None, **extra_fields):
        """
        Creates and saves a superuser with the given phone_number and identity_number.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, identity_number, **extra_fields)

    def normalize_phone_number(self, phone_number):
        """
        Normalizes the phone_number by removing all non-digit characters.
        """
        return re.sub(r'[^\d]+', '', phone_number)




class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'

    objects = CustomUserManager()
