import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cms.cms.settings.py')

celery = Celery('cms', broker='redis://127.0.0.1:6379/15', backend='redis://127.0.0.1:6379/14')


celery.autodiscover_tasks(['asy'])