from celery import shared_task

from task.writers import create_notification
from core.background import app


@app.task
def send_notification(user_id: int, title: str, event_type: str, event_slug: str):
    create_notification(dict(user_id=user_id, title=title, event_type=event_type, event_slug=event_slug))
    return "Notification sent!"
