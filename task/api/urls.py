from django.urls import path

from task.api.views import LocationListAPIView, TaskListCreateAPIView, TaskRetrieveUpdateDestroyAPIView, \
    CalendarTaskListAPIView, CalendarEventsListAPIView, TaskProgressListAPIView, TaskProgressUpdateAPIView, \
    TasksEvaluationAPIView, DashboardAPIView
from task.notification import SubscriptionView, SendNotificationView

urlpatterns = [
    path('dashboard/', DashboardAPIView.as_view()),
    path('locations/', LocationListAPIView.as_view()),
    path('calendar-tasks/', CalendarTaskListAPIView.as_view()),
    path('calendar-events/', CalendarEventsListAPIView.as_view()),
    path('task-progress/', TaskProgressListAPIView.as_view()),
    path('task-progress/<str:slug>/', TaskProgressUpdateAPIView.as_view()),
    path('tasks/', TaskListCreateAPIView.as_view()),
    path('tasks-evaluation/', TasksEvaluationAPIView.as_view()),
    path('tasks/<slug>/', TaskRetrieveUpdateDestroyAPIView.as_view()),
    path('subscribe/', SubscriptionView.as_view(), name='subscribe'),
    path('send_notification/', SendNotificationView.as_view(), name='send_notification'),
]
