from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView

from accounts.forms import UserModelForm, EmployeeForm
from task.forms import TaskForm
from task.mixins import NotificationMixin
from task.models import Task, ExternalCalendarEvent, Progress


class IndexView(NotificationMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        queryset = Progress.objects.filter(user=self.request.user)
        context['tasks_not_started'] = queryset.filter(progress=Progress.TaskProgress.NOT_STARTED).count()
        context['tasks_in_progress'] = queryset.filter(progress=Progress.TaskProgress.IN_PROGRESS).count()
        context['tasks_review'] = queryset.filter(progress=Progress.TaskProgress.REVIEW).count()
        context['tasks_completed'] = queryset.filter(progress=Progress.TaskProgress.COMPLETED).count()
        context['overdue_tasks'] = queryset.filter(progress=Progress.TaskProgress.NOT_STARTED,
                                                   task__end_date__lt=timezone.now()).count()
        context['completed_tasks_6_months'] = queryset.filter(progress=Progress.TaskProgress.COMPLETED,
                                                              created__gte=timezone.now() - timezone.timedelta(
                                                                  days=180)).count()
        context['overdue_tasks_6_months'] = queryset.filter(
            progress=Progress.TaskProgress.NOT_STARTED, task__end_date__lt=timezone.now(),
            created__gte=timezone.now() - timezone.timedelta(days=180)).count()
        return context


class TasksCalendarView(NotificationMixin, TemplateView):
    template_name = "tasks-calendar.html"

    def get_context_data(self, **kwargs):
        context = super(TasksCalendarView, self).get_context_data(**kwargs)
        context['tasks'] = Task.objects.all()
        context['google_calendar_events'] = ExternalCalendarEvent.objects.filter(user=self.request.user)
        return context


class TasksMapView(NotificationMixin, TemplateView):
    template_name = "tasks-map.html"

    def get_context_data(self, **kwargs):
        context = super(TasksMapView, self).get_context_data(**kwargs)
        context['task'] = Task.objects.last()
        context['api_key'] = settings.GOOGLE_CALENDAR_API_KEY
        return context


class TaskCreateView(NotificationMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "task-create.html"
    success_message = "Task created successfully"
    success_url = reverse_lazy("task:profile")

    def get_context_data(self, **kwargs):
        context = super(TaskCreateView, self).get_context_data(**kwargs)
        context['action'] = "Create"
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreateView, self).form_valid(form)


class TaskUpdateView(NotificationMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "task-create.html"
    success_message = "Task updated successfully"
    success_url = reverse_lazy("task:profile")

    def get_context_data(self, **kwargs):
        context = super(TaskUpdateView, self).get_context_data(**kwargs)
        context['action'] = "Update"
        return context


class ProfileView(NotificationMixin, TemplateView):
    template_name = "edit-profile.html"

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            context['form'] = UserModelForm(instance=self.request.user, data=self.request.POST)
            context['p_form'] = EmployeeForm(instance=self.request.user.employee, data=self.request.POST,
                                             files=self.request.FILES)
        else:
            context['form'] = UserModelForm(instance=self.request.user)
            context['p_form'] = EmployeeForm(instance=self.request.user.employee)
        context['task_form'] = TaskForm()
        context['tasks'] = Task.objects.filter(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = context['form']
        p_form = context['p_form']
        if form.is_valid() and p_form.is_valid():
            form.save()
            p_form.save()
            messages.success(request, "Profile updated successfully")
        return self.render_to_response(context=context)


class TaskDeleteView(SuccessMessageMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('task:profile')
    success_message = "Task deleted successfully"


class TaskEvaluationView(NotificationMixin, TemplateView):
    template_name = "task-evaluation.html"

    def get_context_data(self, **kwargs):
        context = super(TaskEvaluationView, self).get_context_data(**kwargs)
        context['task'] = Task.objects.last()
        return context


class KanbanView(NotificationMixin, TemplateView):
    template_name = "kanban.html"

    def get_context_data(self, **kwargs):
        context = super(KanbanView, self).get_context_data(**kwargs)
        context['tasks_not_started'] = Progress.objects.filter(
            user=self.request.user, progress=Progress.TaskProgress.NOT_STARTED)
        context['tasks_in_progress'] = Progress.objects.filter(
            user=self.request.user, progress=Progress.TaskProgress.IN_PROGRESS)
        context['tasks_review'] = Progress.objects.filter(
            user=self.request.user, progress=Progress.TaskProgress.REVIEW)
        context['tasks_completed'] = Progress.objects.filter(
            user=self.request.user, progress=Progress.TaskProgress.COMPLETED)
        return context
