from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Exam, StudentExerciseModel




@receiver(post_save, sender=StudentExerciseModel)
def set_is_done_exercise(sender, instance, created, **kwargs):
    if created:
        instance.is_done_exercise = True
        instance.save()




# @receiver(pre_save, sender=Exam)
# def generate_exam_number(sender, instance, **kwargs):
#     if not instance.exam_number:
#         last_exam = Exam.objects.order_by('exam_number').last()
#         if last_exam:
#             instance.exam_number = last_exam.exam_number + 1
#         else:
#             instance.exam_number = 1









# @receiver(post_save, sender=StudentExerciseModel)
# def set_done_student(sender, instance, **kwargs):
#     exercise = instance.exercise
#     exercise.is_done_exercise = True
#     exercise.save()
