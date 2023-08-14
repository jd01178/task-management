from django.utils import timezone
from datetime import timedelta

from task.models import Progress


def get_progress_data(task_type, duration, user_id):
    today = timezone.now()
    start_date = today - timedelta(days=duration)

    # Filter Progress objects based on the specified interval
    progress_data = Progress.objects.filter(
        user_id=user_id,
        created__gte=start_date,
        created__lte=today, task__task_type=task_type
    )

    # Count occurrences of each progress status for the specified interval
    progress_count = [[f"data{status + 1}", progress_data.filter(progress=status).count()] for status in
                      Progress.TaskProgress.values]

    return progress_count
