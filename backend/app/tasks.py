from datetime import datetime, timedelta
import os
import requests

from .celery_app import celery_app
from .storage import push_tokens, tasks

EXPO_PUSH_URL = os.environ.get('EXPO_PUSH_URL', 'https://exp.host/--/api/v2/push/send')

@celery_app.task
def send_due_task_notifications():
    now = datetime.utcnow()
    upcoming = now + timedelta(minutes=30)
    count = 0
    for task in tasks:
        due = task.get('due')
        if due and now <= due <= upcoming:
            token = push_tokens.get(task.get('user_id'))
            if token:
                requests.post(EXPO_PUSH_URL, json={
                    'to': token,
                    'title': 'Task Reminder',
                    'body': task.get('title', '')
                })
                count += 1
    return count
