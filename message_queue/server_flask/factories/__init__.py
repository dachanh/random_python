
import os

class Config:
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://127.0.0.1:6379/0')
    CELERY_ACCEPT_CONTENT = ['json', 'yaml']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_IMPORTS = ('server_flask.tasks',)
