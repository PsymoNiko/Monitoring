from django.db import models


class DefineMentorModel(models.Model):
    PERSONALITY_TYPES = [
                         "ISTJ",  # -> The Inspector
                         "ISFJ",  # -> The Protector
                         'INFJ',  # -> #The Counselor
                         'INTJ',  # -> The Mastermind
                         'ISTP',  # -> The Craftsman
                         'ISFP',  # -> The Composer
                         'INFP',  # -> The Healer
                         'INTP',  # -> The Architect
                         'ESTP',  # -> The Dynamo
                         'ESFP',  # -> The Performer
                         'ENFP',  # -> The Champion
                         'ENTP',  # -> The Visionary
                         'ESTJ',  # -> The Supervisor
                         'ESFJ',  # -> The Provider
                         'ENFJ',  # -> The Teacher
                         'ENTJ',  # -> The Commander
                         ]
    mentor_picture = models.ImageField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    id_number = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=13)
    mentor_code = models.CharField(max_length=20)
    mentor_birthday = models.DateField()
    personality_type = models.CharField(max_length=4, choices=PERSONALITY_TYPES)


class DefineStudentModel(models.Model):
    PERSONALITY_TYPES = [
                         "ISTJ",  # -> The Inspector
                         "ISFJ",  # -> The Protector
                         'INFJ',  # -> #The Counselor
                         'INTJ',  # -> The Mastermind
                         'ISTP',  # -> The Craftsman
                         'ISFP',  # -> The Composer
                         'INFP',  # -> The Healer
                         'INTP',  # -> The Architect
                         'ESTP',  # -> The Dynamo
                         'ESFP',  # -> The Performer
                         'ENFP',  # -> The Champion
                         'ENTP',  # -> The Visionary
                         'ESTJ',  # -> The Supervisor
                         'ESFJ',  # -> The Provider
                         'ENFJ',  # -> The Teacher
                         'ENTJ',  # -> The Commander
                         ]
    student_picture = models.ImageField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    id_number = models.CharField(max_length=10)
    mentor_birthday = models.DateField()
    personality_type = models.CharField(max_length=4, choices=PERSONALITY_TYPES)
    student_code = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=13)


class Course(models.Model):
    DAY_OF_THE_WEEK = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
    course_picture = models.ImageField()
    day_of_class = models.CharField(max_length=10, choices=DAY_OF_THE_WEEK)
    time_of_class = models.CharField(max_length=10)
    course_name = models.CharField(max_length=50)
    mentor = models.CharField(max_length=20)
    description = models.TextField()
    is_course_completed = models.BooleanField(default=False)


class AdminCommentAndOrganizationalCultureModel(models.Model):
    comment = models.TextField()
    organizational_culture = models.CharField(max_length=5)












