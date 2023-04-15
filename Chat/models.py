from django.contrib.auth.models import User
from django.db import models
from ceo.models import Course
from mentor.models import Mentor
from student.models import Student


class Room(models.Model):
    name = models.CharField(max_length=128)
    online = models.ManyToManyField(to=User, blank=True)

    def get_online_count(self):
        return self.online.count()

    def join(self, user):
        self.online.add(user)
        self.save()

    def leave(self, user):
        self.online.remove(user)
        self.save()

    def __str__(self):
        return f'{self.name} ({self.get_online_count()})'


class Message(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content} [{self.timestamp}]'

# class Chat(models.Model):
#     student = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='student_chat')
#     mentor = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='mentor_chat')
#     students = models.OneToOneField(Mentor, on_delete=models.CASCADE)


# Create your models here.
