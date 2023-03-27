from django.db import models


class DefineMentorModel(models.Model):
    PERSONALITY_TYPES = (
        ('INFJ', "Counselor"),
        ("ISTJ", "Inspector"),
        ("ISFJ", "Protector"),
        ('INTJ', "Mastermind"),
        ('ISTP', "Craftsman"),
        ('ISFP', "Composer"),
        ('INFP', "Healer"),
        ('INTP', "Architect"),
        ('ESTP', "Dynamo"),
        ('ESFP', "Performer"),
        ('ENFP', "Champion"),
        ('ENTP', "Visionary"),
        ('ESTJ', "Supervisor"),
        ('ESFJ', "Provider"),
        ('ENFJ', "Teacher"),
        ('ENTJ', "Commander"),
        )
    mentor_picture = models.ImageField(upload_to="")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    id_number = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=13)
    mentor_code = models.CharField(max_length=20)
    mentor_birthday = models.DateField()
    personality_type = models.CharField(max_length=4, choices=PERSONALITY_TYPES)


class DefineStudentModel(models.Model):
    PERSONALITY_TYPES = (
        ("ISTJ", "Inspector"),
        ("ISFJ", "Protector"),
        ('INFJ', "Counselor"),
        ('INTJ', "Mastermind"),
        ('ISTP', "Craftsman"),
        ('ISFP', "Composer"),
        ('INFP', "Healer"),
        ('INTP', "Architect"),
        ('ESTP', "Dynamo"),
        ('ESFP', "Performer"),
        ('ENFP', "Champion"),
        ('ENTP', "Visionary"),
        ('ESTJ', "Supervisor"),
        ('ESFJ', "Provider"),
        ('ENFJ', "Teacher"),
        ('ENTJ', "Commander"),
        )
    student_picture = models.ImageField(upload_to="task111")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    id_number = models.CharField(max_length=10)
    mentor_birthday = models.DateField()
    personality_type = models.CharField(max_length=4, choices=PERSONALITY_TYPES)
    student_code = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=13)


class Course(models.Model):
    DAY_OF_THE_WEEK = (("sunday", 'یک شنبه'), ("monday", "دو شنبه"), ("tuesday", "سه شنبه"), ("wednesday", "چهار شنبه"),
                       ("thursday", "پنج شنبه"), ("friday", "جمعه"), ("saturday", "شنبه"))
    course_picture = models.ImageField(upload_to="task111")
    class_days = models.CharField(max_length=10, choices=DAY_OF_THE_WEEK)
    time_of_class = models.CharField(max_length=10)
    course_name = models.CharField(max_length=50)
    mentor = models.CharField(max_length=20)
    description = models.TextField()
    is_course_completed = models.BooleanField(default=False)


class AdminCommentAndOrganizationalCultureModel(models.Model):
    comment = models.TextField()
    organizational_culture = models.CharField(max_length=5)
