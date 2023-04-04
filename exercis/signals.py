from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import MentorExerciseModel, StudentExerciseModel

@receiver(post_save, sender=StudentExerciseModel)
def mark_exercise_as_seen(sender, instance, created, **kwargs):
    if not created:
        mentor_exercise = MentorExerciseModel.objects.filter(student_name=instance.student).first()
        if mentor_exercise:
            instance.is_seen_by_mentor = True
            instance.save()


@receiver(post_save, sender=StudentExerciseModel)
def set_done_student(sender, instance, **kwargs):
    exercise = instance.exercise
    exercise.is_done_exercise = True
    exercise.save()

