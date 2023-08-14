import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
# this is also used in manage.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
app.conf.broker_transport_options = {'visibility_timeout': 43200}
app.conf.broker_transport_options = {'fanout_prefix': True}
app.conf.broker_transport_options = {'fanout_patterns': True}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
