from django.forms import ModelForm

from task.models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'location', 'start_date', 'end_date', 'priority', 'task_type')
