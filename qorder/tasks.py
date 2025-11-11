from celery import shared_task
from config.celery import app
from qorder import *
from qorder.importador import *
from django.views.decorators.csrf import csrf_exempt


@shared_task
def inicia_import(_ruta,lista1,oficina,user):
  #print('llega import')
  return parceararchivo(_ruta,lista1,oficina,user)
