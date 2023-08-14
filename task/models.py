from django.contrib.gis.db.models import PointField
from django.db import models

from core.utils import TimeStampModel


class Location(TimeStampModel):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    county = models.CharField(max_length=100, null=True, blank=True)
    postcode = models.CharField(max_length=100, null=True, blank=True)
    coordinates = PointField()

    def __str__(self):
        return self.name


class Task(TimeStampModel):
    class TaskPriority(models.IntegerChoices):
        LOW = 1, 'Low'
        MEDIUM = 2, 'Medium'
        HIGH = 3, 'High'

    class TaskType(models.TextChoices):
        PERSONAL = 'personal', 'Personal'
        WORK = 'work', 'Work'

    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='tasks')
    end_date = models.DateTimeField()
    start_date = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='tasks')
    priority = models.IntegerField(choices=TaskPriority.choices, default=TaskPriority.LOW)
    task_type = models.CharField(max_length=100, choices=TaskType.choices, default=TaskType.WORK)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Progress(TimeStampModel):
    class TaskProgress(models.IntegerChoices):
        NOT_STARTED = 0, 'Not Started'
        IN_PROGRESS = 1, 'In Progress'
        REVIEW = 2, 'Review'
        COMPLETED = 3, 'Completed'

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='progresses')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='progresses')
    progress = models.IntegerField(choices=TaskProgress.choices, default=TaskProgress.NOT_STARTED)
    completion_date = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.task.title} - {self.user.email}"


class UserGoogleCredentials(TimeStampModel):
    class AccountType(models.TextChoices):
        GOOGLE_CALENDAR = 'google_calendar', 'Google Calendar'
        MICROSOFT_CALENDAR = 'microsoft_calendar', 'Microsoft Calendar'

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255, null=True, blank=True)
    refresh_token = models.CharField(max_length=255, null=True, blank=True)
    token_uri = models.CharField(max_length=255, null=True, blank=True)
    client_id = models.CharField(max_length=255, null=True, blank=True)
    client_secret = models.CharField(max_length=255, null=True, blank=True)
    scopes = models.TextField(null=True, blank=True)
    expiry = models.DateTimeField(null=True, blank=True)
    account_type = models.CharField(max_length=100, choices=AccountType.choices, default=AccountType.GOOGLE_CALENDAR)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'User Account Credentials'
        verbose_name_plural = 'User Account Credentials'


class ExternalCalendarEvent(TimeStampModel):
    class CalendarType(models.TextChoices):
        GOOGLE_CALENDAR = 'google_calendar', 'Google Calendar'
        MICROSOFT_CALENDAR = 'microsoft_calendar', 'Microsoft Calendar'

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='external_calendar_events')
    event_id = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name='external_calendar_events', null=True, blank=True
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_all_day = models.BooleanField(default=False)
    is_recurring = models.BooleanField(default=False)
    html_link = models.CharField(max_length=255, null=True, blank=True)
    recurrence = models.CharField(max_length=100, blank=True, null=True)
    meeting_link = models.CharField(max_length=255, null=True, blank=True)
    calendar_type = models.CharField(max_length=100, choices=CalendarType.choices, default=CalendarType.GOOGLE_CALENDAR)

    def __str__(self):
        return f"{self.title} - {self.user.email}"


class Notification(TimeStampModel):
    class EventTypes(models.TextChoices):
        TASK_EVENT = 'task_event', 'Task Event'
        GOOGLE_CALENDAR_EVENT = 'google_calendar_event', 'Google Calendar Event'
        MICROSOFT_CALENDAR_EVENT = 'microsoft_calendar_event', 'Microsoft Calendar Event'

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='notifications')
    event_slug = models.CharField(max_length=255)
    event_type = models.CharField(max_length=100, choices=EventTypes.choices, default=EventTypes.TASK_EVENT,
                                  null=True, blank=True)
    title = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.title}"


class Reminder(TimeStampModel):
    name = models.CharField(max_length=100)
    location = PointField()
    description = models.TextField()

    def __str__(self):
        return self.name
