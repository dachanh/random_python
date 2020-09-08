from celery import Celery

celery = Celery('simpile celery',include=['server_flask.tasks'])