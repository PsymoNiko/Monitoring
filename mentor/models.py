from django.db import models


class MentorCommentModel(models.Model):
    advice = models.TextField()
