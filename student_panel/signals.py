from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Report
import datetime
from .tasks import add_unsubmitted_report
from .models import Payment
from django.utils import timezone
from datetime import timedelta


def create_monthly_receipts(course):
    start_date = course.start_date
    end_date = course.end_date
    for i in range(6):
        month_number = i + 1
        month_start_date = start_date + datetime.timedelta(days=30 * i)
        month_end_date = start_date + datetime.timedelta(days=30 * (i + 1))
        if month_end_date > end_date:
            month_end_date = end_date
        Payment.objects.create(user=course.user, course=course, month_number=month_number,
                               start_at=month_start_date, end_date=month_end_date)


@receiver(post_save, sender=Payment)
def monthly_receipt_saved(sender, instance, created, **kwargs):
    if created:
        if instance.receipt_image:
            # Update monthly receipt status to "completed"
            instance.status = 'completed'
            instance.save()


# @receiver(post_save, sender=Report)
# def update_student_report_count(sender, instance, created, **kwargs):
#     if created:
#         student = instance.student
#         student.report_count += 1
#         student.save()


@receiver(post_save, sender=Report)
def report_saved(sender, instance, **kwargs):
    # Schedule the task to run in 24 hours
    add_unsubmitted_report.apply_async(args=[instance.student_id], eta=timezone.now() + timezone.timedelta(days=1))
