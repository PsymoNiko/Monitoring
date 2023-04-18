from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import MentorExerciseModel, StudentExerciseModel




@receiver(post_save, sender=StudentExerciseModel)
def set_is_done_exercise(sender, instance, created, **kwargs):
    if created:
        instance.is_done_exercise = True
        instance.save()













# @receiver(post_save, sender=StudentExerciseModel)
# def set_done_student(sender, instance, **kwargs):
#     exercise = instance.exercise
#     exercise.is_done_exercise = True
#     exercise.save()

