from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User, Employee


@receiver(post_save, sender=User, dispatch_uid="create_user_profiles")
def create_user_profiles(sender, instance, created, **kwargs):
    if created:
        match instance.type:
            case "EMP":
                Employee.objects.get_or_create(user=instance)
            case _:
                pass
