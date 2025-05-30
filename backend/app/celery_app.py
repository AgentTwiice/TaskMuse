import os
from celery import Celery

celery_app = Celery(
    'taskmuse',
    broker=os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0'),
    backend=os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
)

celery_app.conf.beat_schedule = {
    'send-due-task-notifications': {
        'task': 'app.tasks.send_due_task_notifications',
        'schedule': 60.0,  # every minute
    }
}
