from django.db import models
from django.contrib.auth.models import User
from mentor.models import Mentor
from student.models import Student
from ceo.models import Course
from django.contrib.auth.hashers import make_password

# Create your models here.
class MentorFactory:
    @staticmethod
    def create_mentor(first_name, last_name, date_of_birth, phone_number, identity_code, personality, avatar=None):
        user = User.objects.create(username=phone_number)

        mentor = Mentor(user=user, first_name=first_name, last_name=last_name,
                                       date_of_birth=date_of_birth, phone_number=phone_number,
                                       identity_code=identity_code, personality=personality, avatar=avatar)
        user_creation_handler = UserCreationHandler()
        user_creation_handler.handle(mentor=mentor)
        mentor.save()
        return mentor


class UserCreationHandler:
    def __init__(self, successor=None):
        self._successor = successor


    def handle(self, mentor):
        if mentor.phone_number is not None:
            password = make_password(mentor.identity_code) # hash the identity_code using make_password
            user = User.objects.create(username=mentor.phone_number, password=password)
            mentor.user = user
        elif self._successor:
            self._successor.handle(mentor)


    # def handle(self, mentor):
    #     if mentor.phone_number is not None:
    #         user = User.objects.create(username=mentor.phone_number)
    #         mentor.user = user
    #     elif self._successor:
    #         self._successor.handle(mentor)


class NullUserCreationHandler:
    def handle(self, mentor):
        pass


class CourseFactory:
    @staticmethod
    def create_course(name, mentor, start_at, duration, days_of_week, class_time, how_to_hold, short_brief):
        course = Course.objects.create(name=name, mentor=mentor, start_at=start_at, duration=duration,
                                       days_of_week=days_of_week, class_time=class_time, how_to_hold=how_to_hold,
                                       short_brief=short_brief)
        return course

    @staticmethod
    def add_mentor_and_students_to_course(course, mentor, students):
        course.mentor = mentor
        course.save()
        for student in students:
            student.course = course
            student.save()


class StudentFactory:
    @staticmethod
    def create_student(first_name, last_name, date_of_birth, phone_number, identity_code, personality, course,
                       avatar=None):
        user = User.objects.create()
        student = Student.objects.create(user=user, first_name=first_name, last_name=last_name,
                                         date_of_birth=date_of_birth, phone_number=phone_number,
                                         identity_code=identity_code, personality=personality, course=course,
                                         avatar=avatar)
        return student
