from task.models import Notification


class NotificationMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notifications'] = Notification.objects.filter(user=self.request.user, is_read=False)
        return context
