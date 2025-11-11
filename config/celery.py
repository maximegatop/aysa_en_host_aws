from __future__ import absolute_import
 
import os
 
from celery import Celery
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings') #Nota 1
 
from django.conf import settings  # Nota 2
 
app = Celery('config') #Nota 3
 
app.config_from_object('django.conf:settings') #Nota 4
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS) #Nota 5

