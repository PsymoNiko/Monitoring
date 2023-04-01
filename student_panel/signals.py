# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Report
#
#
# @receiver(post_save, sender=Report)
# def increment_report_number(sender, instance, created, **kwargs):
#     if created:
#         instance.user.first_name.report_count += 1
#         instance.user.first_name.save()
#         instance.report_number = instance.user.first_name.report_count
#         instance.save()
