from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.permissions import IsEmployeeUser
from task.api.serializers import LocationSerializer, TaskSerializer, CalendarTaskSerializer, CalendarEventsSerializer, \
    TaskProgressSerializer
from task.models import Location, Task, ExternalCalendarEvent, Progress
from task.utils import get_progress_data


class LocationListAPIView(ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated, IsEmployeeUser]
    search_fields = ['name', 'address', 'city', 'state', 'zip_code']

    def get_queryset(self):
        return Location.objects.all().order_by('name')


class TaskListCreateAPIView(ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsEmployeeUser]
    search_fields = ['title']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by('-created')


class TaskRetrieveUpdateDestroyAPIView(ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsEmployeeUser]
    search_fields = ['title']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by('-created')


class CalendarTaskListAPIView(ListAPIView):
    serializer_class = CalendarTaskSerializer
    permission_classes = [IsAuthenticated, IsEmployeeUser]
    search_fields = ['title']

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by('-created')


class CalendarEventsListAPIView(ListAPIView):
    serializer_class = CalendarEventsSerializer
    permission_classes = [IsAuthenticated, IsEmployeeUser]
    search_fields = ['title']

    def get_queryset(self):
        return ExternalCalendarEvent.objects.filter(user=self.request.user).order_by('-created')


class TasksEvaluationAPIView(APIView):
    permission_classes = [IsAuthenticated, IsEmployeeUser]

    def get(self, request, *args, **kwargs):
        context = dict(daily=get_progress_data(task_type="work", duration=1, user_id=self.request.user.id),
                       weekly=get_progress_data(task_type="work", duration=7, user_id=self.request.user.id),
                       monthly=get_progress_data(task_type="work", duration=30, user_id=self.request.user.id),
                       personal_daily=get_progress_data(task_type="personal", duration=1,
                                                        user_id=self.request.user.id),
                       personal_weekly=get_progress_data(task_type="personal", duration=7,
                                                         user_id=self.request.user.id),
                       personal_monthly=get_progress_data(task_type="personal", duration=30,
                                                          user_id=self.request.user.id))
        return Response(data=context, status=status.HTTP_200_OK)


class TaskProgressListAPIView(ListAPIView):
    serializer_class = TaskProgressSerializer
    permission_classes = [IsAuthenticated, IsEmployeeUser]

    def get_queryset(self):
        return Progress.objects.filter(user=self.request.user).order_by('-created')


class TaskProgressUpdateAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TaskProgressSerializer
    permission_classes = [IsAuthenticated, IsEmployeeUser]
    lookup_field = 'slug'

    def get_queryset(self):
        return Progress.objects.filter(user=self.request.user).order_by('-created')


class DashboardAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        context = dict()
        if self.request.user.is_authenticated:
            queryset = Progress.objects.filter(user=self.request.user)
            # Filter data for the current year
            current_date = timezone.now()
            start_date = datetime(current_date.year, 1, 1)
            end_date = datetime(current_date.year, 12, 31, 23, 59, 59)
            queryset = queryset.filter(updated__range=(start_date, end_date))
            completed_tasks_1_year = queryset.filter(progress=Progress.TaskProgress.COMPLETED).count()
            overdue_tasks_1_year = queryset.filter(progress=Progress.TaskProgress.NOT_STARTED,
                                                   task__end_date__lt=timezone.now()).count()

            completed_tasks_percentage = 0
            if completed_tasks_1_year > 0:
                completed_tasks_percentage = completed_tasks_1_year / (completed_tasks_1_year + overdue_tasks_1_year) * 100

            # Create a list of all months in the current year
            all_months = [start_date + relativedelta(months=i) for i in range(12)]
            # Get the completed tasks count per month
            completed_tasks_over_a_year = queryset.filter(progress=Progress.TaskProgress.COMPLETED).annotate(
                month=TruncMonth('updated')).values('month').annotate(c=Count('id')).values('c', 'month').order_by(
                'month')

            # Get the overdue tasks count per month
            overdue_tasks_over_a_year = queryset.filter(progress=Progress.TaskProgress.NOT_STARTED,
                                                        task__end_date__lt=timezone.now()).annotate(
                month=TruncMonth('created')).values('month').annotate(c=Count('id')).values('c', "month").order_by('month')
            # Create a list to store the final count for completed tasks for all months
            completed_task_counts_for_all_months = [0 for index in range(12)]

            # Create a list to store the final count for overdue tasks for all months
            overdue_task_counts_for_all_months = [0 for index in range(12)]
            for count in completed_tasks_over_a_year:
                # Get the index of the month in the list of all months
                index = count['month'].month - 1
                completed_task_counts_for_all_months[index] = count['c']
            # Create a dictionary to map month to count for overdue tasks
            for count in overdue_tasks_over_a_year:
                # Get the index of the month in the list of all months
                # Get the index of the month in the list of all months
                index = count['month'].month - 1
                overdue_task_counts_for_all_months[index] = count['c']

            context = dict(
                completed_tasks_percentage=completed_tasks_percentage,
                completed_task_counts_for_all_months=completed_task_counts_for_all_months,
                overdue_task_counts_for_all_months=overdue_task_counts_for_all_months
            )
        return Response(data=context, status=status.HTTP_200_OK)
