from task.models import Notification


def create_notification(kwargs: dict) -> Notification:
    notification, _ = Notification.objects.get_or_create(**kwargs)
    return notification
