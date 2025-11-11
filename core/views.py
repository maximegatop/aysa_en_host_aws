from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext, Context
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import AnonymousUser
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from datetime import datetime, timedelta, date
from django.utils import timezone
from django.utils.translation import gettext as _
#from suds.client import Client
#import xml.etree.ElementTree as ET
#import xmltodict
import logging
from django.views.decorators.csrf import csrf_exempt
import base64

from qorder.models import Desc_Foto, PuntoDeSuministro

log = logging.getLogger('qorderweb')

# Create your views here.
#@user_passes_test(check_admin_or_tech, login_url='/')
@csrf_exempt   #Permite que no pase el 403 forbidden
def log_in(request):
    #print('entra login')
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not username or not password:
            messages.add_message(request, messages.ERROR, 'Por favor, complete todos los campos.')
        else:
            validado = True
            if settings.VALIDAR_CON_E_SECURITY == 1:
               validado = validarUsuarioSCP(username,password)
               if not validado:
                  log.info("usuario {} validado en SCP".format(username))
                  messages.add_message(request, messages.ERROR, 'Usuario no existe')
                  return render_to_response('login.html', context)

            user = authenticate(username=username, password=password)

            if user:
                # Is the account active? It could have been disabled.
                if user.is_active:
                    # If the account is valid and active, we can log the user in.
                    # We'll send the user back to the homepage.
                    log.info("Login QOrder usuario {}".format(user))
                    login(request, user)
                    messages.add_message(request, messages.SUCCESS, 'Bienvenido {}'.format(user))
                    return redirect(settings.LOGIN_OK)

                else:
                    # An inactive account was used - no logging in!
                    log.info("Login QOrder usuario {} inactivo".format(user))
                    messages.add_message(request, messages.ERROR, 'Este usuario no está disponible')
                    return render_to_response('login.html', context)
            else:
                # Bad login details were provided. So we can't log the user in.
                log.info("Login QOrder usuario {} no existe".format(username))
                messages.add_message(request, messages.ERROR, 'No existe este usuario. Por favor, revise sus credenciales.')
                return render_to_response('login.html', context)

            # The request is not a HTTP POST, so display the login form.
            # This scenario would most likely be a HTTP GET.
    log.info("Ingreso QOrder Versión {}".format(settings.APP_VERSION))
    return render_to_response('login.html', context)

#def validarUsuarioSCP(username,password):
#    try:
#        client1 = Client(settings.URL_WS_SCP)
#        result = client1.service.login(userName=username, password=password,AppCode=APP_WS_SCP)
#        if '<loginResult>Ok</loginResult>' in result:
#            print('Entro OK')
#            log.info("SCP usuario {} OK".format(username))
#            return True
#        else:
#            log.info("SCP usuario {} no autorizado".format(username))
#    except Exception as e:
#         print("Error {}".format(e))
#         log.info("Error consultando SCP {}".format(e))
#
#    return False



#def pruebaWS(request):
#    #from pysimplesoap.client import SoapClient
#    #print('pruebaWS')
#    #client = SoapClient(wsdl="https://svn.apache.org/repos/asf/airavata/sandbox/xbaya-web/test/Calculator.wsdl",trace=True)
#    #print(client)
#    #response = client.addRequest()
#    #result = response['AddResult']
#    #print(result)
#    client1 = Client(settings.URL_WS_SCP)
#   
#    print('------------------')
#
#
#    print('***************')
#    result = client1.service.login(userName='victor', password='catbob',AppCode='')
#    if '<loginResult>Ok</loginResult>' not in result:
#        print('Entro OK')
#    else:
#        print('No autorizado')
#    print('***************')
#    #result = client1.service.getRolesByUser(userName='victor', AppCode='')
#    #print(result)
#    
#    #xml = ET.fromstring(result)
#    #data = xmltodict.parse(result,item_depth=3, item_callback=handle_artist)
#
#    #print('------------------')
#    #required_dict = Client.dict(client1.service.getRolesByUser(userName='victor', AppCode=''))
#    #print(required_dict)
    
def handle_artist(_, artist):
    
    #print(artist['getRolesByUserResult'])
    #for item in artist['getRolesByUserResult']:
        #print(item)
    return True
@csrf_exempt
def log_out(request):
    #print('llega logout')
    log.info("Logout QOrder usuario {}".format(request.user))
    logout(request)
    context = RequestContext(request)

    messages.add_message(request, messages.SUCCESS, 'Muchas gracias!')
    return redirect(settings.LOGIN_OK)

@login_required(login_url=settings.LOGIN_PAGE)
def index(request):
    context = RequestContext(request)
    print('llega')
    context['version'] = settings.APP_VERSION
    context['MINUTOS_INACTIVIDAD'] = settings.MINUTOS_INACTIVIDAD
    return render_to_response('base.html', context)


def foto(request):

    context = RequestContext(request)

    numOrden=request.GET.get('numOrden')
    
    q=Desc_Foto.objects.filter( orden_trabajo = numOrden
                        ).values('foto',
                                'orden_trabajo__punto_suministro__num_contrato',
                                'orden_trabajo__punto_suministro__aparato__num_serie'
                                )
    
    
    fotos=[]

    for foto in q:
        fotos.append({"foto":foto['foto'], 
                      "contrato":foto['orden_trabajo__punto_suministro__num_contrato'],
                      "numeroSerie":foto['orden_trabajo__punto_suministro__aparato__num_serie']})
    
    
    context['fotos']=fotos

    return render_to_response('verfoto.html', context)

