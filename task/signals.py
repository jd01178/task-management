# models.py
import datetime
from typing import List

from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from task.models import ExternalCalendarEvent, Task, Progress, Notification
from task.tasks import send_notification


def get_notification_task_args(instance, event_type, event_slug) -> List:
    """
    Create the task args for the celery background tasks
    :param event_slug:
    :param event_type:
    :param instance: Task instance
    :return: List
    """
    tasks_args = [instance.user.id, str(instance.title), str(event_type), str(event_slug)]
    return tasks_args


@receiver(post_save, sender=ExternalCalendarEvent)
def add_background_task_on_save(sender, instance, **kwargs):
    event_type = Notification.EventTypes.GOOGLE_CALENDAR_EVENT
    if instance.calendar_type == ExternalCalendarEvent.CalendarType.MICROSOFT_CALENDAR:
        event_type = Notification.EventTypes.MICROSOFT_CALENDAR_EVENT
    tasks_args = get_notification_task_args(instance, event_type=event_type, event_slug=instance.slug)
    an_hour_before = instance.start_date - datetime.timedelta(hours=1)
    transaction.on_commit(lambda: send_notification.apply_async(args=tasks_args, eta=an_hour_before,
                                                                task_id=f"event_{instance.slug}"))


@receiver(post_save, sender=Task, dispatch_uid="create_task_progress")
def create_task_progress(sender, instance, created, **kwargs):
    if created:
        progress, _ = Progress.objects.get_or_create(task=instance, user=instance.user, progress=0)
        tasks_args = get_notification_task_args(
            instance, event_type=Notification.EventTypes.TASK_EVENT, event_slug=instance.slug)
        an_hour_before = instance.start_date - datetime.timedelta(hours=1)
        send_notification.apply_async(args=tasks_args, eta=an_hour_before, task_id=f"task_{instance.slug}")
