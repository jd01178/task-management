from django.urls import path

from accounts.decorators import decorate_url_patterns
from task.calendar import google_authenticate, google_callback, fetch_google_calendar_events
from task.views import IndexView, TasksCalendarView, TasksMapView, TaskCreateView, TaskUpdateView, ProfileView, \
    TaskDeleteView, TaskEvaluationView, KanbanView

app_name = 'task'

restricted_urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('task-progress/', KanbanView.as_view(), name='kanban'),
    path('tasks-evaluation/', TaskEvaluationView.as_view(), name='tasks_evaluation'),
    path('tasks-calendar/', TasksCalendarView.as_view(), name='tasks_calendar'),
    path('tasks-map/', TasksMapView.as_view(), name='tasks_map'),
    path('task-create/', TaskCreateView.as_view(), name='task_create'),
    path('task-delete/<str:slug>/', TaskDeleteView.as_view(), name='task_delete'),
    path('task-update/<str:slug>/', TaskUpdateView.as_view(), name='task_update'),
    path('google/auth/', google_authenticate, name='google_authenticate'),
    # URL to handle the Google OAuth2 callback
    path('google/callback/', google_callback, name='google_callback'),
    path('google-calendar-events/<int:user_id>/', fetch_google_calendar_events, name='fetch_google_calendar_events'),
    path('profile/', ProfileView.as_view(), name='profile'),
]

urlpatterns = decorate_url_patterns(patterns=restricted_urlpatterns, user_type="EMP")
