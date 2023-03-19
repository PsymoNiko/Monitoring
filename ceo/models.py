from django.db import models


class AdminCommentModel(models.Model):
    comment = models.TextField()

    def __str__(self):
        return f"{self.comment}"


# class StudentInformationModel(models.Model):
#     student_name = models.CharField(max_length=100)
#     id_card_number = models.CharField(max_length=10, unique=True)
#     phone_number = models.CharField(max_length=13)
#     personality_type = models.CharField(max_length=4)
#     password = models.CharField(max_length=20)
#     username = models.CharField(max_length=8)
#     birthday = models.TimeField()


class MentorInformationModel(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    id_card_number = models.CharField(max_length=10, unique=True)
    phone_number = models.CharField(max_length=13)
    personality_type = models.CharField(max_length=4)
    birthday = models.TimeField()




