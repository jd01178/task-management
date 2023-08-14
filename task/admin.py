from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.gis.admin import OSMGeoAdmin

from accounts.mixins import ExportCsvMixin
from task.models import Location, Task, Progress, ExternalCalendarEvent, UserGoogleCredentials, Notification, Reminder


@admin.register(Location)
class LocationAdmin(ExportCsvMixin, OSMGeoAdmin):
    search_fields = ['name']
    search_help_text = "Search by name"
    list_display = ('slug', 'name', 'coordinates', 'created', 'updated')
    list_display_links = ['slug', 'name']
    list_filter = ('updated', 'created')
    actions = ['export_as_csv']


@admin.register(Task)
class TaskAdmin(ExportCsvMixin, ModelAdmin):
    search_fields = ['title']
    search_help_text = "Search by title"
    list_display = ('slug', 'title', 'description', 'location', 'end_date', 'priority', 'created', 'updated')
    list_display_links = ['slug', 'title']
    list_filter = ('task_type', 'is_completed', 'end_date', 'priority', 'updated', 'created')
    actions = ['export_as_csv']


@admin.register(Progress)
class ProgressAdmin(ExportCsvMixin, ModelAdmin):
    search_fields = ['task__title', 'user__email']
    search_help_text = "Search by task title or user email"
    list_display = ('slug', 'task', 'user', 'completion_date', 'is_completed', 'created', 'updated')
    list_display_links = ['slug', 'task']
    list_filter = ('is_completed', 'completion_date', 'updated', 'created')
    actions = ['export_as_csv']


@admin.register(ExternalCalendarEvent)
class ExternalCalendarEventAdmin(ExportCsvMixin, ModelAdmin):
    search_fields = ['title', 'user__email']
    search_help_text = "Search by title or user email"
    list_display = ('slug', 'user', 'event_id', 'title', 'description', 'location', 'start_date', 'end_date',
                    'is_all_day', 'is_recurring', 'recurrence', 'created', 'updated')
    list_display_links = ['slug', 'title']
    list_filter = ('is_all_day', 'is_recurring', 'updated', 'created')
    actions = ['export_as_csv']


@admin.register(UserGoogleCredentials)
class UserGoogleCredentialsAdmin(ExportCsvMixin, ModelAdmin):
    search_fields = ['user__email']
    search_help_text = "Search by user email"
    list_display = (
        'slug', 'user', 'account_type', 'access_token', 'refresh_token', 'token_uri', 'client_id', 'client_secret',
        'created', 'updated'
    )
    list_display_links = ['slug', 'user']
    list_filter = ('updated', 'created')
    actions = ['export_as_csv']


@admin.register(Notification)
class NotificationAdmin(ExportCsvMixin, ModelAdmin):
    search_fields = ['user__email', 'title']
    search_help_text = "Search by user email or event title"
    list_display = ('slug', 'user', 'event_slug', 'title', 'is_read', 'created', 'updated')
    list_display_links = ['slug', 'user']
    list_filter = ('is_read', 'updated', 'created')
    actions = ['export_as_csv']


@admin.register(Reminder)
class ReminderAdmin(ExportCsvMixin, OSMGeoAdmin):
    search_fields = ['name']
    search_help_text = "Search by name"
    list_display = ('slug', 'name', 'location', 'description', 'created', 'updated')
    list_display_links = ['slug', 'name']
    list_filter = ('updated', 'created')
    actions = ['export_as_csv']
