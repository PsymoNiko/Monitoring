from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MentorReportSubmission

@receiver(post_save, sender=MentorReportSubmission)
def is_not_send_reports_student(sender, instance, **kwargs):
    if not instance.Is_send_student:
        instance.user.is_not_sent_student += 1
        instance.user.save()






