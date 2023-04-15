from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Report


# @receiver(post_save, sender=Report)
# def update_is_submitted(sender, instance, created, **kwargs):
#     if created and not instance.is_submitted:
#         instance.is_submitted = True
#         instance.save()
@receiver(post_save, sender=Report)
def update_created_through_command(sender, instance, **kwargs):
    if kwargs.get('created', False):
        # If the student object is being created, do not update the field
        return
    instance.created_through_command = False
    instance.save()


