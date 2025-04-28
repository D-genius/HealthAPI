import os
import time
from celery import Celery
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare.settings')
FIELD_ENCRYPTION_KEY = os.getenv('FIELD_ENCRYPTION_KEY')

app = Celery('healthcare')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
# time.sleep(5)