import mimetypes
from qorder.reportController import reporte_controller
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext, Context
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from django.db.models import Q
from django.db import transaction
from datetime import timedelta, date, datetime
import json
from django.utils.timezone import now
from django.utils import timezone
from django.contrib import messages
from qorder.models import *
from core.models import *
from qorder.forms import *
import math
from django.http import JsonResponse
from qorder.moduloImport import *
from qorder.moduloExport import *
from django_datatables_view.base_datatable_view import BaseDatatableView
from operator import itemgetter
from django.utils.safestring import SafeString
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, Count, Case, When, IntegerField
import urllib
from qorder.importador import *
from django.db import connection
import logging
from api.log import *
import operator
from os import listdir
from os.path import isfile, join
import glob
import os
from qorder.tasks import *
import hashlib
import shutil
import os, re, os.path, tempfile, zipfile
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
import json
import base64
from django.db.utils import IntegrityError
import random
import re
import requests
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from collections import defaultdict

_ruta1 = ''
log = logging.getLogger('qorderweb')


def query_to_dicts(query_string, *query_args):
    # print('query_string {}'.format(query_string))
    # print('query_args {}'.format(query_args))
    cursor = connection.cursor()
    cursor.execute(query_string, query_args)
    col_names = [desc[0] for desc in cursor.description]
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        row_dict = dict(zip(col_names, row))
        yield row_dict
    return


def writeAudit(actividad, accion, usuario, datos):
    Log_Auditoria(fh_registro=datetime.now(), actividad=actividad, accion=accion, usuario=usuario, datos=datos).save()


class orderListJson(BaseDatatableView):
    model = OrdenDeTrabajo
    columns = ['numero_orden', 'punto_suministro.punto_suministro', 'punto_suministro.num_contrato',
               'secuencial_registro', 'punto_suministro.aparato.num_serie', 'punto_suministro.cliente.apellido_1',
               'punto_suministro.calle', 'punto_suministro.numero_puerta', 'punto_suministro.municipio']
    order_columns = ['numero_orden', 'punto_suministro.punto_suministro', 'punto_suministro.num_contrato',
                     'secuencial_registro', 'punto_suministro.aparato.num_serie', 'punto_suministro.cliente',
                     'punto_suministro.calle', 'punto_suministro.numero_puerta', 'punto_suministro.municipio']

    def get_initial_queryset(self):
        # return queryset used as base for futher sorting/filtering
        # these are simply objects displayed in datatable
        # You should not filter data returned here by any filter values entered by user. This is because
        # we need some base queryset to count total number of records.
        try:
            ordenes = []
            if 'tipo' in self.request.session:
                tipo = self.request.session['tipo']
            if 'id_tecnico' in self.request.session:
                id_tecnico = self.request.session['id_tecnico']

            if len(id_tecnico) == 0:
                return HttpResponse(status=302)

            tecnico = Tecnico.objects.get(pk=id_tecnico)
            # log.error("TIPO {}".format(tipo))
            if int(tipo) == 0:  # asignadas
                ordenes = OrdenDeTrabajo.objects.filter(tecnico=tecnico).extra(where=['estado = 3'])
            elif int(tipo) == 1:  # cargadas
                ordenes = OrdenDeTrabajo.objects.filter(tecnico=tecnico).extra(where=['estado = 7'])
            elif int(tipo) == 2:  # trabajadas
                ordenes = OrdenDeTrabajo.objects.filter(tecnico=tecnico).extra(where=['estado = 9  OR estado = 17'])
            elif int(tipo) == 3:  # lista para exportar
                # print('estado = 256 OR estado = 273')
                ordenes = OrdenDeTrabajo.objects.filter(tecnico=tecnico).extra(where=['estado = 265 OR estado = 273'])
            elif int(tipo) == 4:  # exportadas
                hoy = datetime.now().strftime("%Y%m%d000000")
                # print('estado = 777 OR estado = 785 OR estado= 913 OR estado = 905')
                ordenes = OrdenDeTrabajo.objects.filter(tecnico=tecnico, fecha_hora_exportacion__gte=hoy).extra(
                    where=['estado = 777 OR estado = 785 OR estado= 913 OR estado = 905'])
            # print(ordenes)
            return ordenes
        except Exception as e:
            log.error("Excepcion {}".format(e))
        # OrdenDeTrabajo.objects.filter(something=self.kwargs['something'])

    '''
  def render_column(self, row, column):
    # We want to render user as a custom column
    #print(row.punto_suministro.cliente)
    if column == 'user':
       nombre = 'afdf'
       #Cliente.objects.get(id=row.punto_suministro.cliente)
       return '{0}'.format(nombre)
    else:
       return super(orderListJson, self).render_column(row, column)
  '''

    def filter_queryset(self, qs):
        # print(qs.punto_suministro)
        sSearch = self.request.GET.get('sSearch', None)
        if sSearch:
            # qs = qs.filter(numero_orden__contains=sSearch )
            qs = qs.filter(punto_suministro__calle__contains=sSearch)
        # _odt = PuntoSuministro.objects.select_related('punto_suministro__aparato').filter(calle = sSearch)
        # _odt = PuntoDeSuministro.objects.filter(qs.punto_suministro)
        # print(_odt)
        return qs

    '''
  def filter_queryset(self, qs):
    # use parameters passed in GET request to filter queryset

    # simple example:
    search = self.request.GET.get(u'search[value]', None)
    print(search)
    if search:
      qs = qs.filter(numero_orden__istartswith=search)
    return qs

      # more advanced example using extra parameters
      filter_customer = self.request.GET.get(u'customer', None)

      if filter_customer:
        customer_parts = filter_customer.split(' ')
        qs_params = None
        for part in customer_parts:
          q = Q(customer_firstname__istartswith=part)|Q(customer_lastname__istartswith=part)
          qs_params = qs_params | q if qs_params else q
          qs = qs.filter(qs_params)
          return qs
  '''


class suminListJson(BaseDatatableView):
    model = OrdenDeTrabajo
    columns = ['punto_suministro.punto_suministro', 'punto_suministro.num_contrato',
               'punto_suministro.aparato.num_serie', 'punto_suministro.calle', 'numero_orden']
    order_columns = ['punto_suministro.punto_suministro', 'punto_suministro.num_contrato',
                     'punto_suministro.aparato.num_serie', 'punto_suministro.calle']
    max_display_length = 20

    def get_initial_queryset(self):
        # return queryset used as base for futher sorting/filtering
        # these are simply objects displayed in datatable
        # You should not filter data returned here by any filter values entered by user. This is because
        # we need some base queryset to count total number of records.
        try:
            sumin = []
            todas = '2'
            if 'id_ruta' in self.request.session:
                id_ruta = self.request.session['id_ruta']
            if 'todas' in self.request.session:
                todas = self.request.session['todas']

            # print("Id ruta {} todas {}".format(id_ruta,todas))
            if len(id_ruta) == 0:
                return HttpResponse(status=302)
            ruta = Ruta.objects.get(pk=id_ruta)
            # print(str(ruta))
            if todas == '2':
                # print("entro sin filtro")
                sumin = OrdenDeTrabajo.objects.filter(ruta=ruta)
            else:
                # print("entro con filtro")
                sumin = OrdenDeTrabajo.objects.filter(ruta=ruta).extra(where=['estado = 9 or estado=17'])

            # print("Len {}".format(len(sumin)))
            return sumin
        except Exception as e:
            log.error("Excepcion {}".format(e))
        # OrdenDeTrabajo.objects.filter(something=self.kwargs['something'])

    def render_column(self, row, column):
        # We want to render user as a custom column
        # print(row.punto_suministro.cliente)
        if column == 'punto_suministro.calle':
            nombre = ' '

            desc = Desc_Lectura.objects.filter(orden_trabajo=row.numero_orden)
            if desc:
                for d in desc:
                    if d.resultado_lectura == 2:
                        nombre = 'Alto consumo'
                    elif d.resultado_lectura == 1:
                        nombre = 'Lectura normal'
                    elif d.resultado_lectura == 3:
                        nombre = 'Lectura menor'
                    elif d.resultado_lectura == 4:
                        nombre = 'Sin Lectura'
                    elif d.resultado_lectura == 5:
                        nombre = 'Lectura sin Controles'
                    else:
                        nombre = str(d.resultado_lectura)
            else:
                nombre = '--'
            return '{0}'.format(nombre)
        else:
            return super(suminListJson, self).render_column(row, column)

    def filter_queryset(self, qs):

        sSearch = self.request.GET.get('sSearch', None)

        if sSearch:
            campos = sSearch.split(":")
            # print(campos)
            if len(campos) == 1:
                qs = qs.filter(punto_suministro__punto_suministro__contains=sSearch)
            else:
                if campos[0] == 'O':
                    if campos[1] != None:
                        qs = qs.filter(numero_orden__contains=campos[1])
                elif campos[0] == 'S':
                    if campos[1] != None:
                        qs = qs.filter(punto_suministro__aparato__num_serie__contains=campos[1])
                elif campos[0] == 'E':

                    if campos[1] != None:
                        resultado_lectura = 0
                        if campos[1] == 'A':
                            resultado_lectura = 2
                        elif campos[1] == 'N':
                            resultado_lectura = 1
                        elif campos[1] == 'M':
                            resultado_lectura = 3
                        elif campos[1] == 'S':
                            resultado_lectura = 4
                        elif campos[1] == 'C':
                            resultado_lectura = 5

                        desc = Desc_Lectura.objects.filter(resultado_lectura=resultado_lectura).values('orden_trabajo')

                        qs = qs.filter(numero_orden__in=desc)

        # _odt = PuntoSuministro.objects.select_related('punto_suministro__aparato').filter(calle = sSearch)
        # _odt = PuntoDeSuministro.objects.filter(qs.punto_suministro)
        # print(_odt)
        return qs

###### ------------------------- ADMIN USER  ------------------------- ######

@login_required(login_url=settings.LOGIN_PAGE)
def change_password(request):
    context = RequestContext(request)
    if request.method == 'POST':

        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():

            writeAudit('Cambio de password', 'grabacion ok', request.user, '')
            form.save()
            update_session_auth_hash(request, form.user)  # Important!

            messages.success(request, 'Contraseña actualizada correctamente!')

            return redirect(settings.LOGIN_PAGE)

        else:
            update_session_auth_hash(request, form.user)

    else:

        form = PasswordChangeForm(user=request.user)

    context['form'] = form
    return render(request, 'account/change_password.html', context.flatten())


@login_required(login_url=settings.LOGIN_PAGE)
def about(request):
    context_dict = {'version': settings.APP_VERSION}
    return render(request, 'account/about.html', context_dict)

###### ------------------------- ADMIN TERMINALES  ------------------------- ######
@login_required(login_url=settings.LOGIN_PAGE)
def atp_main(request):
    # log.debug("Hey there it works!!")
    # ("entro adm terminales")

    # log.info("Hey there it works!!")
    # log.warn("Hey there it works!!")
    # log.error("Hey there it works!!")
    try:
        context = RequestContext(request)
        context['terminales'] = TerminalPortatil.objects.all()
        context['form'] = tpForm()
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)
    return render_to_response('data_admin/tp/_terminales.html', context)


@login_required(login_url=settings.LOGIN_PAGE)
def atp_edit1(request):
    context = RequestContext(request)
    try:
        # print('entro atp_edit1')
        id = request.POST['id']
        # print(id)
        terminal = TerminalPortatil.objects.get(numero_serie=id)
        form = tpForm(request.POST or None, instance=terminal)
        if form.is_valid():
            # prefijo = form.cleaned_data['prefijo']

            form.save()
            writeAudit("gestion terminales", "edicion", request.user, form.cleaned_data)

            context['terminales'] = TerminalPortatil.objects.all()
            context['form'] = form
            # return HttpResponse("getPage('{% url 'qorder:atp_main' %}')")
            return render_to_response('data_admin/tp/_terminales.html', context)
        else:
            variable = json.loads(form.errors.as_json())
            # print(variable)
            for v in variable:
                mensaje = variable[v]
            # print(mensaje)
            for p in mensaje:
                print(p)
            variable1 = str(p['message'])
            mensaje = str(variable1)
            return HttpResponse(mensaje, status=300)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)
    context['terminal'] = terminal
    context['form'] = form
    return render_to_response('data_admin/tp/_tp_edit.html', context)


@login_required(login_url=settings.LOGIN_PAGE)
def atp_edit(request):
    context = RequestContext(request)
    try:
        # print("ENTRO ATP_EDIT")
        id = request.POST['id']
        # print(id)
        terminal = TerminalPortatil.objects.get(numero_serie=id)
        # print('antes isInactivable')
        tecnico = Tecnico.objects.filter(terminal_portatil=terminal.numero_serie)
        # print(tecnico)
        if len(tecnico) > 0:
            # print('isInactivable')
            Initial_data = []
            Initial_data.append({'oficina': request.user.get_my_oficinas()})
            context['terminal'] = terminal
            form = tpFormInactivable(instance=terminal)
        else:
            # print('not isInactivable')
            Initial_data = []
            Initial_data.append({'oficina': request.user.get_my_oficinas()})

            context['terminal'] = terminal
            form = tpForm(instance=terminal)
            form.fields["oficina"].queryset = request.user.get_my_oficinas()

        context['form'] = form
        return render_to_response('data_admin/tp/_tp_edit.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def tp_cflags(request):
    context = RequestContext(request)
    try:
        # print('Entro tp_cflags')
        id = request.POST['id']
        # print(id)
        name = request.POST['name']
        # print(name)
        action = request.POST['action']
        # print(action)

        tp = TerminalPortatil.objects.get(numero_serie=id)

        if action == '0':
            tp.enable('0')
            writeAudit("gestion terminales", "edicion", request.user, '{} disable'.format(tp))
            return JsonResponse({"accion": action})
        elif action == '1':
            tp.enable('1')
            writeAudit("gestion terminales", "edicion", request.user, '{} enable'.format(tp))
            return JsonResponse({"accion": action})
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)
    return HttpResponse(status=200)


###### ------------------------- ADMIN TECNICOS  ------------------------- ######
@login_required(login_url=settings.LOGIN_PAGE)
def tecnicos_main(request):
    try:
        context = RequestContext(request)
        context['tecnicos'] = []
        form = tecnicoForm(edit=True)
        context['form'] = form

    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)

    return render_to_response('data_admin/tecnicos/_tecnicos.html', context)


@login_required(login_url=settings.LOGIN_PAGE)
def tecnico_new(request):
    try:
        context = RequestContext(request)
        # print("ENTRO TECNICO_NEW")
        id_centro = request.POST['id_oficina']
        # print(id_centro)
        if id_centro:
            centro = WorkUnit.objects.get(pk=id_centro)
        form = tecnicoForm(initial={'activo': 1}, edit=True)
        form.fields["terminal_portatil"].queryset = TerminalPortatil.objects.filter(tecnico=None,
                                                                                    oficina=centro,
                                                                                    estado=1)
        context['form'] = form
        return render_to_response('data_admin/tecnicos/_tech_edit.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def tecnico_edit(request):
    try:
        context = RequestContext(request)
        # print("ENTRO TECNICO_EDIT")
        id_centro = request.POST['id_oficina']
        # print(id_centro)
        if id_centro:
            centro = WorkUnit.objects.get(pk=id_centro)

        id = request.POST['id']
        # print(id)
        tecnico = Tecnico.objects.get(codigo=id)
        context['tecnico'] = tecnico

        if tecnico.terminal_portatil != None:
            # print('{} {} '.format(tecnico.terminal_portatil.estado_asignada,tecnico.terminal_portatil.estado_asignada))
            if tecnico.terminal_portatil.estado_asignada == 1 or tecnico.terminal_portatil.estado_cargada == 1:
                # print('Esta asignada')
                form = tecnicoForm(instance=tecnico,
                                   initial={'TerminalPortatil': tecnico.terminal_portatil.numero_serie}, edit=False)

            else:
                form = tecnicoForm(instance=tecnico, initial={'TerminalPortatil': tecnico.terminal_portatil}, edit=True)
                form.fields["terminal_portatil"].queryset = TerminalPortatil.objects.filter(
                    Q(tecnico=None) | Q(tecnico=tecnico),
                    oficina=centro,
                    estado=1)
        else:
            form = tecnicoForm(instance=tecnico, initial={'TerminalPortatil': tecnico.terminal_portatil}, edit=True)
            form.fields["terminal_portatil"].queryset = TerminalPortatil.objects.filter(
                Q(tecnico=None) | Q(tecnico=tecnico),
                oficina=centro,
                estado=1)
        context['form'] = form

        return render_to_response('data_admin/tecnicos/_tech_edit.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@csrf_exempt
def gt_tabla(request):
    try:
        context = RequestContext(request)
        id_centro = request.POST['id_oficina']
        # print(id_centro)
        if id_centro:
            centro = WorkUnit.objects.get(pk=id_centro)
            # print(centro)
            tecnicos_oficina = OficinaXTecnico.objects.filter(oficina=id_centro, fecha_baja=None)
            tecs = []
            for item in tecnicos_oficina:
                tecs.append(item.tecnico.codigo)
            # print(tecs)
            tecnicos = Tecnico.objects.filter(codigo__in=tecs)
            # print(len(tecnicos))
            context['tecnicos'] = tecnicos
            # print(tecnicos)
            context['terminales_disponibles'] = TerminalPortatil.objects.filter(tecnico=None,
                                                                                oficina=centro,
                                                                                estado=1)
            # print( context['terminales_disponibles'])
            form = tecnicoForm(request.POST, edit=True)
            # form = tecnicoForm()
            form.fields["terminal_portatil"].queryset = context['terminales_disponibles']

            context['form'] = form
        return render_to_response('data_admin/tecnicos/_table_techs.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def tecnico_save(request):
    context = RequestContext(request)

    try:
        # print("ENTRO TECNICO_SAVE")
        id = request.POST['id']
        oficina = request.POST['id_oficinah']
        if id:
            tecnico = Tecnico.objects.get(codigo=id)
            if tecnico.terminal_portatil != None:
                if tecnico.terminal_portatil.estado_asignada == 1 or tecnico.terminal_portatil.estado_cargada == 1:
                    form = tecnicoForm(request.POST, instance=tecnico, edit=False)
                else:
                    form = tecnicoForm(request.POST, instance=tecnico, edit=True)
            else:
                form = tecnicoForm(request.POST, instance=tecnico, edit=True)
            if form.is_valid():
                tecnico = Tecnico.objects.get(codigo=id)
                # print(tecnico)
                var1 = tecnico.flag_reset_password
                var2 = tecnico.flag_descarga_total
                var3 = tecnico.flag_descarga_parcial
                var4 = tecnico.flag_liberar_datos
                # print(var1)
                # print(var2)
                # print(var3)
                # print(var4)
                form.save()
                tecnico = Tecnico.objects.get(codigo=id)
                tecnico.flag_reset_password = var1
                tecnico.flag_descarga_total = var2
                tecnico.flag_descarga_parcial = var3
                tecnico.flag_liberar_datos = var4
                tecnico.save()

                writeAudit("gestion tecnicos", "edicion", request.user, form.cleaned_data)
                # grabar la relacion con oficina si cambió

                context['id_oficina'] = oficina

                tecnicos_oficina = OficinaXTecnico.objects.filter(oficina=oficina, fecha_baja=None)
                # print(tecnicos_oficina)
                tecs = []
                for item in tecnicos_oficina:
                    tecs.append(item.tecnico.codigo)
                # print(tecs)
                tecnicos = Tecnico.objects.filter(codigo__in=tecs)

                context['tecnicos'] = tecnicos

                context['terminales_disponibles'] = TerminalPortatil.objects.filter(tecnico=None,
                                                                                    oficina=oficina,
                                                                                    estado=1)
                context['form'] = form
                # return HttpResponse("getPage('{% url 'qorder:atp_main' %}')")
                return render_to_response('data_admin/tecnicos/_table_techs.html', context)
            # print('Form no valido')
            # print(form.errors.as_json())
        else:

            form = tecnicoForm(request.POST, edit=True)

            if form.is_valid():
                # print("form is valid 1")
                # print(form.cleaned_data)
                new_tecnico = form.save()

                writeAudit("gestion tecnico", "nuevo", request.user, form.cleaned_data)

                centro = WorkUnit.objects.get(pk=oficina)
                # print(centro)
                # print(new_tecnico.codigo)
                tecnico = Tecnico.objects.get(codigo=new_tecnico.codigo)
                # print(tecnico)

                tecnico.flag_reset_password = 1
                tecnico.flag_descarga_total = 0
                tecnico.flag_descarga_parcial = 0
                tecnico.flag_liberar_datos = 0
                tecnico.save()

                oftec = OficinaXTecnico.objects.create(tecnico=tecnico,
                                                       oficina=centro,
                                                       fecha_asignacion=date.today(),
                                                       fecha_baja=None)

                oftec.save()
                writeAudit("gestion tecnico", "nuevo", request.user,
                           'Se agregó el técnico {} a la oficina:{}'.format(tecnico, oficina))

                tecnicos_oficina = OficinaXTecnico.objects.filter(oficina=oficina, fecha_baja=None)
                # print(tecnicos_oficina)
                tecs = []
                for item in tecnicos_oficina:
                    tecs.append(item.tecnico.codigo)
                # print(tecs)
                tecnicos = Tecnico.objects.filter(codigo__in=tecs)

                context['tecnicos'] = tecnicos
                context['form'] = form

                return render_to_response('data_admin/tecnicos/_table_techs.html', context)
            else:
                # print(form.errors.as_json())
                if "obligatorio" in form.errors.as_json():
                    return HttpResponse(status=300)
                else:
                    return HttpResponse(status=302)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)

    form.fields["terminal_portatil"].queryset = TerminalPortatil.objects.filter(tecnico=None,
                                                                                oficina=oficina,
                                                                                estado=1)

    context['tecnico'] = tecnico
    context['form'] = form
    return render_to_response('data_admin/tp/_tp_edit.html', context)


def tecnico_cflag(request):
    context = RequestContext(request)
    try:

        id = request.POST['id']
        # print(id)
        name = request.POST['name']
        # print(name)
        action = request.POST['action']
        # print(action)

        tecnico = Tecnico.objects.get(codigo=id)
        # print('tecnico {}'.format(tecnico))

        if action == '0' or action == '1':

            tecnico.resetpassword(action)
            return JsonResponse({"accion": str(action)})
        elif action == '2':
            tecnico.descarga('0')
            writeAudit("gestion tecnico", "descarga", request.user, 'Se cancelo la descarga al tecnico {}'.format(id))
            return JsonResponse({"accion": action})
        elif action == '3':
            
            rutas = Ruta.objects.filter(tecnico=tecnico, estado__in=[3])
            
            rutas.update(tecnico=None, estado=33, fecha_hora_asignacion=None, usuario_asignacion=None,
                        flag_asignacion_guardada='0')
            
            ordenes = OrdenDeTrabajo.objects.filter(tecnico=tecnico, estado__in=[3])
            
            ordenes.update(tecnico=None, estado=33, fecha_hora_asignacion=None, usuario_asignacion=None,
                        flag_asignacion_guardada='0')
            
            tecnico.liberar('1')
            tecnico.descarga('1')
            writeAudit("gestion tecnico", "descarga", request.user, 'Se solicitó descarga al tecnico {}'.format(id))
            return JsonResponse({"accion": action})
        elif action == '4':
            # tecnico.liberar('0')
            return JsonResponse({"accion": action})
            # print('llega ')
        elif action == '5':
            tecnico.liberar('1')
            writeAudit("gestion tecnico", "liberar", request.user, 'Se solicitó liberar al tecnico {}'.format(id))
            rutas = Ruta.objects.filter(tecnico=tecnico, estado=7)
            rutas.update(tecnico=None,
                         estado=33,
                         fecha_hora_asignacion=None,
                         usuario_asignacion=None,
                         flag_asignacion_guardada='0')
            ordenes = OrdenDeTrabajo.objects.filter(tecnico=tecnico, estado=7)
            ordenes.update(tecnico=None,
                           estado=33,
                           fecha_hora_asignacion=None,
                           usuario_asignacion=None,
                           flag_asignacion_guardada='0')

            tt = TerminalPortatil.objects.filter(pk=tecnico.terminal_portatil)
            tt.update(estado_cargada='0',
                      cantidad_cargada=0)
            return JsonResponse({"accion": action})
        elif action == '6':
            # print(tecnico.terminal_portatil)
            if tecnico.terminal_portatil == None:
                tecnico.enable('0')
                return JsonResponse({"accion": action})
            else:
                return HttpResponse(status=300)
        elif action == '7':
            tecnico.enable('1')
            return JsonResponse({"accion": action})
    except Exception as e:
        # print ("Error {}".format(e))
        return HttpResponse(status=500)
    return HttpResponse(status=200)
    # context['terminales'] = TerminalPortatil.objects.all()
    # return render_to_response('data_admin/tp/_terminales.html', context)


###### ------------------------- ADMIN ANOMALIAS  ------------------------- ######
@login_required(login_url=settings.LOGIN_PAGE)
def anomalias_main(request):
    try:
        context = RequestContext(request)
        anomalias = Anomalia.objects.all()
        # print("ENTRO ANOMALIAS")
        # print(anomalias)
        context['anomalias'] = anomalias
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)

    return render_to_response('data_admin/anomalias/_anomalias.html', context)


@login_required(login_url=settings.LOGIN_PAGE)
def anomalias_edit(request):
    try:
        context = RequestContext(request)
        # print("ENTRO ANOMALIA_EDIT")
        id = request.POST['id']
        anomalia = Anomalia.objects.get(id_anomalia=id)
        context['anomalia'] = anomalia
        form = anomaliaForm(instance=anomalia)
        context['form'] = form
        return render_to_response('data_admin/anomalias/_anomalias_edit.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def anomalias_new(request):
    try:
        context = RequestContext(request)
        # print("ENTRO ANOMALIA_NEW")

        form = anomaliaForm(initial={'activo': 1})
        context['form'] = form
        return render_to_response('data_admin/anomalias/_anomalias_edit.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def anomalias_obs(request):
    try:
        context = RequestContext(request)
        id = request.POST['id']
        anomalia = Anomalia.objects.get(id_anomalia=id)
        context['anomalia'] = anomalia

        observaciones = ObservacionXAnomalia.objects.filter(anomalia=anomalia)

        vobs = []
        for obs in observaciones:
            vobs.append(obs.codigo.codigo)

        context['observaciones'] = Codigo.objects.filter(codigo__in=vobs)

        codigos = Codigo.objects.filter(prefijo='OB').exclude(codigo__in=vobs)
        context['codigos'] = codigos

        return render_to_response('data_admin/anomalias/_anomalias_obs.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


def agregarobservaciones(request):
    return HttpResponse(status=500)


@csrf_exempt
def anomalias_tabla(request):
    try:
        context = RequestContext(request)

        anomalias = Anomalia.objects.all()
        context['anomalias'] = anomalias

        return render_to_response('data_admin/anomalias/_table_anomalias.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


def anomalias_save(request):
    context = RequestContext(request)

    try:
        # print("ENTRO ANOMALIA_SAVE")
        id = request.POST['id_anomalia']
        accion = request.POST['accion']
        # print("Id "+id)

        if accion == 'edit':
            anomalia = Anomalia.objects.get(id_anomalia=id)

            form = anomaliaForm(request.POST, instance=anomalia)

            if form.is_valid():
                form.save()
                writeAudit("gestion anomalias", "edicion", request.user, form.cleaned_data)
                # grabar la relacion con oficina si cambió

                anomalias = Anomalia.objects.all()

                context['anomalias'] = anomalias

                context['form'] = form
                # return HttpResponse("getPage('{% url 'qorder:atp_main' %}')")
                return render_to_response('data_admin/anomalias/_anomalias.html', context)

            # print(form.errors.as_json())
        elif accion == 'observaciones':
            anomalia = Anomalia.objects.get(id_anomalia=id)
            codigos = request.POST['codigos']
            observaciones = ObservacionXAnomalia.objects.filter(anomalia=anomalia)
            observaciones.delete();
            writeAudit("gestion terminales", "edicion", request.user,
                       'Se borró las anomalías {} desde observaciones por anomalias'.format(observaciones))

            if len(codigos) > 0:
                cod = codigos.split(",")
                writeAudit("gestion terminales", "edicion", request.user,
                           'Se agregaron las observaciones {} a la anomalia {}'.format(cod, anomalia))
                for value in cod:
                    codigo = Codigo.objects.get(codigo=value)
                    obs = ObservacionXAnomalia()
                    obs.anomalia = anomalia
                    obs.codigo = codigo
                    obs.save()

            return HttpResponse(status=200)

        else:

            form = anomaliaForm(request.POST)

            if form.is_valid():
                new_anomalia = form.save()
                writeAudit("gestion anomalias", "nuevo", request.user, form.cleaned_data)

                context['anomalias'] = Anomalia.objects.all()
                context['form'] = form
                # return HttpResponse("getPage('{% url 'qorder:atp_main' %}')")

                return render_to_response('data_admin/anomalias/_anomalias.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)

    context['anomalias'] = anomalias
    context['form'] = form
    return render_to_response('data_admin/anomalias/_anomalias_edit.html', context)


def anomalias_cflags(request):
    context = RequestContext(request)
    try:

        # print(request.user)
        id = request.POST['id']
        # print(id)
        name = request.POST['name']
        # print(name)
        action = request.POST['action']
        # print(action)

        anomalia = Anomalia.objects.get(id_anomalia=id)
        if name == 'enable':
            writeAudit("gestion anomalias", "edicion", request.user, 'habilitar anomalía {}'.format(anomalia))
            anomalia.enable(action)
            return JsonResponse({"activo": str(anomalia.activo)})
        else:
            writeAudit("gestion anomalias", "edicion", request.user, 'deshabilitar anomalía {}'.format(anomalia))
            anomalia.disable(action)
            return JsonResponse({"activo": str(anomalia.activo)})

    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)
    return HttpResponse(status=300)


###### ------------------------- ADMIN CODIGOS  ------------------------- ######
@login_required(login_url=settings.LOGIN_PAGE)
def codigos_main(request):
    try:
        context = RequestContext(request)
        codigos = []
        prefijos = Prefijo.objects.all()
        # print(prefijos)
        # print("ENTRO codigos")
        context['codigos'] = codigos
        context['prefijos'] = prefijos
        context['prefijo'] = 'TR'
        form = codigoForm()
        context['form'] = form

    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)

    return render_to_response('data_admin/codigos/_codigos.html', context)


@login_required(login_url=settings.LOGIN_PAGE)
def codigos_edit(request):
    try:
        context = RequestContext(request)
        # print("ENTRO codigos_EDIT")
        id = request.POST['id']
        # print(id)
        codigo = Codigo.objects.get(codigo=id)
        context['codigo'] = codigo
        # print('codigo{}'.format(codigo))
        form = codigoForm(instance=codigo)
        context['form'] = form
        return render_to_response('data_admin/codigos/_codigos_edit.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def codigos_new(request):
    try:
        context = RequestContext(request)
        # print("ENTRO codigo_NEW")
        id_prefijo = request.POST['id_prefijo']
        # print(id_prefijo)
        prefijo = Prefijo.objects.get(prefijo=id_prefijo)

        form = codigoForm(initial={'prefijo': prefijo, 'activo': 1})
        form.prefijo = prefijo
        context['form'] = form
        return render_to_response('data_admin/codigos/_codigos_edit.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@csrf_exempt
def codigos_tabla(request):
    try:
        context = RequestContext(request)
        id = request.POST['id_prefijo']
        # print(id)
        if id == '':
            codigos = Codigo.objects.filter(prefijo='')
        else:
            prefijo = Prefijo.objects.get(prefijo=id)
            codigos = Codigo.objects.filter(prefijo=prefijo)
            context['codigos'] = codigos

        return render_to_response('data_admin/codigos/_table_codigos.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


def codigos_save(request):
    context = RequestContext(request)

    try:
        # print("ENTRO codigo_SAVE")
        id = request.POST['id_codigo']

        accion = request.POST['accion']
        # print("Id "+id)
        # print("Accion "+accion)
        if accion == 'edit':
            codigo = Codigo.objects.get(codigo=id)

            form = codigoForm(request.POST, instance=codigo)

            if form.is_valid():
                prefijo = form.cleaned_data['prefijo']
                form.save()
                writeAudit("gestion códigos", "edicion", request.user, form.cleaned_data)
                prefijos = Prefijo.objects.all()
                codigos = Codigo.objects.filter(prefijo=prefijo)
                context['codigos'] = codigos
                context['prefijos'] = prefijos
                context['prefijo'] = prefijo.prefijo
                context['form'] = form
                return render_to_response('data_admin/codigos/_codigos.html', context)
            else:
                # print(form.errors.as_json())
                context['form'] = form
                return HttpResponse(form.errors.as_json(), status=301)

        else:

            form = codigoForm(request.POST)

            if form.is_valid():
                prefijo = form.cleaned_data['prefijo']
                new_codigo = form.save()
                writeAudit("gestion códigos", "nuevo", request.user, form.cleaned_data)
                prefijos = Prefijo.objects.all()
                codigos = Codigo.objects.filter(prefijo=prefijo)
                context['codigos'] = codigos
                context['prefijos'] = prefijos
                context['prefijo'] = prefijo.prefijo
                context['form'] = form
                # return HttpResponse("getPage('{% url 'qorder:atp_main' %}')")

                return render_to_response('data_admin/codigos/_codigos.html', context, status=200)
            else:
                # print(form.errors.as_json())
                context['form'] = form
                return HttpResponse(status=300)

    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)

    context['codigos'] = codigos
    context['form'] = form
    return render_to_response('data_admin/codigos/_codigos_edit.html', context)


def codigos_cflags(request):
    context = RequestContext(request)
    try:
        context['form'] = codigoForm()
        # print(request.user)
        id = request.POST['id']
        # print(id)
        name = request.POST['name']
        # print(name)
        action = request.POST['action']
        # print(action)

        codigo = Codigo.objects.get(codigo=id)
        if name == 'enable':
            codigo.enable(action)
            return JsonResponse({"activo": str(codigo.activo)})

    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)
    return HttpResponse(status=300)


###### ------------------------- ADMIN ENCUESTAS  ------------------------- ######
@login_required(login_url=settings.LOGIN_PAGE)
def encuestas_main(request):
    try:
        context = RequestContext(request)
        encuestas = Encuesta.objects.all()
        # print("ENTRO encuestas")
        context['encuestas'] = encuestas
        form = encuestaForm()
        context['form'] = form

    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)

    return render_to_response('data_admin/encuestas/_encuestas.html', context)


@login_required(login_url=settings.LOGIN_PAGE)
def encuestas_edit(request):
    try:
        context = RequestContext(request)
        # print("ENTRO encuestas_EDIT")
        id = request.POST['id']
        encuesta = Encuesta.objects.get(id=id)
        context['encuesta'] = encuesta
        form = encuestaForm(instance=encuesta)
        context['form'] = form
        return render_to_response('data_admin/encuestas/_encuestas_edit.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def encuestas_new(request):
    try:
        context = RequestContext(request)
        # print("ENTRO encuesta_NEW")
        form = encuestaForm(initial={'activo': 1})
        context['form'] = form
        return render_to_response('data_admin/encuestas/_encuestas_edit.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@csrf_exempt
def encuesta_detail(request):
    try:
        # print('ENTRO detalle encuesta')
        context = RequestContext(request)
        id = request.POST['id_encuesta']
        encuesta = Encuesta.objects.get(id=id)
        detalleencuesta = EncuestaDetalle.objects.filter(encuesta=encuesta).order_by('orden')
        # print(detalleencuesta)
        context['detalleencuesta'] = detalleencuesta

        return render_to_response('data_admin/encuestas/_table_detalle.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def pregunta_new(request):
    try:
        context = RequestContext(request)
        # print("ENTRO pregunta_NEW")
        id = request.POST['id_encuesta']
        encuesta = Encuesta.objects.get(id=id)
        preguntas = EncuestaDetalle.objects.filter(encuesta=encuesta)
        orden = len(preguntas) + 1
        form = preguntaForm(initial={'encuesta': encuesta, 'orden': orden})
        # print(encuesta)
        context['form'] = form

        return render_to_response('data_admin/encuestas/_pregunta_edit.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def pregunta_edit(request):
    try:
        context = RequestContext(request)
        # print("ENTRO pregunta_EDIT")
        id = request.POST['id']
        pregunta = EncuestaDetalle.objects.get(id=id)
        context['pregunta'] = pregunta
        form = preguntaForm(instance=pregunta)
        context['form'] = form
        return render_to_response('data_admin/encuestas/_pregunta_edit.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


def pregunta_orden(request):
    context = RequestContext(request)
    try:
        # print("ENTRO pregunta_orden")
        id = request.POST['id_encuesta']
        ordenes = json.loads(request.POST['diff'])

        encuesta = Encuesta.objects.get(id=id)

        for orden in ordenes:
            # print(orden)
            o = EncuestaDetalle.objects.get(id=orden['id'])
            # print(o.orden)
            o.orden = orden['newData']
            o.save()
            # print(o.orden)

        detalles = EncuestaDetalle.objects.filter(encuesta=encuesta)
        for d in detalles:
            print('{} {}'.format(d.id, d.orden))

        return HttpResponse(status=200)


    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


def pregunta_save(request):
    context = RequestContext(request)
    try:
        # print("ENTRO codigo_SAVE")
        id = request.POST['id_pregunta']
        accion = request.POST['accion']
        if accion == 'edit':
            pregunta = EncuestaDetalle.objects.get(id=id)

            form = preguntaForm(request.POST, instance=pregunta)

            if form.is_valid():
                form.save()
                writeAudit("preguntas encuestas", "edicion", request.user, form.cleaned_data)
                encuesta = form.cleaned_data['encuesta']
                preguntas = EncuestaDetalle.objects.filter(encuesta=encuesta)
                context['preguntas'] = preguntas
                context['form'] = form
                return render_to_response('data_admin/encuestas/_table_detalle.html', context)
            # print('Form no valido')
            # print(form.errors.as_json())
        else:
            form = preguntaForm(request.POST)
            if form.is_valid():
                # print("form is valid")
                encuesta = form.cleaned_data['encuesta']
                form.save()
                writeAudit("preguntas encuestas", "nueva", request.user, form.cleaned_data)
                preguntas = EncuestaDetalle.objects.filter(encuesta=encuesta)
                context['preguntas'] = preguntas
                context['form'] = form
                return render_to_response('data_admin/encuestas/_table_detalle.html', context)
            else:
                # print(form.errors.as_json())
                context['form'] = form
                return HttpResponse(status=300)

    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)

    context['encuestas'] = encuestas
    context['form'] = form
    return render_to_response('data_admin/encuestas/_encuestas_edit.html', context)


def encuestas_save(request):
    context = RequestContext(request)

    try:
        # print("ENTRO codigo_SAVE")
        id = request.POST['id_encuesta']

        accion = request.POST['accion']
        # print("Id "+id)
        # print("Accion "+accion)
        if accion == 'edit':
            encuesta = Encuesta.objects.get(id=id)

            form = encuestaForm(request.POST, instance=encuesta)

            if form.is_valid():
                form.save()
                writeAudit("gestion encuesta", "edicion", request.user, form.cleaned_data)
                encuestas = Encuesta.objects.all()
                context['encuestas'] = encuestas
                context['form'] = form
                return render_to_response('data_admin/encuestas/_encuestas.html', context)
            # print('Form no valido')
            # print(form.errors.as_json())
        else:

            form = encuestaForm(request.POST)
            # print("evaluate if form is valid")

            if form.is_valid():
                # print("form is valid")

                new_codigo = form.save()
                writeAudit("gestion encuesta", "nueva", request.user, form.cleaned_data)
                encuestas = Encuesta.objects.all()
                context['encuestas'] = encuestas
                context['form'] = form
                # return HttpResponse("getPage('{% url 'qorder:atp_main' %}')")

                return render_to_response('data_admin/encuestas/_encuestas.html', context)
            else:
                # print(form.errors.as_json())
                context['form'] = form
                return HttpResponse(status=300)

    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)

    context['encuestas'] = encuestas
    context['form'] = form
    return render_to_response('data_admin/encuestas/_encuestas_edit.html', context)


def encuestas_cflags(request):
    context = RequestContext(request)
    try:
        context['form'] = encuestaForm()
        # print(request.user)
        id = request.POST['id']
        # print(id)
        name = request.POST['name']
        # print(name)
        action = request.POST['action']
        # print(action)

        encuesta = Encuesta.objects.get(id=id)
        if name == 'enable':
            encuesta.enable(action)
            if action == '1':
                writeAudit("gestion encuesta", "edicion", request.user, "Habilitar encuesta {}".format(encuesta))
            else:
                writeAudit("gestion encuesta", "edicion", request.user, "Deshabilitar encuesta {}".format(encuesta))

            return JsonResponse({"activo": str(encuesta.activo)})

    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)
    return HttpResponse(status=300)


###### ------------------------- ADMIN PROBLEMAS  ------------------------- ######
@login_required(login_url=settings.LOGIN_PAGE)
def problemas_main(request):
    try:
        context = RequestContext(request)
        problemas = Problema.objects.all()
        # print("ENTRO problemas")
        # print(problemas)
        context['problemas'] = problemas
        form = problemaForm()
        context['form'] = form

    except Exception as e:
        # print ("Error {}".format(e))
        return HttpResponse(status=500)

    return render_to_response('data_admin/problemas/_problemas.html', context)


@login_required(login_url=settings.LOGIN_PAGE)
def problemas_edit(request):
    try:
        context = RequestContext(request)
        # print("ENTRO problema_EDIT")
        id = request.POST['id']
        problema = Problema.objects.get(id_problema=id)
        context['problema'] = problema
        form = problemaForm(instance=problema)
        context['form'] = form
        return render_to_response('data_admin/problemas/_problemas_edit.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def problemas_new(request):
    try:
        context = RequestContext(request)
        # print("ENTRO problema_NEW")
        form = problemaForm()
        context['form'] = form
        return render_to_response('data_admin/problemas/_problemas_edit.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@csrf_exempt
def problemas_tabla(request):
    try:
        context = RequestContext(request)

        problemas = Problema.objects.all()
        context['problemas'] = problemas

        return render_to_response('data_admin/problemas/_table_problemas.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


def problemas_save(request):
    context = RequestContext(request)

    try:
        # print("ENTRO problema_SAVE")
        id = request.POST['id_problema']
        accion = request.POST['accion']
        # print("Id "+id)

        if accion == 'edit':
            problema = Problema.objects.get(id_problema=id)

            form = problemaForm(request.POST, instance=problema)

            if form.is_valid():
                form.save()
                # grabar la relacion con oficina si cambió

                problemas = Problema.objects.all()

                context['problemas'] = problemas

                context['form'] = form
                # return HttpResponse("getPage('{% url 'qorder:atp_main' %}')")
                return render_to_response('data_admin/problemas/_problemas.html', context)
            # print('Form no valido')
            # print(form.errors.as_json())
        else:

            form = problemaForm(request.POST)

            if form.is_valid():
                # print("form is valid")
                new_problema = form.save()

                context['problemas'] = Problema.objects.all()
                context['form'] = form
                # return HttpResponse("getPage('{% url 'qorder:atp_main' %}')")

                return render_to_response('data_admin/problemas/_problemas.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)

    context['problemas'] = problemas
    context['form'] = form
    return render_to_response('data_admin/problemas/_problemas_edit.html', context)


def problemas_cflags(request):
    context = RequestContext(request)
    try:
        context['form'] = problemaForm()
        # print(request.user)
        id = request.POST['id']
        # print(id)
        name = request.POST['name']
        # print(name)
        action = request.POST['action']
        # print(action)

        problema = Problema.objects.get(id_problema=id)
        if name == 'enable':
            problema.enable(action)
            return JsonResponse({"activo": str(problema.activo)})

    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)
    return HttpResponse(status=300)


###### ------------------------- ADMIN TIPO ORDENES  ------------------------- ######
@login_required(login_url=settings.LOGIN_PAGE)
def tiposordenes_main(request):
    try:
        context = RequestContext(request)
        context['tipos_ordenes'] = TipoOrden.objects.all()
        # print(context['tipos_ordenes'])
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)
    return render_to_response('data_admin/tipo_orden/_tipos_orden.html', context)


@csrf_exempt
def tiposordenes_tabla(request):
    try:
        context = RequestContext(request)

        tipos_ordenes = TipoOrden.objects.all()
        context['tipos_ordenes'] = tipos_ordenes

        return render_to_response('data_admin/tipo_orden/_table_tipos_ordenes.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@csrf_exempt
def tiposordenes_propiedades(request):
    try:
        context = RequestContext(request)
        # print("PROPIEDADES")
        tipo_orden = TipoOrden.objects.get(tipo_orden=request.POST['tipo_orden'])
        anomalias = Anomalia.objects.filter(activo=1)

        lista_resultado = []
        for anomalia in anomalias:
            anomaliasxtipoorden = AnomaliaXTipo.objects.filter(tipo_orden=tipo_orden, anomalia=anomalia)
            # print(anomaliasxtipoorden)
            if anomaliasxtipoorden:

                dados_lancamento = {
                    'id_anomalia': anomalia.id_anomalia,
                    'descripcion': anomalia.descripcion,
                    'foto_obligatoria': anomaliasxtipoorden[0].foto_obligatoria,
                    'observacion_obligatoria': anomaliasxtipoorden[0].observacion_obligatoria,
                    'observacion_tabulada': anomaliasxtipoorden[0].observacion_tabulada,
                    'datos_medidor': anomaliasxtipoorden[0].datos_medidor,
                    'activo': anomaliasxtipoorden[0].activo
                }
            else:
                dados_lancamento = {
                    'id_anomalia': anomalia.id_anomalia,
                    'descripcion': anomalia.descripcion,
                    'foto_obligatoria': None,
                    'observacion_obligatoria': None,
                    'observacion_tabulada': None,
                    'datos_medidor': None,
                    'activo': 0
                }

            lista_resultado.append(dados_lancamento)
        context['anomalias'] = lista_resultado
        context['tipo_orden'] = tipo_orden
        return render_to_response('data_admin/tipo_orden/_propiedades.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


def tiposordenes_anomaliaxtipo_save(request):
    try:
        context = RequestContext(request)
        if request.method == 'POST':
            id_to = request.POST['id_tipo_orden']
            id_anomalias = eval(request.POST['id_anomalias'])
            picture = request.POST['picture']
            observaciones = request.POST['observaciones']
            observacionestabuladas = request.POST['observacionestabuladas']
            counter_data = request.POST['counter_data']
            if 'true' in picture:
                picture = '1'
            else:
                picture = '0'
            if 'true' in observaciones:
                observaciones = '1'
            else:
                observaciones = '0'
            if 'true' in observacionestabuladas:
                observacionestabuladas = '1'
            else:
                observacionestabuladas = '0'
            if 'true' in counter_data:
                counter_data = '1'
            else:
                counter_data = '0'
            tipo_orden = TipoOrden.objects.get(tipo_orden=id_to)
            cto = AnomaliaXTipo.objects.filter(tipo_orden=tipo_orden, anomalia__in=id_anomalias)

            # cto = QwConfigTiposOrdenes.objects.filter(id_dato_config__in=id_anomalias,
            #                                          id_tipo_orden=id_to,
            #                                          id_config=ANOMALIA)

            a = cto.delete()
            writeAudit("anomalías por tipo ordenes", "edicion", request.user,
                       "Borrar anomalías tipo de orden {}".format(tipo_orden))

            cp = []
            for pid in id_anomalias:
                anomalia = Anomalia.objects.get(id_anomalia=pid)
                cp.append(AnomaliaXTipo(tipo_orden=tipo_orden,
                                        anomalia=anomalia,
                                        foto_obligatoria=picture,
                                        observacion_obligatoria=observaciones,
                                        observacion_tabulada=observacionestabuladas,
                                        datos_medidor=counter_data,
                                        activo=1))

            AnomaliaXTipo.objects.bulk_create(cp)

            writeAudit("anomalías tipo ordenes", "edicion", request.user,
                       "Se adicionaron {} anomalías al tipo de orden {}".format(len(cp), tipo_orden))

            # return HttpResponse('Se configuraron {} anomalias'.format(len(id_anomalias)),status=200)
            anomalias = Anomalia.objects.filter(activo=1)

            lista_resultado = []
            for anomalia in anomalias:
                anomaliasxtipoorden = AnomaliaXTipo.objects.filter(tipo_orden=tipo_orden, anomalia=anomalia)

                if anomaliasxtipoorden:

                    dados_lancamento = {
                        'id_anomalia': anomalia.id_anomalia,
                        'descripcion': anomalia.descripcion,
                        'foto_obligatoria': anomaliasxtipoorden[0].foto_obligatoria,
                        'observacion_obligatoria': anomaliasxtipoorden[0].observacion_obligatoria,
                        'observacion_tabulada': anomaliasxtipoorden[0].observacion_tabulada,
                        'datos_medidor': anomaliasxtipoorden[0].datos_medidor,
                        'activo': anomaliasxtipoorden[0].activo
                    }
                else:
                    dados_lancamento = {
                        'id_anomalia': anomalia.id_anomalia,
                        'descripcion': anomalia.descripcion,
                        'foto_obligatoria': None,
                        'observacion_obligatoria': None,
                        'observacion_tabulada': None,
                        'datos_medidor': None,
                        'activo': 0
                    }

                lista_resultado.append(dados_lancamento)
            context['anomalias'] = lista_resultado
            context['tipo_orden'] = tipo_orden
            return render_to_response('data_admin/tipo_orden/_propiedades.html', context)


    except Exception as e:
        log.error("Propiedades Error {}".format(e))
        return HttpResponse(status=500)
    return HttpResponse(status=500)


def anomaliaxtipo_cflags(request):
    context = RequestContext(request)
    try:

        id = request.POST['id']
        # print(id)
        name = request.POST['name']
        # print(name)
        action = request.POST['action']
        # print(action)

        anomalia = Anomalia.objects.get(id_anomalia=id)
        anomaliato = AnomaliaXTipo.objects.get(anomalia=anomalia)
        # print(anomaliato)
        '''
      if action == '0' or action == '1':

         anomaliato.foto(action)
         return JsonResponse({"accion": str(action)})
      elif action == '2' :
         anomaliato.obs('0')
         return JsonResponse({"accion": action})
      elif action == '3':
         anomaliato.obs('1')
         return JsonResponse({"accion": action})
      elif action == '4':
         anomaliato.obst('0')
         return JsonResponse({"accion": action})
      elif action == '5':
         anomaliato.obst('1')
         return JsonResponse({"accion": action})
      elif action == '6':
         anomaliato.medidor('0')
         return JsonResponse({"accion": action})
      elif action == '7':
         anomaliato.medidor('1')
         return JsonResponse({"accion": action})
      '''
        if action == '8':
            anomaliato.enable('0')
            writeAudit("anomalías tipo ordenes", "edicion", request.user,
                       "Deshabilitar anomalía {} para el tipo de orden {}".format(anomalia, anomaliato.tipo_orden))

            return JsonResponse({"accion": action})
        elif action == '9':
            writeAudit("anomalías tipo ordenes", "edicion", request.user,
                       "Habilitar anomalía {} para el tipo de orden {}".format(anomalia, anomaliato.tipo_orden))

            anomaliato.enable('1')
            return JsonResponse({"accion": action})
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)
    return HttpResponse(status=200)


###### ------------------------- ADMIN RUTA_SUM  ------------------------- ######
@login_required(login_url=settings.LOGIN_PAGE)
def rutasum_main(request):
    localidad1 = []
    context = RequestContext(request)
    localidad = PuntoDeSuministro.objects.filter(rutasum=None, estado_suministro=1).values('id_localidad',
                                                                                           'localidad').distinct().order_by(
        'id_localidad')
    # print(str(localidad.query))
    form = rutasumForm()
    context['form'] = form
    context['localidad'] = localidad
    return render_to_response('data_admin/ruta_sum/_ruta_sum.html', context)


@csrf_exempt
@login_required(login_url=settings.LOGIN_PAGE)
def rutasum_tabla(request):
    try:
        context = RequestContext(request)
        id_centro = request.POST['id_oficina']
        # print(id_centro)
        if id_centro:
            centro = WorkUnit.objects.get(pk=id_centro)
            ruta_oficina = RutaSum.objects.filter(oficina=id_centro)
            context['rutasum'] = ruta_oficina
        return render_to_response('data_admin/ruta_sum/tabla_rutasum.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def rutasum_edit(request):
    try:
        context = RequestContext(request)
        id = request.POST['id']
        rutasum = RutaSum.objects.get(idrutasum=id)
        suministro = PuntoDeSuministro.objects.filter(rutasum=rutasum).count()
        # print(suministro)
        if suministro > 0:
            return HttpResponse(status=500)

        context['rutasum'] = rutasum
        context['suministro'] = suministro
        form = rutasumForm(instance=rutasum)
        context['form'] = form
        return render_to_response('data_admin/ruta_sum/edit_rutasum.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def rutasum_new(request):
    try:
        context = RequestContext(request)
        id_centro = request.POST['id_centro']
        centro = WorkUnit.objects.get(pk=id_centro)
        form = rutasumForm(initial={'oficina': centro})
        form.oficina = centro
        context['form'] = form
        return render_to_response('data_admin/ruta_sum/edit_rutasum.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def rutasum_delete(request):
    try:
        context = RequestContext(request)
        id_centro = request.POST['id_oficina']
        id_ruta = request.POST['id_rutasum']
        rutasumdelete = RutaSum.objects.get(pk=id_ruta, oficina=id_centro)
        rutasum = RutaSum.objects.filter(oficina=id_centro)
        if rutasumdelete.Frecuencia == 'B':
            # print('pasa')
            suministro = PuntoDeSuministro.objects.filter(rutasum=rutasumdelete) | PuntoDeSuministro.objects.filter(
                rutasum2=rutasumdelete)

        valor = suministro.count()
        print(valor)
        # print('pasa')

        if valor == 0:
            rutasumdelete.delete()
            writeAudit("gestion RutaSum", "Eliminar", request.user, "Se elimino la ruta {}".format(rutasumdelete))
            context['rutasum'] = rutasum
            return render_to_response('data_admin/ruta_sum/tabla_rutasum.html', context)
        else:
            if Ruta.objects.filter(rutasum=rutasumdelete).exists():
                # print('aca')
                context['rutasum'] = rutasum
                writeAudit("gestion RutaSum", "Eliminar", request.user,
                           "No se puede eliminar, Ya se creo una Ruta para esta Rutasuministro  ")
                return render_to_response('data_admin/ruta_sum/tabla_rutasum.html', context, status=500)
            else:
                # print('llega else')
                if rutasumdelete.Frecuencia == 'B':
                    suministros = PuntoDeSuministro.objects.filter(rutasum=rutasumdelete).update(rutasum=None,
                                                                                                 secuencia_teorica=None) | PuntoDeSuministro.objects.filter(
                        rutasum2=rutasumdelete).update(rutasum2=None, secuencia_teorica2=None)
                    rutasumdelete.delete()
                    context['rutasum'] = rutasum
                    return render_to_response('data_admin/ruta_sum/tabla_rutasum.html', context)
        context['rutasum'] = rutasum
        return render_to_response('data_admin/ruta_sum/tabla_rutasum.html', context)

    except Exception as e:

        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def rutasum_save(request):
    context = RequestContext(request)
    try:
        id = request.POST['id_rutasum']
        accion = request.POST['accion']
        # print("Id "+id)
        # print("Accion save"+accion)
        if accion == 'edit':
            rutasum = RutaSum.objects.get(idrutasum=id)

            form = rutasumForm(request.POST, instance=rutasum)

            if form.is_valid():
                # print('validar save')
                id_workunit = form.cleaned_data['oficina']
                # print(id_workunit.id_workunit)
                form.save()
                # print('llega save')
                writeAudit("gestion Rutasum", "edicion", request.user, form.cleaned_data)
                oficinas = WorkUnit.objects.all()
                rutasums = RutaSum.objects.filter(oficina=id_workunit)
                # print(rutasums)
                context['rutasum'] = rutasums

                return render_to_response('data_admin/ruta_sum/tabla_rutasum.html', context)
            else:
                # print(form.errors.as_json())
                context['form'] = form
                return HttpResponse(form.errors.as_json(), status=301)

        else:

            form = rutasumForm(request.POST)
            if form.is_valid():
                # print('entra')
                id_workunit = form.cleaned_data['oficina']
                rutasum = form.cleaned_data['rutasum']
                itinerario = form.cleaned_data['itinerario']
                id_rutasum = id_workunit.id_workunit + rutasum + itinerario
                # print(id_rutasum)
                try:
                    rs = RutaSum.objects.get(idrutasum=id_rutasum)
                    return HttpResponse(status=300)
                except Exception as e:
                    ruta = RutaSum.objects.create(idrutasum=id_rutasum, oficina=id_workunit)
                    ruta.itinerario = itinerario
                    ruta.Frecuencia = 'B'
                    ruta.rutasum = rutasum
                    ruta.save()
                writeAudit("gestion RutaSum", "nuevo", request.user, form.cleaned_data)
                # print('aca')
                oficinas = WorkUnit.objects.all()
                rutasums = RutaSum.objects.filter(oficina=id_workunit)
                # print(rutasums)
                context['rutasum'] = rutasums

                return render_to_response('data_admin/ruta_sum/tabla_rutasum.html', context, status=200)
            else:
                # print(form.errors.as_json())
                context['form'] = form
                return HttpResponse(status=300)

    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)

    context['rutasums'] = rutasums
    context['form'] = form
    return render_to_response('data_admin/ruta_sum/edit_rutasum.html', context)


@csrf_exempt
def suministro_tabla(request):
    try:
        context = RequestContext(request)
        id_rutasum = request.POST['idrutasum']
        dic_suministro = []
        lista = []
        if id_rutasum:
            # print('pasa')
            # print(id_rutasum)
            ruta_oficina = RutaSum.objects.get(idrutasum=id_rutasum)
            if ruta_oficina.Frecuencia == 'B':
                suministros = PuntoDeSuministro.objects.filter(rutasum2__isnull=True, rutasum=ruta_oficina,
                                                               Frecuencia='M') | PuntoDeSuministro.objects.filter(
                    rutasum__isnull=False, rutasum2=ruta_oficina, Frecuencia='M') | PuntoDeSuministro.objects.filter(
                    rutasum__isnull=True, rutasum2=ruta_oficina, Frecuencia='B') | PuntoDeSuministro.objects.filter(
                    rutasum=ruta_oficina, rutasum2__isnull=False, Frecuencia='M').order_by('secuencia_teorica2')
                # print(suministros)
                # print('pasa1')
            for sumin in suministros:
                suministro = PuntoDeSuministro.objects.get(punto_suministro=sumin.punto_suministro)
                # print(suministro)
                # print(suministro.rutasum2)
                if suministro.rutasum == ruta_oficina:
                    datos = {
                        'secuencia_teorica': suministro.secuencia_teorica,
                        'punto_suministro': suministro.punto_suministro,
                        'Frecuencia': suministro.Frecuencia,
                        'cliente': suministro.cliente.codigo,
                        'calle': suministro.calle,
                        'numero_puerta': suministro.numero_puerta,
                        'id_localidad': suministro.id_localidad,
                        'barrio': suministro.barrio,
                        'rutasum': suministro.rutasum
                    }
                elif suministro.rutasum2 == ruta_oficina:
                    datos = {
                        'secuencia_teorica': suministro.secuencia_teorica2,
                        'punto_suministro': suministro.punto_suministro,
                        'Frecuencia': suministro.Frecuencia,
                        'cliente': suministro.cliente.codigo,
                        'calle': suministro.calle,
                        'numero_puerta': suministro.numero_puerta,
                        'id_localidad': suministro.id_localidad,
                        'barrio': suministro.barrio,
                        'rutasum': suministro.rutasum2
                    }

                # print(datos)
                dic_suministro.append(datos)
                lista = sorted(dic_suministro, key=itemgetter('secuencia_teorica'))
            # print(lista)
            context['suministros'] = lista
            return render_to_response('data_admin/ruta_sum/tabla_suministros.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def tabla_suministros_sin_ruta(request):
    try:
        context = RequestContext(request)
        id_ruta = request.POST['id_ruta']
        id_centro = request.POST['id_oficina']
        id_localidad = request.POST['id_localidad']

        ruta = RutaSum.objects.get(idrutasum=id_ruta)

        if ruta.Frecuencia == 'B':
            suministros = PuntoDeSuministro.objects.filter(rutasum__isnull=False, rutasum2__isnull=True,
                                                           id_localidad=id_localidad, Frecuencia='M',
                                                           estado_suministro=1).exclude(
                rutasum=ruta) | PuntoDeSuministro.objects.filter(rutasum__isnull=True, rutasum2__isnull=False,
                                                                 id_localidad=id_localidad, Frecuencia='M',
                                                                 estado_suministro=1).exclude(
                rutasum2=ruta) | PuntoDeSuministro.objects.filter(rutasum__isnull=True, rutasum2__isnull=True,
                                                                  id_localidad=id_localidad, Frecuencia='M',
                                                                  estado_suministro=1) | PuntoDeSuministro.objects.filter(
                rutasum2=None, id_localidad=id_localidad, Frecuencia='B', estado_suministro=1)

            context['suministros_sinRuta'] = suministros
            return render_to_response('data_admin/ruta_sum/tabla_sum_asignar.html', context)




    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def trasferir_suministro(request, ):
    try:
        lista = []
        context = RequestContext(request)
        # print('entro transferir')
        id_centro = request.POST['id_centro']
        id_suministros = request.POST['id_suministros']
        id_rutasum = request.POST['id_rutasum']
        id_localidad = request.POST['id_localidad']
        ruta = RutaSum.objects.get(idrutasum=id_rutasum)
        # print('rutasum {}'.format(ruta.idrutasum))
        if ruta.Frecuencia == 'B':
            ptosumin = PuntoDeSuministro.objects.filter(rutasum=id_rutasum, Frecuencia='M').update(rutasum=None,
                                                                                                   secuencia_teorica=None) | PuntoDeSuministro.objects.filter(
                rutasum2=id_rutasum, Frecuencia='B').update(rutasum2=None,
                                                            secuencia_teorica2=None) | PuntoDeSuministro.objects.filter(
                rutasum2=id_rutasum, Frecuencia='M').update(rutasum2=None, secuencia_teorica2=None)

        # print(id_localidad)
        if id_suministros == '[]':
            suministrosnuevos = PuntoDeSuministro.objects.filter(rutasum=None, localidad=id_localidad)
            context['suministros_sinRuta'] = suministrosnuevos
            return render_to_response('data_admin/ruta_sum/tabla_sum_asignar.html', context)
        else:
            # print('llega')
            id_suministros = id_suministros.replace('[', '').replace(']', '').rstrip(',').split(',')
            for i in id_suministros:
                lista = i.split('|')
                suministro = lista[1]
                # print(ruta)
                if ruta.Frecuencia == 'B':
                    # print('pasa')
                    suministros = PuntoDeSuministro.objects.get(punto_suministro=suministro)
                    if suministros.Frecuencia == 'M':
                        if suministros.rutasum != None:
                            # print('llega1')
                            suministros.rutasum2 = ruta
                            suministros.secuencia_teorica2 = lista[0]
                            suministros.save()
                        else:
                            # print('entra')
                            suministros.rutasum = ruta
                            suministros.secuencia_teorica = lista[0]
                            suministros.save()


                    else:

                        suministros = PuntoDeSuministro.objects.get(punto_suministro=suministro)
                        suministros.rutasum2 = ruta
                        suministros.secuencia_teorica2 = lista[0]
                        suministros.save()

        suministrosnuevos = PuntoDeSuministro.objects.filter(rutasum=None, localidad=id_localidad, estado_suministro=1)
        # print(suministrosnuevos)
        writeAudit("gestion AgregarSuministro", "Guardar", request.user,
                   "se guardaron suministros {} para la ruta {}".format(id_suministros, ruta))
        context['suministros_sinRuta'] = suministrosnuevos
        return render_to_response('data_admin/ruta_sum/tabla_sum_asignar.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def suministro_delete(request):
    try:
        lista = []
        context = RequestContext(request)
        id_centro = request.POST['id_centro']
        id_ruta = request.POST['id_rutasum']
        id_suministro = request.POST['id_suministros']
        id_suministros = id_suministro.replace('[', '').replace(']', '').rstrip(',').split(',')
        for i in id_suministros:
            # print(i)
            lista = i.split('|')
            suministro = lista[1]
            # print(suministro)
            suministro = PuntoDeSuministro.objects.get(punto_suministro=suministro)
            suministro.rutasum = None
            suministro.secuencia_teorica = None
            suministro.save()
        suministrosRuta = PuntoDeSuministro.objects.filter(rutasum=id_ruta).order_by('secuencia_teorica')
        sec = 0
        for i in suministrosRuta:
            sec = sec + 10
            i.secuencia_teorica = sec
            i.save()
        context['suministros'] = suministrosRuta
        return render_to_response('data_admin/ruta_sum/tabla_suministros.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


# ADMIN reportes

# @login_required(login_url=settings.LOGIN_PAGE)
# def reporte_main(request):
#    context = RequestContext(request)
#    print("geofencing main")
#    return render_to_response('data_admin/Reportes/Reporte.html', context)
#
# @csrf_exempt
# def tabla_rutasuministro(request):
#    try:
#        context = RequestContext(request)
#        id_centro = request.POST['id_oficina']
#        print(id_centro)
#        if id_centro:
#           centro = WorkUnit.objects.get(pk=id_centro)
#           print(centro)
#           ruta_oficina =RutaSum.objects.filter(oficina=id_centro)
#           rutas = []
#           for item in ruta_oficina:
#               rutas.append(item.rutasum)
#           print(rutas)
#           rutasum = RutaSum.objects.filter(rutasum__in=rutas)
#           context['rutasum'] = rutasum
#        return render_to_response('data_admin/Reportes/tabla_rutasuministro.html', context)
#    except Exception as e:
#        print ("Error {}".format(e))
#        return HttpResponse(status=500)
#


###### ------------------------- DIVISION  ------------------------- ######
@login_required(login_url=settings.LOGIN_PAGE)
def dividir(request):
    try:
        context = RequestContext(request)
        # print("###### ------------------------- DIVISION  ------------------------- ######")
        # id_ruta = request.POST['id_ruta']
        # ruta = Ruta.objects.get(id=id_ruta)
        # print("Dividir {}".format(ruta))
        # divisiones = Ruta.objects.filter(ruta=ruta.ruta,itinerario=ruta.itinerario,plan__isnull=False )
        # context['divisiones'] = divisiones
        # context['ruta'] = ruta
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)

    return render_to_response('ordenes/division/_division.html', context)


def generardivision(request):
    try:
        context = RequestContext(request)
        # print('generardivision')
        id_ruta = request.POST['id_ruta']
        objRuta = Ruta.objects.get(id=id_ruta)
        # print("Dividir {}".format(objRuta))
        cantidad = request.POST['cantidad']
        cant_divisiones = 0
        divisiones = Ruta.objects.filter(ciclo=objRuta.ciclo, ruta=objRuta.ruta, itinerario=objRuta.itinerario,
                                         plan__isnull=False)
        if divisiones:
            if len(divisiones) + int(cantidad) > 10:
                return HttpResponse(status=301)
            cant_divisiones = len(divisiones)

        cantgenerar = cant_divisiones + int(cantidad) + 1
        numero = 0
        for x in range(cant_divisiones + 1, cantgenerar):

            while True:
                numero = numero + 1
                divisiones = Ruta.objects.filter(ciclo=objRuta.ciclo, ruta=objRuta.ruta, itinerario=objRuta.itinerario,
                                                 plan=str(numero))
                # print("Divisiones {} {}".format(len(divisiones),numero))
                if len(divisiones) == 0:
                    _ruta = Ruta()
                    _ruta.oficina = objRuta.oficina
                    _ruta.ciclo = objRuta.ciclo
                    _ruta.ruta = objRuta.ruta
                    _ruta.itinerario = objRuta.itinerario
                    _ruta.anio = objRuta.anio
                    _ruta.plan = str(numero)
                    _ruta.cantidad = 0
                    _ruta.fecha_generacion = objRuta.fecha_generacion
                    _ruta.fecha_estimada_resolucion = objRuta.fecha_estimada_resolucion
                    _ruta.estado = EstadoRuta.objects.get(pk=1)
                    _ruta.save()
                    writeAudit("división rutas", "agregar división", request.user,
                               "Generó división {} para la ruta {} {} {}".format(str(numero), objRuta.ruta,
                                                                                 objRuta.itinerario, objRuta.ciclo))

                    # print(str(numero))
                    break

        divisiones = Ruta.objects.filter(ruta=objRuta.ruta, itinerario=objRuta.itinerario, plan__isnull=False)
        context['divisiones'] = divisiones
        context['ruta'] = objRuta
        return render_to_response('ordenes/division/_table_divisiones.html', context)

    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)

    return render_to_response('ordenes/division/_division.html', context)


def quitardivision(request):
    try:
        # print('Borrar Division ruta')
        context = RequestContext(request)
        id = request.POST['id']
        division = Ruta.objects.get(id=id)
        # print("Division {}".format(division.ruta))

        ruta = Ruta.objects.get(ruta=division.ruta, itinerario=division.itinerario, ciclo=division.ciclo,
                                plan__isnull=True)
        # print(ruta)
        ordT = OrdenDeTrabajo.objects.filter(ruta=division)
        # print('Cantidad de ordenes a liberar {}'.format(len(ordT)))
        ruta.cantidad = ruta.cantidad + len(ordT)
        ruta.save()
        ordT.update(ruta=ruta)
        writeAudit("división rutas", "quitar división", request.user,
                   "Borró división {} para la ruta {} {} {} liberó {} ordenes".format(division.plan, ruta.ruta,
                                                                                      ruta.itinerario, ruta.ciclo,
                                                                                      len(ordT)))

        division.delete()

        divisiones = Ruta.objects.filter(ruta=ruta.ruta, itinerario=ruta.itinerario, ciclo=ruta.ciclo,
                                         plan__isnull=False)
        # print(divisiones)
        context['divisiones'] = divisiones
        context['ruta'] = ruta
        return render_to_response('ordenes/division/_table_divisiones.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@csrf_exempt
def division_route(request):
    try:
        # print('Division ruta')
        context = RequestContext(request)
        id_centro = request.POST['id_oficina']
        # print(id_centro)
        if id_centro:
            centro = WorkUnit.objects.get(pk=id_centro)
            # print(centro)

            rutas = Ruta.objects.filter(oficina=centro, estado=1, plan__isnull=True)

            context['rutas'] = rutas
            # print(rutas)

        return render_to_response('ordenes/division/_table_routes.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@csrf_exempt
def list_divisiones(request):
    try:
        # print('Division ruta')
        context = RequestContext(request)
        id_ruta = request.POST['id_ruta']
        # print(id_ruta)
        ruta = Ruta.objects.get(id=id_ruta)
        divisiones = Ruta.objects.filter(ruta=ruta.ruta, itinerario=ruta.itinerario, plan__isnull=False)
        # print(divisiones)
        context['divisiones'] = divisiones
        context['ruta'] = ruta
        return render_to_response('ordenes/division/_table_divisiones.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@csrf_exempt
def list_suministros_ruta(request):
    try:
        # print('Lista suministros ruta')
        context = RequestContext(request)
        id_ruta = request.POST['id_ruta']
        todas = 2
        # print(id_ruta)
        # print("Todas "+str(todas))
        if id_ruta:
            request.session['id_ruta'] = id_ruta
            request.session['todas'] = todas

            # ruta = Ruta.objects.get(pk=id_ruta)
            # print(ruta)
            # falta el filtro por todas
            # sumin = PuntoDeSuministro.objects.filter(ruta=ruta)

            context['sumin'] = []

        return render_to_response('ordenes/division/_table_suministros_ruta.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@csrf_exempt
def mover_ordenes(request):
    try:
        # print('MOver ordenes')
        context = RequestContext(request)
        ords = request.POST['ordenes']

        if ords == '':
            desde = request.POST['desde']
            hasta = request.POST['hasta']
            ordT = OrdenDeTrabajo.objects.filter(secuencial_registro__gte=desde, secuencial_registro__lte=hasta)
        else:
            ordenes = ords.split(",")
            # print(ordenes)
            ordT = OrdenDeTrabajo.objects.filter(numero_orden__in=ordenes)
        old = request.POST['old']
        new = request.POST['new']

        nRuta = Ruta.objects.get(id=new)
        oRuta = Ruta.objects.get(id=old)

        # print(ordT)
        ordT.update(ruta=nRuta)

        nRuta.cantidad = nRuta.cantidad + len(ordT)
        nRuta.save()

        oRuta.cantidad = oRuta.cantidad - len(ordT)
        oRuta.save()
        writeAudit("división rutas", "mover ordenes", request.user,
                   " {} ordenes fueron movidas de {} {} {} {} a {} {} {} {}".format(len(ordT), oruta.ruta,
                                                                                    oruta.itinerario, oruta.ciclo,
                                                                                    oruta.plan, cruta.ruta,
                                                                                    cruta.itinerario, cruta.ciclo,
                                                                                    cruta.plan))

        return HttpResponse(status=200)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@csrf_exempt
def list_suministros_division(request):
    try:
        # print('Lista suministros division')
        context = RequestContext(request)
        id_ruta = request.POST['id_ruta']
        todas = 2
        # print(id_ruta)
        # print("Todas "+str(todas))
        if id_ruta:
            request.session['id_ruta'] = id_ruta
            request.session['todas'] = todas

            # ruta = Ruta.objects.get(pk=id_ruta)
            # print(ruta)
            # falta el filtro por todas
            # sumin = PuntoDeSuministro.objects.filter(ruta=ruta)

            context['sumin'] = []

        return render_to_response('ordenes/division/_table_suministros_division.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


###### ------------------------- SEMANA ------------------------- ######

@login_required(login_url=settings.LOGIN_PAGE)
def semana(request):
    try:
        context = RequestContext(request)

        try:
            semana = SemanaXUser.objects.get(usuario=request.user)
            context['semana'] = semana
            form = semanaForm(instance=semana)


        except:
            form = semanaForm(initial={'usuario': request.user})

        context['form'] = form
        return render_to_response('config/_semana.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


def semana_save(request):
    context = RequestContext(request)
    print('semana_save')
    try:
        try:
            semana = SemanaXUser.objects.get(usuario=request.user)
            print(semana)
            form = semanaForm(request.POST, instance=semana)
            print(form)
            if form.is_valid():
                print('entraeditar')
                form.save()
                writeAudit("semana", "editar", request.user, form.cleaned_data)
                return HttpResponse(status=200)
            return HttpResponse('Complete los campos obligatorios', status=301)
        except Exception as e:
            print("exceptsemana {}".format(e))
            form = semanaForm(request.POST)
            if form.is_valid():
                print('entranueva')
                new_parametro = form.save()
                writeAudit("semana", "nueva", request.user, form.cleaned_data)
                return HttpResponse(status=200)
            return HttpResponse('Complete los campos obligatorios', status=301)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)
    print('from1')
    form = semanaForm(initial={'usuario': request.user})
    context['form'] = form
    return render_to_response('config/_semana.html', context)

    ###### ------------------------- GENERACION ------------------------- ######


@login_required(login_url=settings.LOGIN_PAGE)
def generacion_main(request):
    context = RequestContext(request)
    form = generacionForm()
    context['form'] = form
    return render_to_response('ordenes/generacion/_generacion.html', context)


@csrf_exempt
def generacion_ruta(request):
    try:
        context = RequestContext(request)
        id_centro = request.POST['id_oficina']
        listas = []
        if id_centro:
            centro = WorkUnit.objects.get(pk=id_centro)

            rutas_oficina = RutaSum.objects.filter(oficina=id_centro, Frecuencia='B')
            # sumin = PuntoDeSuministro.objects.filter(rutasum__in=rutas_oficina)
            # sumin.count('rutasum')
            for ruta in rutas_oficina:

                if ruta.Frecuencia == 'B':
                    # print(ruta.Frecuencia=='M')
                    countsuministro = PuntoDeSuministro.objects.filter(rutasum2__isnull=True, rutasum=ruta,
                                                                       Frecuencia='M',
                                                                       estado_suministro=1) | PuntoDeSuministro.objects.filter(
                        rutasum__isnull=False, rutasum2=ruta, Frecuencia='M',
                        estado_suministro=1) | PuntoDeSuministro.objects.filter(rutasum__isnull=True, rutasum2=ruta,
                                                                                Frecuencia='B',
                                                                                estado_suministro=1) | PuntoDeSuministro.objects.filter(
                        rutasum=ruta, rutasum2__isnull=False, Frecuencia='M', estado_suministro=1)
                    cant = countsuministro.count()
                datos = {'idrutasum': ruta.idrutasum,
                         'rutasum': ruta.rutasum,
                         'itinerario': ruta.itinerario,
                         'cantidad': cant}
                listas.append(datos)
            # print(listas)
            total_suministros = rutas_oficina.annotate(total_suministros=Count('puntodesuministro'))
            # print('puntos suministro count {}'.format(total_suministros.query))

            context['cantidad'] = listas
            context['rutasum'] = total_suministros
        return render_to_response('ordenes/generacion/_tabla_rutasum.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def generar(request):
    form = generacionForm()
    lista = []
    valor1 = ''
    try:
        if request.method == 'POST':

            context = RequestContext(request)
            id_centro = request.POST['id_centro']
            rutas = eval(request.POST['rutas'])
            ciclo = request.POST['ciclo']
            fecha = request.POST['fecha']
            # print(fecha)
            # print(ciclo)
            # print(rutas)
            fer = datetime.strptime(fecha, "%d/%m/%Y")

            cp = []
            cpo = []
            tipo_orden = TipoOrden.objects.get(tipo_orden='LECT')
            for ruta in rutas:
                datosruta = RutaSum.objects.get(idrutasum=ruta)
                # print(datosruta)
                if datosruta.Frecuencia == 'B':
                    total_suministros = PuntoDeSuministro.objects.filter(rutasum2__isnull=True, rutasum=datosruta,
                                                                         Frecuencia='M',
                                                                         estado_suministro=1) | PuntoDeSuministro.objects.filter(
                        rutasum__isnull=False, rutasum2=datosruta, Frecuencia='M',
                        estado_suministro=1) | PuntoDeSuministro.objects.filter(rutasum__isnull=True,
                                                                                rutasum2=datosruta, Frecuencia='B',
                                                                                estado_suministro=1) | PuntoDeSuministro.objects.filter(
                        rutasum=datosruta, rutasum2__isnull=False, Frecuencia='M', estado_suministro=1)
                    cant_sum = total_suministros.count()
                datosoficina = WorkUnit.objects.get(pk=id_centro)
                # print('llega')
                rutarep = Ruta.objects.filter(rutasum=datosruta, anio=ciclo)
                # print(rutarep)
                # print('paso')
                if valor1 in '':
                    # print('entra')
                    valor1 = '0'
                if rutarep.exists():
                    for i in rutarep:
                        valor1 += str(i) + ','

                    # print('existe')
                    continue
                else:

                    # print('entra else')
                    cp.append(Ruta(idruta=id_centro + datosruta.rutasum + datosruta.itinerario.zfill(4) + ciclo,
                                   rutasum=datosruta,
                                   oficina=datosoficina,
                                   ciclo=ciclo,
                                   ruta=datosruta.rutasum,
                                   itinerario=datosruta.itinerario,
                                   plan='',
                                   anio=ciclo,
                                   cantidad=cant_sum,
                                   cantidad_leido=0,
                                   fecha_generacion=datetime.now(),
                                   fecha_estimada_resolucion=fer,
                                   estado=1,
                                   fecha_hora_importacion=datetime.now().strftime('%Y%m%d%H%M%S')
                                   ))
            # print(cp)
            Ruta.objects.bulk_create(cp)
            for ruta in cp:
                rutanueva = Ruta.objects.get(idruta=ruta.idruta, ciclo=ciclo)
                # print('rutanueva {}'.format(rutanueva))
                # print(ruta.idruta)
                datosruta = RutaSum.objects.get(idrutasum=rutanueva.rutasum.idrutasum)
                # print(datosruta)
                if datosruta.Frecuencia == 'B':
                    datosum = PuntoDeSuministro.objects.filter(rutasum2__isnull=True, rutasum=datosruta, Frecuencia='M',
                                                               estado_suministro=1) | PuntoDeSuministro.objects.filter(
                        rutasum__isnull=False, rutasum2=datosruta, Frecuencia='M',
                        estado_suministro=1) | PuntoDeSuministro.objects.filter(rutasum__isnull=True,
                                                                                rutasum2=datosruta, Frecuencia='B',
                                                                                estado_suministro=1) | PuntoDeSuministro.objects.filter(
                        rutasum=datosruta, rutasum2__isnull=False, Frecuencia='M', estado_suministro=1)
                    # print('datosum {}'.format(datosum))
                    for sumin in datosum:

                        if sumin.rutasum == datosruta:
                            consumo = Consumo.objects.get(aparato=sumin.aparato)
                            date = (str(ciclo) + str(datetime.now().day))
                            # print(date)
                            cpo.append(OrdenDeTrabajo(
                                numero_orden=id_centro + date + datosruta.rutasum + datosruta.itinerario.zfill(4) + str(
                                    sumin.secuencia_teorica).zfill(4),
                                punto_suministro=sumin,
                                tipo_orden=tipo_orden,
                                secuencial_registro=sumin.secuencia_teorica,
                                secuencia_teorica=sumin.secuencia_teorica,
                                ruta=rutanueva,
                                consumo=consumo
                            ))
                            # print(cpo)
                        else:
                            consumo = Consumo.objects.get(aparato=sumin.aparato)
                            date = (str(ciclo) + str(datetime.now().day))
                            # print(date)
                            cpo.append(OrdenDeTrabajo(
                                numero_orden=id_centro + date + datosruta.rutasum + datosruta.itinerario.zfill(4) + str(
                                    sumin.secuencia_teorica2).zfill(4),
                                punto_suministro=sumin,
                                tipo_orden=tipo_orden,
                                secuencial_registro=sumin.secuencia_teorica2,
                                secuencia_teorica=sumin.secuencia_teorica2,
                                ruta=rutanueva,
                                consumo=consumo
                                ))

            OrdenDeTrabajo.objects.bulk_create(cpo)
            # print('rutas {}'.format(rutas))
            valor = ''
            for i in cp:
                valor += str(i) + ','
            if valor in '':
                valor = '0'
            writeAudit("generacion Ordenes", "generacion", request.user,
                       "Ordenes generadas para la ruta: {} .Rutas repetidas: {}".format(valor, valor1))
            return HttpResponse('Órdenes generadas para la ruta: {} .Rutas repetidas: {}'.format(valor, valor1),
                                status=200)

    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


###### ------------------------- ASIGNACION  ------------------------- ######
@login_required(login_url=settings.LOGIN_PAGE)
def asignacion_main(request):
    try:
        context = RequestContext(request)
        context['tecnicos'] = []
        try:
            semana = SemanaXUser.objects.get(usuario=request.user)
            context['semana'] = semana
        except:
            pass
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)

    return render_to_response('ordenes/asignacion/_asignacion.html', context)


@login_required(login_url=settings.LOGIN_PAGE)
def asignacion_tech(request):
    try:

        context = RequestContext(request)
        id_centro = request.POST['id_oficina']
        # print(id_centro)
        if id_centro:
            centro = WorkUnit.objects.get(pk=id_centro)
            tecnicos_oficina = OficinaXTecnico.objects.filter(oficina=id_centro, fecha_baja=None)
            tecs = []
            for item in tecnicos_oficina:
                tecs.append(item.tecnico.codigo)
                # print('tecs {}'.format(tecs))
            tecnicos = Tecnico.objects.filter(codigo__in=tecs, terminal_portatil__isnull=False)
            # print(len(tecnicos))
            context['tecnicos'] = tecnicos
            # print(tecnicos)

        return render_to_response('ordenes/asignacion/rutas/_table_techs.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def asignacion_route(request):
    try:

        context = RequestContext(request)
        id_centro = request.POST['id_oficina']
        _result = []
        semana = request.POST['semana']
        if id_centro:
            centro = WorkUnit.objects.get(pk=id_centro)
            if semana == 'TODAS' or semana == '':
                # rutas = Ruta.objects.filter(oficina=centro,estado__in=STATUS_ENABLED)
                rutas = Ruta.objects.filter(oficina=centro, estado__in=STATUS_ENABLED).values('idruta', 'oficina',
                                                                                              'ciclo', 'ruta',
                                                                                              'itinerario', 'anio',
                                                                                              'fecha_estimada_resolucion',
                                                                                              'cantidad',
                                                                                              'cantidad_leido')
            else:
                rutas = Ruta.objects.filter(oficina=centro, anio=semana, estado__in=STATUS_ENABLED).values('idruta',
                                                                                                           'oficina',
                                                                                                           'ciclo',
                                                                                                           'ruta',
                                                                                                           'itinerario',
                                                                                                           'anio',
                                                                                                           'fecha_estimada_resolucion',
                                                                                                           'cantidad',
                                                                                                           'cantidad_leido')
                # rutas = Ruta.objects.filter(oficina=centro,anio=semana, estado__in=STATUS_ENABLED)
                
            # Busco órdenes de las rutas con PS que tengan un Segmento asociado
            
            ordenes_por_ruta = OrdenDeTrabajo.objects.filter(
                ruta__in=[ruta['idruta'] for ruta in rutas],
                punto_suministro__segmentosum_id__isnull=False
            ).values('ruta', 'estado').annotate(total=Count('numero_orden'))
            
            ordenes_pendientes = defaultdict(int)
            total_ordenes = defaultdict(int)
            
            for item in ordenes_por_ruta:
                ruta_id = item['ruta']
                estado = item['estado']
                
                if estado in STATUS_ENABLED:
                    ordenes_pendientes[ruta_id] += item['total']
                if estado in STATUS_ENABLED + [3, 7]:
                    total_ordenes[ruta_id] += item['total']

            for ruta in rutas:
                segmentos_pendientes = ordenes_pendientes.get(ruta['idruta'], 0)
                segmento_total = total_ordenes.get(ruta['idruta'], 0)
                
                _result.append({'idruta': ruta['idruta'],
                                'oficina': ruta['oficina'],
                                'ciclo': ruta['ciclo'],
                                'ruta': ruta['ruta'],
                                'itinerario': ruta['itinerario'],
                                'anio': ruta['anio'],
                                'fecha_estimada_resolucion': ruta['fecha_estimada_resolucion'],
                                'cantidad': ruta['cantidad'],
                                'cantidad_leido': str(int(ruta['cantidad']) - int(ruta['cantidad_leido']) - segmento_total),
                                'segmentos': segmentos_pendientes,
                                })

            context['rutas'] = _result

        return render_to_response('ordenes/asignacion/rutas/_table_routes.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def asignacion_asignaciones(request):
    try:
        # print("Asignacion asignaciones")
        context = RequestContext(request)
        id_centro = request.POST['id_oficina']
        valuecheck = request.POST['valuecheck']
        # print(id_centro)
        if id_centro:
            centro = WorkUnit.objects.get(pk=id_centro)
            # print(centro)
            if valuecheck == '0':
                rutas = Ruta.objects.filter(oficina=centro, estado=3, usuario_asignacion=request.user,
                            ordendetrabajo__punto_suministro__segmentosum_id__isnull=True).exclude(
                            flag_asignacion_guardada=1).annotate(
                            pendientes=Count(
                                'ordendetrabajo',
                                filter=Q(ordendetrabajo__estado__in=[3],
                                        ordendetrabajo__punto_suministro__segmentosum_id__isnull=True)
                            )
                        )
            else:
                rutas = Ruta.objects.filter(oficina=centro, estado=3, usuario_asignacion=request.user,
                            flag_asignacion_guardada=1,
                            ordendetrabajo__punto_suministro__segmentosum_id__isnull=True).annotate(
                            pendientes=Count(
                                'ordendetrabajo',
                                filter=Q(ordendetrabajo__estado__in=[3],
                                        ordendetrabajo__punto_suministro__segmentosum_id__isnull=True)
                            )
                        )
            context['rutasasignadas'] = rutas
            # print(rutas)

        return render_to_response('ordenes/asignacion/rutas/_table_asignados.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def asignacion_desasignar(request):
    try:
        # print("Asignacion desasignar")
        context = RequestContext(request)

        _log=Logger()
        _parametro=Parametro.objects.get(pk='P_QW_PATH_LOGS')
        path=_parametro.valor_1
        path1=path
        _log.logsetlevel('INFO')
        _log.setpath(path1)

        id_ruta = request.POST['id_ruta']
        id_tecnico = request.POST['id_tecnico']
        cantidad = request.POST['cantidad']
        # print(id_ruta)
        laruta = None

        if id_ruta:

            # verifico si la ruta ya esta cargada para no hacer nada
            try:
                laruta = Ruta.objects.filter(pk=id_ruta)
                # print(laruta)
                # print('aca')
                OrdenesCargadas = OrdenDeTrabajo.objects.filter(ruta=laruta, estado=7).count()
                if not laruta[0].estado == 3 or OrdenesCargadas > 0:
                    return HttpResponse(status=301)
                else:
                    # print('paso')
                    tecnico = Tecnico.objects.get(codigo=id_tecnico)
                    terminal_portatil = TerminalPortatil.objects.get(pk=tecnico.terminal_portatil.numero_serie)
                    cantidad_asignada = terminal_portatil.cantidad_asignada - int(cantidad)
                    terminal_portatil.cantidad_asignada = cantidad_asignada

                    if cantidad_asignada > 0:
                        terminal_portatil.estado_asignada = '1'
                        # print('llega')
                    else:
                        terminal_portatil.estado_asignada = '0'
                    terminal_portatil.save()
                    # print('llega')

                    laruta.update(tecnico=None, usuario_asignacion=None,
                                  fecha_hora_asignacion=None,
                                  estado=1, flag_asignacion_guardada='0')

                    ordenesLect = OrdenDeTrabajo.objects.filter(ruta=laruta, estado=3)
                    # print('aca')
                    ordenesLect.update(tecnico=None, usuario_asignacion=None,
                                       fecha_hora_asignacion=None,
                                       estado=1, flag_asignacion_guardada='0')

                    log_rutas.objects.create(estado='Asignación', fecha_log=datetime.now(),
                                             observacion='Se desasignó la ruta al tecnico: ' + str(
                                                 tecnico.nombre_1) + ',' + str(tecnico.apellido_1), ruta_id=id_ruta,
                                             usuario=request.user)
                    writeAudit("asignación rutas", "desasignar", request.user,
                               " La ruta {} fué desasignada".format(laruta))

                    return HttpResponse('Ruta desasignada', status=200)
            except Exception as e:
                _log.Writelog_N("Ocurrió el siguiente error en la asignación de órdenes: {}".format(e))
                log.error("Error {}".format(e))
                return HttpResponse(str(e), status=500)
    except Exception as e:

        # print("Error {}".format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def asignar_route(request):
    # print('entra asignar route')
    _log=Logger()
    _parametro=Parametro.objects.get(pk='P_QW_PATH_LOGS')
    path=_parametro.valor_1
    _log.logsetlevel('INFO')
    _log.setpath(path)

    context = RequestContext(request)
    if request.method == 'POST':
        try:
            ids_rutas = eval(request.POST['ids_rutas'])
            id_tecnico = eval(request.POST['id_tecnico'])
            # print(ids_rutas)
            # print("Tecnico " + str(id_tecnico))
            try:
                tecnico = Tecnico.objects.get(pk=id_tecnico)
            except:
                return HttpResponse(status=300)

            if len(ids_rutas) < 1:
                return HttpResponse(status=303)

            # agrego el estado a las rutas, para evitar que re asignen una ruta ya asignada
            # por tener la página abierta y ver la ruta pendiente.
            rutas = Ruta.objects.filter(pk__in=ids_rutas, estado__in=STATUS_ENABLED).values('idruta')
            if len(rutas) > 0:

                # Comprobación para saber si el técnico ya tiene algún segmento asignado con ordenes de rutas que se quieren asignar

                rutas_asignadas = set(rutas.values_list('idruta', flat=True))

                ordenes_tecnico = OrdenDeTrabajo.objects.filter(tecnico=tecnico, estado__in=[3,7],punto_suministro__segmentosum__isnull=False)

                if len(ordenes_tecnico) > 0:
                    
                    rutas_ordenes_tecnico = set(ordenes_tecnico.values_list('ruta', flat=True).distinct())

                    if rutas_asignadas.intersection(rutas_ordenes_tecnico):
                        mensaje = 'Esta/s ruta/s no se puede/n asignar ya que el técnico tiene segmentos con ordenes de la/s ruta/s asignada/s'
                        return HttpResponse(mensaje, status=301)

                # Fin de la comprobación

                for ruta in rutas:
                    log_rutas.objects.create(estado='Asignación', fecha_log=datetime.now(),
                                             observacion='Se asignó al tecnico: ' + str(tecnico.nombre_1) + ',' + str(
                                                 tecnico.apellido_1), ruta_id=ruta['idruta'], usuario=request.user)

                ordenesLect = OrdenDeTrabajo.objects.filter(estado__in=STATUS_ENABLED,ruta__in=rutas,punto_suministro__segmentosum__isnull=True).values(
                    'numero_orden')

                ordenesLect.update(tecnico=tecnico, usuario_asignacion=request.user,
                                   fecha_hora_asignacion=now().strftime("%Y%m%d%H%M%S"),
                                   estado=3, flag_asignacion_guardada='0')

                cant_ordenes = OrdenDeTrabajo.objects.filter(estado=3,
                                                             tecnico=tecnico,
                                                             usuario_asignacion=request.user).values(
                    'numero_orden').count()

                rutas.update(tecnico=tecnico, usuario_asignacion=request.user,
                             fecha_hora_asignacion=now().strftime("%Y%m%d%H%M%S"),
                             estado=3, flag_asignacion_guardada='0')

                terminal_portatil = TerminalPortatil.objects.get(pk=tecnico.terminal_portatil.numero_serie)
                terminal_portatil.cantidad_asignada = cant_ordenes
                terminal_portatil.estado_asignada = '1'
                terminal_portatil.save()

                writeAudit("asignación rutas", "asignar", request.user,
                           " Rutas {} asignadas al técnico {}".format(rutas, tecnico))

                mensaje = 'Se asignó {} itinerario con éxito. Hay {} ' \
                          'ordenes asignadas al técnico.'.format(len(ids_rutas), cant_ordenes)

                if len(ids_rutas) > 1:
                    mensaje = 'Se asignaron {} itinerarios con éxito. Hay {} ' \
                              'ordenes asignadas al técnico.'.format(len(ids_rutas), cant_ordenes)

                return HttpResponse(mensaje, status=200)

            else:
                mensaje = 'Las rutas seleccionadas no se encuentran disponible para asignar'
                return HttpResponse(mensaje, status=301)

        except Exception as e:
            _log.Writelog_N("Ocurrió el siguiente error en la asignación de órdenes: {}".format(e))
            log.error("Error {}".format(e))
            return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def guardar_asignar_ordenes(request):
    context = RequestContext(request)

    _log=Logger()
    _parametro=Parametro.objects.get(pk='P_QW_PATH_LOGS')
    path=_parametro.valor_1
    path1=path
    _log.logsetlevel('INFO')
    _log.setpath(path1)

    if request.method == 'POST':

        try:

            ordenes = OrdenDeTrabajo.objects.filter(
                estado=3,
                usuario_asignacion=request.user,
                flag_asignacion_guardada=0,
            ).exclude(punto_suministro__segmentosum_id__gt=0)

            # cantidad = ordenes.count()
            # print("ordenes.count() = " + str( cantidad ))

            cantidad = ordenes.update(flag_asignacion_guardada=1)

            rutas = Ruta.objects.filter(estado=3, usuario_asignacion=request.user, flag_asignacion_guardada=0)
            # print(str(rutas.query))

            for ruta in rutas:
                log_rutas.objects.create(estado='Asignación', fecha_log=datetime.now(),
                                         observacion='Se guardó la asignación de  la ruta', ruta_id=ruta.idruta,
                                         usuario=request.user)

            rutas.update(flag_asignacion_guardada=1)

            writeAudit("asignación rutas", "asignar", request.user,
                       "Asignación guardada para las rutas {} ".format(rutas))

            if (cantidad > 0):

                return HttpResponse('{}'.format(cantidad), status=200)

            else:

                return HttpResponse(status=301)

        except Exception as e:

            _log.Writelog_N("Ocurrió el siguiente error en la asignación de órdenes: {}".format(e))

            log.error("Error {}".format(e))

            return HttpResponse(status=300)

    return HttpResponse(status=500)


###### ----------------- ASIGNACION  SEGMENTACIÓN POR RUTAS------------------------- ######
@login_required(login_url=settings.LOGIN_PAGE)
def asignar_segmento(request):
    # print('entra asignar segmento')
    _log=Logger()
    _parametro=Parametro.objects.get(pk='P_QW_PATH_LOGS')
    path=_parametro.valor_1
    _log.logsetlevel('INFO')
    _log.setpath(path)

    if request.method == 'POST':
        # try:
        ids_segmentos = eval(request.POST['ids_segmentos'])
        id_tecnico = eval(request.POST['id_tecnico'])
        id_centro = request.POST['id_centro']
        id_semana=request.POST['id_semana']
            
        try:
            tecnico = Tecnico.objects.get(pk=id_tecnico)
        except:
            return HttpResponse(status=300)

        if len(ids_segmentos) < 1:
            return HttpResponse(status=303)

    
        # Chequeo si se repiten rutas en los segmentos

        rutas_ordenes_segmentos = set()
        rutas_repetidas = set()

        for segmento in ids_segmentos:
            rutas_segmento = OrdenDeTrabajo.objects.filter(
                estado__in=[1, 33, 1024],
                ruta__anio=id_semana,
                ruta__oficina=id_centro,
                usuario_asignacion=None,
                punto_suministro__segmentosum_id=segmento
            ).exclude(flag_asignacion_guardada=1)\
            .values_list('ruta', flat=True).distinct()

            for ruta in rutas_segmento:
                if ruta in rutas_ordenes_segmentos:
                    rutas_repetidas.add(ruta)
                else:
                    rutas_ordenes_segmentos.add(ruta)

        if len(rutas_repetidas) > 0:

            mensaje = 'Los segmentos seleccionados no se pueden asignar porque se repiten rutas'
            return HttpResponse(mensaje, status=301)

        # Comprobación para saber si el técnico ya tiene otra ruta o segmento asignado con ordenes de rutas que se quieren asignar

        ordenes_tecnico = OrdenDeTrabajo.objects.filter(tecnico=tecnico, estado__in=[3,7])

        if len(ordenes_tecnico) > 0:
            
            rutas_ordenes = set(ordenes_tecnico.values_list('ruta', flat=True).distinct())

            if rutas_ordenes_segmentos.intersection(rutas_ordenes):
                mensaje = 'Este segmento no se puede asignar porque el técnico ya tiene ordenes de esa/s ruta/s asignadas'
                return HttpResponse(mensaje, status=301)

        # Fin de la comprobación

        ordenesSeg = OrdenDeTrabajo.objects.filter(
            estado__in=[1,33,1024],
            ruta__anio=id_semana,
            ruta__oficina=id_centro,
            usuario_asignacion=None,
            punto_suministro__segmentosum_id__in=ids_segmentos
        ).exclude(flag_asignacion_guardada=1)
        
        cantidad_asignada=ordenesSeg.count()

        ordenesSeg.update(
            tecnico=tecnico,
            usuario_asignacion=request.user,
            fecha_hora_asignacion=now().strftime("%Y%m%d%H%M%S"),
            estado=3,
            flag_asignacion_guardada=0)

        
        terminal_portatil = TerminalPortatil.objects.get(pk=tecnico.terminal_portatil.numero_serie)
        cant = 0 if not terminal_portatil.cantidad_asignada else terminal_portatil.cantidad_asignada
        terminal_portatil.cantidad_asignada = cant + cantidad_asignada
        terminal_portatil.estado_asignada = '1'
        terminal_portatil.save()

        # # writeAudit("asignación rutas", "asignar", request.user,
        # #             " Segmentos {} asignadas al técnico {}".format(rutas, tecnico))

        # mensaje = 'Se asignó {} itinerario con éxito. Hay {} ' \
        #             'ordenes asignadas al técnico.'.format(len(ids_ordenes), cant_ordenes)

        if len(ids_segmentos) > 0:
            mensaje = 'Se asignaron {} segmentos con éxito. y {} órdenes'.format(len(ids_segmentos),cantidad_asignada)

            return HttpResponse(mensaje, status=200)

        else:
            mensaje = 'Los segmentos seleccionadss no se encuentran disponibles para asignar'
            return HttpResponse(mensaje, status=301)

        # except Exception as e:
        #     log.error("Error {}".format(e))
        #     return HttpResponse(status=500)

@login_required(login_url=settings.LOGIN_PAGE)
def asignacion_desasignar_segmento(request):
    # print('entra asignar segmento')
    _log=Logger()
    _parametro=Parametro.objects.get(pk='P_QW_PATH_LOGS')
    path=_parametro.valor_1
    _log.logsetlevel('INFO')
    _log.setpath(path)

    if request.method == 'POST':
        # try:
        ids_orden = request.POST['id_segmento']
        id_tecnico = request.POST['id_tecnico']
        cantidad = request.POST['cantidad']
        
        try:
            tecnico = Tecnico.objects.get(pk=id_tecnico)
        except:
            return HttpResponse(status=300)

        if not ids_orden:
            return HttpResponse(status=303)

        ordenesSeg = OrdenDeTrabajo.objects.filter(
            estado__in=[3],
            punto_suministro__segmentosum_id=ids_orden
        ).exclude(flag_asignacion_guardada=1)
        
        # for _ in ordenesSeg:
        #     print(_)
        if ordenesSeg.count()<1:
            return HttpResponse(status=301)    
        
        ordenesSeg.update(
            tecnico=None,
            usuario_asignacion=None,
            fecha_hora_asignacion=None,
            estado=1,
            flag_asignacion_guardada=0
        )
        
        terminal_portatil = TerminalPortatil.objects.get(pk=tecnico.terminal_portatil.numero_serie)
        cantidad_asignada = terminal_portatil.cantidad_asignada - int(cantidad)
        terminal_portatil.cantidad_asignada = cantidad_asignada

        if cantidad_asignada > 0:
            terminal_portatil.estado_asignada = '1'
            # print('llega')
        else:
            terminal_portatil.estado_asignada = '0'
        terminal_portatil.save()


        # # writeAudit("asignación rutas", "asignar", request.user,
        # #             " Segmentos {} asignadas al técnico {}".format(rutas, tecnico))

        # mensaje = 'Se asignó {} itinerario con éxito. Hay {} ' \
        #             'ordenes asignadas al técnico.'.format(len(ids_ordenes), cant_ordenes)

        # if len(ids_ordenes) > 1:
        #     mensaje = 'Se asignaron {} itinerarios con éxito. Hay {} ' \
        #                 'ordenes asignadas al técnico.'.format(len(ids_ordenes), cant_ordenes)

        # return HttpResponse(mensaje, status=200)
        return HttpResponse('{}'.format(cantidad), status=200)

        # else:
        #     mensaje = 'Las rutas seleccionadas no se encuentran disponible para asignar'
        #     return HttpResponse(mensaje, status=301)

        # except Exception as e:
        #     log.error("Error {}".format(e))
        #     return HttpResponse(status=500)

@login_required(login_url=settings.LOGIN_PAGE)
def guardar_asignar_segmentos(request):
    _log=Logger()
    _parametro=Parametro.objects.get(pk='P_QW_PATH_LOGS')
    path=_parametro.valor_1
    path1=path
    _log.logsetlevel('INFO')
    _log.setpath(path1)

    if request.method == 'POST':

        try:

            ordenes = OrdenDeTrabajo.objects.filter(estado=3,
                                                    usuario_asignacion=request.user,
                                                    flag_asignacion_guardada=0,
                                                    punto_suministro__segmentosum_id__gt=0
                                                    )

            
            cantidad = ordenes.update(flag_asignacion_guardada=1)
            
            writeAudit("asignación segmentos", "asignar", request.user,
                       "Asignación guardada para las rutas {} ".format(ordenes))

            if (cantidad > 0):

                return HttpResponse('{}'.format(cantidad), status=200)

            else:

                return HttpResponse(status=301)

        except Exception as e:

            _log.Writelog_N("Ocurrió el siguiente error en la asignación de órdenes: {}".format(e))

            log.error("Error {}".format(e))

            return HttpResponse(status=300)

    return HttpResponse(status=500)

@login_required(login_url=settings.LOGIN_PAGE)
def segmentacion_rutas_main(request):
    try:
        context = RequestContext(request)
        context['tecnicos'] = []
        try:
            semana = SemanaXUser.objects.get(usuario=request.user)
            context['semana'] = semana
            
        except:
            pass
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)
    
    return render_to_response('ordenes/asignacion_segmentos/_asignacion_segmentos.html', context)

@login_required(login_url=settings.LOGIN_PAGE)
def obtener_rutas_segmentos(request):
    try:
        context = RequestContext(request)
        oficina = request.POST['id_oficina']
        semanas = request.POST['num_semana']
        segmentos=segmentos.objects.filter(oficina_id=oficina)
        if semana == 'TODAS' or semana == '':
            rutas = Ruta.objects.filter(oficina=oficina,estado__in=[1,33,1025])
        else:
            rutas = Ruta.objects.filter(oficina=oficina, anio=semanas,estado__in=[1,33,1025])
        context['ruta'] = rutas
        context['segmentos'] = segmentos
        return render_to_response('ordenes/asignacion_segmentos/_table_routes.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)
    
@login_required(login_url=settings.LOGIN_PAGE)
def asignacion_segmento_route(request):
    try:

        context = RequestContext(request)
        id_centro = request.POST['id_oficina']
        _result = []
        semana = request.POST['semana']
        
        if id_centro:
            centro = WorkUnit.objects.get(pk=id_centro)
            if semana == 'TODAS' or semana == '':
                # rutas = Ruta.objects.filter(oficina=centro,estado__in=STATUS_ENABLED)
                rutas = OrdenDeTrabajo.objects.filter(ruta__oficina=centro, ruta__estado__in=[1,33,1025],
                                                      punto_suministro__segmentosum_id=None).values(
                                                            'ruta__idruta',
                                                            'ruta__oficina',
                                                            'ruta__ciclo', 'ruta__ruta',
                                                            'ruta__itinerario', 'ruta__anio',
                                                            'ruta__fecha_estimada_resolucion',
                                                            'ruta__cantidad',
                                                            'ruta__cantidad_leido').exclude(
                                                        punto_suministro__gps_latitud='0', 
                                                        punto_suministro__gps_longitud='0').distinct()
            else:
                
                rutas = OrdenDeTrabajo.objects.filter(ruta__oficina=centro, ruta__anio=semana, 
                                                      ruta__estado__in=[1,33,1025],
                                                      punto_suministro__segmentosum_id=None).values(
                                                            'ruta__idruta',
                                                            'ruta__oficina',
                                                            'ruta__ciclo',
                                                            'ruta__ruta',
                                                            'ruta__itinerario',
                                                            'ruta__anio',
                                                            'ruta__fecha_estimada_resolucion',
                                                            'ruta__cantidad',
                                                            'ruta__cantidad_leido').distinct()
                # rutas = Ruta.objects.filter(oficina=centro,anio=semana, estado__in=STATUS_ENABLED)
            for ruta in rutas:
                _result.append({'idruta': ruta['ruta__idruta'],
                                'oficina': ruta['ruta__oficina'],
                                'ciclo': ruta['ruta__ciclo'],
                                'ruta': ruta['ruta__ruta'],
                                'itinerario': ruta['ruta__itinerario'],
                                'anio': ruta['ruta__anio'],
                                'fecha_estimada_resolucion': ruta['ruta__fecha_estimada_resolucion'],
                                'cantidad': ruta['ruta__cantidad'],
                                'cantidad_leido': str(int(ruta['ruta__cantidad']) - int(ruta['ruta__cantidad_leido'])),
                                })
                
            
            
            # context['rutas'] = _result
            context={'rutas':_result}
            
            # context['segmentos'] = _segmentos
        return render_to_response('ordenes/asignacion_segmentos/_table_routes.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)

@login_required(login_url=settings.LOGIN_PAGE)
def segmentacion_rutas_coordenadas(request):
    try:
        
        _ruta_id=request.POST['ruta_id']
        
        coordenada = OrdenDeTrabajo.objects.filter(
            ruta_id=_ruta_id,
            punto_suministro__segmentosum_id = None,
            estado__in=[1, 33, 1025]
        ).select_related(
            'punto_suministro'
        ).exclude(
            punto_suministro__gps_latitud='0',
            punto_suministro__gps_longitud='0',
        ).values(
            'ruta_id',
            'punto_suministro_id',
            'punto_suministro__gps_latitud',
            'punto_suministro__gps_longitud'
        )
        
        print("cantidad de puntos: " + str(coordenada.count()))
        if coordenada:
            contexto={'coordenada':list(coordenada)}
            return JsonResponse(contexto,safe=False)
        else:
            return HttpResponse(status=301)

    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)

@login_required(login_url=settings.LOGIN_PAGE)
def segmentacion_save(request):
    try:
        context = RequestContext(request)
        oficina = request.POST['id_oficina']
        cod_segmento = request.POST['cod_seg']
        desc_segmento = request.POST['desc_seg']
        
        if SegmentoSum.objects.filter(codigo_segmento=cod_segmento).exists():
            return HttpResponse(status=300)
        
        objsegmento=SegmentoSum.objects.create(
            oficina_id=oficina,
            codigo_segmento=cod_segmento,
            descripcion_segmento=desc_segmento)
        objsegmento.save()
        context={'id_seg':objsegmento.id,'cod_seg':cod_segmento,'desc_seg':desc_segmento}
        
        return JsonResponse(context,safe=False)
        
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)

@login_required(login_url=settings.LOGIN_PAGE)
def segmentacion_asignacion_save(request):
    try:
        _lst_data_asignaciones = json.loads(request.POST['datos_asign'])

        #Registra el Geojson en la tabla Areas
        for lst_area in _lst_data_asignaciones:
            areas_objects=lst_area['areas']
            for area in areas_objects:
                Segmento_Areas.objects.create(area =area,segmentosum_id=lst_area['idsegmento'])
        
        
        _puntos_suministros=[]
        
        for lst in _lst_data_asignaciones:
            
            puntos_objects = lst.get('areas', [])
            _idseg=lst['idsegmento']
            for areas in puntos_objects:       
                    
                if isinstance(areas, str):
    
                    areas = json.loads(areas)
                
                if isinstance(areas, dict):
                    
                    features = areas.get('features', [])
                    
                    for feature in features:
                        
                        if isinstance(feature, dict):
                            properties = feature.get('properties', {})
                            _markers_list = properties.get('markers', [])
                            for markers_group in _markers_list:
                                for marker in markers_group:
                                    if isinstance(marker, dict):
                                        # Ahora puedes acceder a las propiedades de cada marcador individual
                                        id_pumsum = marker.get('id_pumsum')
                                        # latitud = marker.get('latitud')
                                        # longitud = marker.get('longitud')
                                        _puntos_suministros.append({'id_pumsum':id_pumsum,'id_segmento':_idseg})

        
        #Actualiza el campo sementosum_id de table punto_suministro
        for lst_punsum in _puntos_suministros:
            ps=PuntoDeSuministro.objects.get(punto_suministro=int(lst_punsum['id_pumsum']))
            ps.segmentosum_id=int(lst_punsum['id_segmento'])
            ps.save()
                
        return HttpResponse(status=200)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)
    
@login_required(login_url=settings.LOGIN_PAGE)
def asignacion_segmento_area_delete(request):
    try:
        _id_area=request.POST['id_area']
        area_eliminar=Segmento_Areas.objects.get(id=_id_area)#obtenemos el geojson texto
        geojson=json.loads(area_eliminar.area)#convertimos texto a json
        features = geojson['features']#obtenemos el atributo features

        contexto=""
        # Iterar sobre las features
        for feature in features:
            # Acceder a la propiedad 'markers' dentro de 'properties'
            markers = feature['properties']['markers'][0]    
            contexto=markers
            # Iterar sobre los markers para actualizar la tabla PuntoDeSuministro
            for marker in markers:
                id_pumsum = marker['id_pumsum']
                # latitud = marker['latitud']
                # longitud = marker['longitud']
                
                puntos_suministros=PuntoDeSuministro.objects.get(punto_suministro=id_pumsum)
                puntos_suministros.segmentosum_id=None
                puntos_suministros.save()
                
        area_eliminar.delete()##Cuando termina el proceso recien puede eliminar el area
        
        return JsonResponse(contexto,safe=False)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)

@login_required(login_url=settings.LOGIN_PAGE)
def segmentacion_segmentos_show(request):
    try:
        context = RequestContext(request)
        _id_oficina=request.POST['id_oficina']
        semana = request.POST['semana']
        
        segmentos_asignados = list(OrdenDeTrabajo.objects.filter(
                estado__in=[3, 7, 9, 17, 65, 265, 273, 401, 777, 785, 1025, 2049],
                ruta__anio=semana,
                ruta__oficina=_id_oficina,
                usuario_asignacion=request.user,
                punto_suministro__segmentosum_id__gt=0
            ).select_related(
                'punto_suministro__segmentosum_id',
                'ruta'
            ).values_list(
                'punto_suministro__segmentosum_id',
                flat=True 
            ).distinct())
        
        _segmentos=list(SegmentoSum.objects.filter(oficina_id=_id_oficina)\
            .exclude(id__in = segmentos_asignados).values())
        context={'segmentos':_segmentos}
        return JsonResponse(context,safe=False)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)

@login_required(login_url=settings.LOGIN_PAGE)
def segmentacion_areas_show(request):
    try:
        context = RequestContext(request)
        _id_segmento=request.POST['id_segmento']
        _segmentos_areas=list(Segmento_Areas.objects.filter(segmentosum_id=_id_segmento).values())
        _marcadores_coordenadas=list(PuntoDeSuministro.objects.filter(segmentosum_id=_id_segmento).values('punto_suministro','gps_latitud','gps_longitud'))
        context={'segmentos_areas':_segmentos_areas,
                 'marcadores_coordenadas':_marcadores_coordenadas}
        return JsonResponse(context,safe=False)

    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)

@login_required(login_url=settings.LOGIN_PAGE)
def segmentacion_segmentos_edit(request):
    try:
        _id_segmento=request.POST['id_segmento']
        segmento=SegmentoSum.objects.get(id=_id_segmento)
        contexto={'cod_segmento':segmento.codigo_segmento,
                'desc_descripcion':segmento.descripcion_segmento}
        return JsonResponse(contexto,safe=False)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)
    

@login_required(login_url=settings.LOGIN_PAGE)
def segmentacion_segmentos_delete(request):
    try:
        _id_segmento=request.POST['id_segmento']
        asignada =OrdenDeTrabajo.objects.filter(
            punto_suministro__segmentosum_id=_id_segmento,
            estado=3
        )
        
        if asignada:
            return HttpResponse(status=301)#Segmento no se puede asignar    
        
        Segmento_Areas.objects.filter(segmentosum_id=_id_segmento).delete()        
        PuntoDeSuministro.objects.filter(segmentosum_id=_id_segmento).update(segmentosum_id=None)
        SegmentoSum.objects.get(id=_id_segmento).delete()
  
        return HttpResponse(status=200)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)

    
@login_required(login_url=settings.LOGIN_PAGE)
def segmentacion_segmentos_update(request):
    try:
        _id_segmento = request.POST['_id_segmento']
        cod_segmento = request.POST['cod_seg']
        desc_segmento = request.POST['desc_seg']
        segmento=SegmentoSum.objects.get(id=_id_segmento)
        segmento.codigo_segmento=cod_segmento
        segmento.descripcion_segmento=desc_segmento
        segmento.save()
        contexto={'id_segmento':segmento.id}
        return JsonResponse(contexto,safe=False,status=200)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)
    
@login_required(login_url=settings.LOGIN_PAGE)
def segmentacion_asignacion_update(request):
    try:
        _lst_puntossum = json.loads(request.POST['lst_puntossum'])
        _geojson_areas = request.POST['geojson_areas']
        _id_segmento_sum = request.POST['id_segmento_sum']

        sa=Segmento_Areas.objects.filter(segmentosum_id=_id_segmento_sum)
        sa.update(area=_geojson_areas)
        
        for punto_sum in _lst_puntossum:
            ps=PuntoDeSuministro.objects.get(punto_suministro=punto_sum['id_pumsum'])
            ps.update(segmentosum_id=_id_segmento_sum)
            # ps.save()
        return HttpResponse(status=200)
    except Exception as e:
            log.error("Error {}".format(e))
            return HttpResponse(status=500)

####  -------------------TERMINA SEGMENTOS  ---------------------- #######

###### ------------- ASIGNACION  SEGMENTACIÓN PUNTOS SIN COORDENADAS (LISTA)----------- ######
@login_required(login_url=settings.LOGIN_PAGE)
def asignacion_table_puntos_sincoord(request):
    try:

        context = RequestContext(request)
        id_centro = request.POST['id_oficina']
        
        semana = request.POST['semana']
        
        filtro_rutas = request.POST['rutas']
        
        lista_rutas = filtro_rutas.split(',')
        
        if id_centro:
            centro = WorkUnit.objects.get(pk=id_centro)
            if semana == 'TODAS' or semana == '':
                rutas= OrdenDeTrabajo.objects.filter(
                    ruta__oficina=centro,
                    punto_suministro__gps_latitud='0',                    
                    punto_suministro__gps_longitud='0',
                    ruta__estado__in=[1,33,1025],
                    ruta_id__in=lista_rutas
                    ).prefetch_related(
                        'punto_suministro',
                    ).values(
                        'punto_suministro_id',
                        'punto_suministro__gps_latitud',
                        'punto_suministro__gps_longitud',
                        'punto_suministro__calle',
                        'punto_suministro__numero_puerta',
                        'ruta__idruta'
                    )
            else:
                rutas= OrdenDeTrabajo.objects.filter(
                    ruta__anio=semana,
                    ruta__oficina=centro,
                    punto_suministro__gps_latitud='0',
                    punto_suministro__gps_longitud='0',
                    ruta__estado__in=[1,33,1025],
                    ruta_id__in=lista_rutas
                ).prefetch_related(
                    'punto_suministro',
                ).values(
                    'punto_suministro_id',
                    'punto_suministro__gps_latitud', 
                    'punto_suministro__gps_longitud',
                    'punto_suministro__calle',
                    'punto_suministro__numero_puerta',
                    'ruta__idruta'
                ).distinct()
                    
        context={'puntossum_sincoor':list(rutas)}
        
        cantidad_sin_coordenadas = rutas.count()
        
        if cantidad_sin_coordenadas > settings.MAX_POINTS_IN_MAP:
            return HttpResponse(status=304)
            
        return render_to_response('ordenes/asignacion_segmentos/_table_suministros_sincoord.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)

@login_required(login_url=settings.LOGIN_PAGE)
def asignacion_ubicacion_save(request):
    try:
        _id_punto_suministro=request.POST['id_punto_suministro']
        _gps_lat = request.POST['gps_lat']
        _gps_lng = request.POST['gps_lng']
        _gps_lat = round(float(_gps_lat), 10)
        _gps_lng = round(float(_gps_lng), 10)

        ps=PuntoDeSuministro.objects.get(punto_suministro=_id_punto_suministro)
        ps.gps_latitud=str(_gps_lat)
        ps.gps_longitud=str(_gps_lng)
        ps.save()
        return HttpResponse(status=200)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)
    
####-----------------------TERMINA SEGMENTOS SINCOORDENADAS------------------#########




####-----------------------ASIGNACION SEGMENTOS--------------------#########333
@login_required(login_url=settings.LOGIN_PAGE)
def asignacion_tech_seg(request):
    try:

        context = RequestContext(request)
        id_centro = request.POST['id_oficina']
        # print(id_centro)
        if id_centro:
            # centro = WorkUnit.objects.get(pk=id_centro)
            tecnicos_oficina = OficinaXTecnico.objects.filter(oficina=id_centro, fecha_baja=None)
            tecs = []
            for item in tecnicos_oficina:
                tecs.append(item.tecnico.codigo)
                # print('tecs {}'.format(tecs))
            tecnicos = Tecnico.objects.filter(codigo__in=tecs, terminal_portatil__isnull=False)
            # print(len(tecnicos))
            context['tecnicos'] = tecnicos
            # print(tecnicos)

        return render_to_response('ordenes/asignacion/segmentos/_table_techs_seg.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)

from django.db import connection

@login_required(login_url=settings.LOGIN_PAGE)
def asignacion_segmento_table(request):
    try:
        context = RequestContext(request)
        id_centro = request.POST['id_oficina']
        id_semana = request.POST['semana']
        
        segmentos = (
            OrdenDeTrabajo.objects.filter(
                ruta__anio=id_semana,
                ruta__oficina=id_centro,
                punto_suministro__segmentosum_id__isnull=False,
            )
            .exclude(flag_asignacion_guardada=1)
            .values(
                'punto_suministro__segmentosum_id',
                'punto_suministro__segmentosum_id__codigo_segmento',
                'punto_suministro__segmentosum_id__descripcion_segmento',
                'ruta__fecha_estimada_resolucion',
            )
            .annotate(
                cantidad=Count('numero_orden'),
                pendiente=Count(Case(
                    When(
                        usuario_asignacion=None,
                        estado__in=[1, 33, 1025],
                        then=1
                    ),
                    output_field=IntegerField(),
                ))
            ).filter(pendiente__gt=0)
        )
        
        context['segmentos']=segmentos
        
        return render_to_response('ordenes/asignacion/segmentos/_table_seg.html', context)
    
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)
    


@login_required(login_url=settings.LOGIN_PAGE)
def asignacion_asignaciones_seg(request):
    try:

        context = RequestContext(request)
        id_centro = request.POST['id_oficina']
        id_semana = request.POST['id_semana']
        valuecheckSeg = request.POST['valuecheckSeg']

        if id_centro:      
            
            exclude_flag_asignacion= 1 if valuecheckSeg == '0' else 0
            
            segmentos = OrdenDeTrabajo.objects.filter(
                estado=3,
                ruta__anio=id_semana,
                ruta__oficina=id_centro,
                usuario_asignacion=request.user,
                punto_suministro__segmentosum_id__gt=0
            ).select_related(
                'punto_suministro__segmentosum_id',
                'ruta'
            ).exclude(flag_asignacion_guardada=exclude_flag_asignacion).values(
                'ruta__oficina',
                'ruta__oficina__name',
                'punto_suministro__segmentosum_id__codigo_segmento',
                'punto_suministro__segmentosum_id__descripcion_segmento',
                'ruta__anio',
                'tecnico__codigo',
                'usuario_asignacion__username',
                'ruta__fecha_estimada_resolucion',
                'punto_suministro__segmentosum_id',
            ).annotate(cantidad=Count('punto_suministro__segmentosum_id')).distinct()


            context['segmentos_asignados'] = segmentos
        
        return render_to_response('ordenes/asignacion/segmentos/_table_asignados_seg.html', context)

    except Exception as e:
        log.error("Error {}".format(e))



###### ------------------------- REORGANIZACION  ------------------------- ######
@login_required(login_url=settings.LOGIN_PAGE)
def reorganizacion_main(request):
    try:
        context = RequestContext(request)
        context['rutas'] = []
        context['center'] = "d3"
        return render_to_response('ordenes/reorganizacion/_reorganizacion.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@csrf_exempt
@login_required(login_url=settings.LOGIN_PAGE)
def reorganizacion_list(request):
    try:
        # print('entra reorganizar list')
        context = RequestContext(request)
        id_centro = request.POST['id_oficina']
        solicitar = request.POST['solicitar']
        if id_centro:
            centro = WorkUnit.objects.get(pk=id_centro)
            if solicitar == '3':
                reorganizar = Reorganizar.objects.filter(fecha_denegado__isnull=False, oficina=centro,
                                                         fecha_solicitud__isnull=False, fecha_autorizado__isnull=True,
                                                         usuario__isnull=False)
                context['ruta'] = reorganizar
                return render_to_response('ordenes/reorganizacion/_table_routes.html', context)
            elif solicitar == '2':
                reorganizar = Reorganizar.objects.filter(oficina=centro, fecha_solicitud__isnull=False,
                                                         fecha_autorizado__isnull=False, usuario__isnull=False,
                                                         fecha_denegado__isnull=True)
                context['ruta'] = reorganizar
                return render_to_response('ordenes/reorganizacion/_table_routes.html', context)
            else:
                reorganizar = Reorganizar.objects.filter(oficina=centro, fecha_autorizado__isnull=True,
                                                         fecha_denegado__isnull=True, usuario__isnull=True)
                context['ruta'] = reorganizar
                return render_to_response('ordenes/reorganizacion/_table_routes.html', context)
        context['ruta'] = reorganizar
        return render_to_response('ordenes/reorganizacion/_table_routes.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@csrf_exempt
@login_required(login_url=settings.LOGIN_PAGE)
def autorizar(request):
    try:
        # print('entra autorizar')
        context = RequestContext(request)
        lista = []
        lista1 = []
        id_centro = request.POST['oficina']
        solicitar = request.POST['solicitud']
        rutas = request.POST['rutas']
        if solicitar == '1':
            rutas = rutas.replace('[', '').replace(']', '').rstrip(',').split(',')
            for i in rutas:
                lista = i.split('|')
                valor = lista[0]
                ruta = Ruta.objects.get(idruta=valor)
                cant_lect = OrdenDeTrabajo.objects.filter(ruta=ruta, estado__gt=7).count()
                # print(cant_lect)
                if ruta.cantidad == ruta.cantidad_leido or cant_lect == ruta.cantidad:
                    reorganizar = Reorganizar.objects.get(ruta=valor)
                    reorganizar.usuario = request.user
                    reorganizar.fecha_autorizado = datetime.now()
                    reorganizar.save()
                else:
                    return HttpResponse(status=500)
                rutasuministro = RutaSum.objects.get(idrutasum=ruta.rutasum_id)
                # print(rutasuministro)
                # print('llega')
                ptosuministro = PuntoDeSuministro.objects.filter(rutasum=rutasuministro.idrutasum)
                for p in ptosuministro:
                    suministro = PuntoDeSuministro.objects.get(punto_suministro=p.punto_suministro)
                    # print(suministro)
                    if suministro.rutasum == rutasuministro:
                        # print('aca')
                        suministro.secuencia_anterior = suministro.secuencia_teorica
                        suministro.fecha_actualizacion_secuencia = datetime.now()
                        ordtrabajo = OrdenDeTrabajo.objects.get(punto_suministro=suministro, ruta=ruta)
                        desc_ord = Desc_Orden.objects.get(orden_trabajo=ordtrabajo)
                        if desc_ord.id_descarga == 'FORZADO':
                            suministro.secuencia_teorica = desc_ord.secuencia_real
                            suministro.save()
                        else:
                            # print('llega aca')
                            suministro.secuencia_teorica = int(desc_ord.secuencia_real) * 1
                            suministro.save()
                log_rutas.objects.create(estado='Reorganización', fecha_log=datetime.now(),
                                         observacion='Se autorizó la reorganización de la ruta', ruta_id=ruta.idruta,
                                         usuario=request.user)
        rutas = Reorganizar.objects.filter(oficina=id_centro, fecha_autorizado__isnull=True,
                                           fecha_denegado__isnull=True,
                                           usuario__isnull=True)
        context['ruta'] = rutas
        return render_to_response('ordenes/reorganizacion/_table_routes.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@csrf_exempt
@login_required(login_url=settings.LOGIN_PAGE)
def denegar(request):
    try:
        context = RequestContext(request)
        lista = []
        id_centro = request.POST['oficina']
        solicitar = request.POST['solicitud']
        rutas = request.POST['rutas']
        if solicitar == '1':
            rutas = rutas.replace('[', '').replace(']', '').rstrip(',').split(',')
            for i in rutas:
                lista = i.split('|')
                valor = lista[0]
                ruta = Ruta.objects.get(idruta=valor)
                reorganizar = Reorganizar.objects.get(ruta=valor)
                reorganizar.usuario = request.user
                reorganizar.fecha_denegado = datetime.now()
                reorganizar.save()
                log_rutas.objects.create(estado='Reorganización', fecha_log=datetime.now(),
                                         observacion='Se denego la reorganización de la ruta', ruta_id=ruta.idruta,
                                         usuario=request.user)
        rutas = Reorganizar.objects.filter(fecha_autorizado__isnull=True, fecha_denegado__isnull=True,
                                           usuario__isnull=True)
        context['ruta'] = rutas
        return render_to_response('ordenes/reorganizacion/_table_routes.html', context)

    except Exception as e:
        log.error("Error {}".format(e))


@csrf_exempt
@login_required(login_url=settings.LOGIN_PAGE)
def posicionmapa(request):
    try:
        # print('llega a mapa')
        context = RequestContext(request)
        posiciones = []
        lista = []
        id_centro = request.POST['oficina']
        solicitar = request.POST['solicitud']
        rutas = request.POST['rutas']
        # print(id_centro)
        # print(solicitar)
        # print(rutas)
        oficina = WorkUnit.objects.get(id_workunit=id_centro)
        rutas = rutas.replace('[', '').replace(']', '').rstrip(',').split(',')
        for i in rutas:
            posiciones = []
            lista = i.split('|')
            valor = lista[0]
            ruta = Ruta.objects.get(idruta=valor)
            # print('aca')
            # print(ruta.cantidad)
            # print(ruta.cantidad_leido)
            if ruta.cantidad == ruta.cantidad_leido:
                # print(ruta)
                ordtrabajo = OrdenDeTrabajo.objects.filter(ruta=ruta)

                # print(ordtrabajo)
                for o in ordtrabajo:
                    desc_ord = Desc_Orden.objects.get(orden_trabajo=o.numero_orden)
                    # print('desc {}'.format(desc_ord))
                    posiciones.append({'latitud': desc_ord.gps_latitud, 'longitud': desc_ord.gps_longitud,
                                       'secuencia': desc_ord.secuencia_real})
                rutas = []
                # print(posiciones)
                context['posiciones'] = posiciones
                context['center'] = oficina.coords

                return render_to_response('ordenes/reorganizacion/_mapa.html', context)
            else:
                return HttpResponse(status=500)
    except Exception as e:
        log.error("Error {}".format(e))


def export_reorganizar(request):
    try:
        # print('entra autorizar')
        context = RequestContext(request)
        lista = []
        lista1 = []
        strsec = ''
        strsecuencia = ''
        DataList = []
        archivo = ''
        id_centro = request.POST['oficina']
        solicitar = request.POST['solicitud']
        rutas = request.POST['rutas']

        paramexport = ConfigParamsImpExp.objects.get(oficina=id_centro)
        ruta = paramexport.path_txt_export

        if solicitar == '2':
            rutas = rutas.replace('[', '').replace(']', '').rstrip(',').split(',')
            for i in rutas:
                lista = i.split('|')
                valor = lista[0]
                ruta = Ruta.objects.get(idruta=valor)
                cant_lect = OrdenDeTrabajo.objects.filter(ruta=ruta, estado=777).order_by('secuencia_teorica')
                for o in cant_lect:
                    desc_ord = Desc_Orden.objects.get(orden_trabajo=o.orden_trabajo).order_by('secuencia_real')

                    strsec = str(o.punto_suministro.aparato.num_serie) + ';' + str(o.secuencia_teorica) + ';' + str(
                        desc_ord.secuencia_real)

                    strsecuencia = strsecuencia + strsec + '\n'

                _Name = ruta.ruta.getfilename()
                pathruta = ruta + '/'
                if os.path.exists(pathruta):
                    archivo = open(pathruta + _Name, 'r')
                    DataList = archivo.readlines()
                    # print(DataList)
                    # print('entra if')
                    DataList = ''.join(DataList)
                    reescribir.append(DataList + strsecuencia)
                    escribir = ''.join(reescribir)
                    archivo = open(pathruta + _Name, 'w')
                    archivo.write(escribir)
                    # print(escribir)
                    archivo.close()
                else:
                    if not os.path.exists(pathruta):
                        os.makedirs(pathruta)
                    archivo = open(pathruta + _Name, 'w')
                    archivo.write(strsecuencia)
                    archivo.close()

        context['rutas'] = []
        context['center'] = "d3"

        return render_to_response('ordenes/reorganizacion/_reorganizacion.html', context)
    except Exception as e:

        log.error("Error {}".format(e))
        return HttpResponse(status=500)


###### ------------------------- CONSULTA  ------------------------- ######
@login_required(login_url=settings.LOGIN_PAGE)
def consulta_main(request):
    try:
        context = RequestContext(request)
        context['tecnicos'] = []
        activa_revision = ''
        try:
            activa_revision = Parametro.objects.get(parametro='P_ACTIVA_REVISION')
            if activa_revision.valor_1 == '0':
                activa_revision = ''
            else:
                activa_revision = '1'
        except:
            print('No tiene revision activa')
        # print(activa_revision)
        context['activa_revision'] = activa_revision
        try:
            semana = SemanaXUser.objects.get(usuario=request.user)
            context['semana'] = semana
        except:
            pass
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)

    return render_to_response('ordenes/consulta/_consulta.html', context)


@csrf_exempt
def consulta_route(request):
    try:

        context = RequestContext(request)
        id_centro = request.POST['id_oficina']
        semana = request.POST['semana']
        # print(id_centro)
        if id_centro:
            centro = WorkUnit.objects.get(pk=id_centro)
            if semana == 'TODAS' or semana == '':
                rutas = Ruta.objects.filter(oficina=centro, estado__lt=777)
            else:
                rutas = Ruta.objects.filter(oficina=centro, anio=semana, estado__lt=777)

            context['rutas'] = rutas

        return render_to_response('ordenes/consulta/_table_routes.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@csrf_exempt
def estado_ruta(request):
    try:
        # print('estado_ruta')
        context = RequestContext(request)
        id_rutas = request.POST['rutas']
        # print(id_rutas)
        estados = log_rutas.objects.filter(ruta=id_rutas)

        context['estado'] = estados

        return render_to_response('ordenes/consulta/_table_logrutas.html', context)
    except Exception as e:
        log.error("Error {}".format(e))

        return HttpResponse(status=500)


@csrf_exempt
def lista_suministros(request):
    try:
        # print('-*-*-* Lista suministros')
        context = RequestContext(request)
        id_ruta = request.POST['id_ruta']
        todas = request.POST['todas']
        # print(id_ruta)
        # print("Todas "+str(todas))
        if id_ruta:
            request.session['id_ruta'] = id_ruta
            request.session['todas'] = todas

        RESULTADOS = {1: 'Lectura Normal',
                      2: 'Alto consumo',
                      3: 'Bajo consumo',
                      4: 'Sin Lectura',
                      5: 'Lectura sin controles',
                      6: 'Consumo cero',
                      7: 'Consumo negativo'}

        ruta = Ruta.objects.get(pk=id_ruta)
        print(ruta)

        if todas == '2':
            # ordenes = OrdenDeTrabajo.objects.filter(ruta=ruta).values('punto_suministro__punto_suministro', 'punto_suministro__num_contrato', 'punto_suministro__aparato__num_serie', 'numero_orden')
            # print('entra')
            ordenes = list(query_to_dicts(
                'SELECT QORDER_ORDENDETRABAJO.PUNTO_SUMINISTRO_ID, QORDER_PUNTODESUMINISTRO.NUM_CONTRATO, QORDER_APARATO.NUM_SERIE, QORDER_ORDENDETRABAJO.NUMERO_ORDEN,QORDER_DESC_LECTURA.RESULTADO_LECTURA FROM QORDER_ORDENDETRABAJO INNER JOIN QORDER_PUNTODESUMINISTRO ON ( QORDER_ORDENDETRABAJO.PUNTO_SUMINISTRO_ID=QORDER_PUNTODESUMINISTRO.PUNTO_SUMINISTRO) LEFT OUTER JOIN QORDER_APARATO ON ( QORDER_PUNTODESUMINISTRO.APARATO_ID= QORDER_APARATO.APARATO ) LEFT OUTER JOIN QORDER_DESC_LECTURA ON ( QORDER_ORDENDETRABAJO.NUMERO_ORDEN = QORDER_DESC_LECTURA.ORDEN_TRABAJO_ID ) WHERE QORDER_ORDENDETRABAJO.RUTA_ID = "' + id_ruta + '"'))

            # print(int(583/10))
        else:
            # print('llega')
            # ordenes = OrdenDeTrabajo.objects.filter(ruta=ruta).extra(where=['estado = 9 or estado=17']).values('punto_suministro__punto_suministro', 'punto_suministro__num_contrato', 'punto_suministro__aparato__num_serie', 'numero_orden','lecturas__re')
            ordenes = list(query_to_dicts(
                'SELECT QORDER_ORDENDETRABAJO.PUNTO_SUMINISTRO_ID, QORDER_PUNTODESUMINISTRO.NUM_CONTRATO, QORDER_APARATO.NUM_SERIE, QORDER_ORDENDETRABAJO.NUMERO_ORDEN,QORDER_DESC_LECTURA.RESULTADO_LECTURA FROM QORDER_ORDENDETRABAJO INNER JOIN QORDER_PUNTODESUMINISTRO ON ( QORDER_ORDENDETRABAJO.PUNTO_SUMINISTRO_ID = QORDER_PUNTODESUMINISTRO.PUNTO_SUMINISTRO ) LEFT OUTER JOIN QORDER_APARATO ON ( QORDER_PUNTODESUMINISTRO.APARATO_ID = QORDER_APARATO.APARATO ) LEFT OUTER JOIN QORDER_DESC_LECTURA ON ( QORDER_ORDENDETRABAJO.NUMERO_ORDEN = QORDER_DESC_LECTURA.ORDEN_TRABAJO_ID ) WHERE (QORDER_ORDENDETRABAJO.ESTADO = 9 OR QORDER_ORDENDETRABAJO.ESTADO=17) AND QORDER_ORDENDETRABAJO.RUTA_ID = "' + id_ruta + '"'))
            # print(583/10)
            # print('ordenes {}'.format(ordenes))
        sumin = []
        for row in ordenes:

            # print(row)
            nombre = ' '
            # desc = Desc_Lectura.objects.filter(orden_trabajo=row['numero_orden']).values('resultado_lectura').first()
            # if desc:
            try:
                if row['RESULTADO_LECTURA']:
                    nombre = RESULTADOS[row['RESULTADO_LECTURA']]
            except:
                pass
                # print('pass')
            # print('mensaje')
            dato = {"NIS": row['PUNTO_SUMINISTRO_ID'], "NIC": row['NUM_CONTRATO'], "NUM_MEDIDOR": row['NUM_SERIE'],
                    "RESULTADO": nombre, "num_orden": row['NUMERO_ORDEN']}
            sumin.append(dato)
        context['sumin'] = sumin

        return render_to_response('ordenes/consulta/_table_sum.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def datos_suministro(request):
    try:
        # print('Datos suministro')
        context = RequestContext(request)
        punto_suministro = request.POST['punto_suministro']
        num_contrato = request.POST['num_contrato']
        numero_orden = request.POST['numero_orden']
        # print(punto_suministro)
        # print(num_contrato)
        # print(numero_orden)

        if numero_orden:

            # ruta = Ruta.objects.get(pk=id_ruta)
            # print(ruta)
            # falta el filtro por todas
            sumin = PuntoDeSuministro.objects.get(punto_suministro=punto_suministro, num_contrato=num_contrato)
            orden = OrdenDeTrabajo.objects.get(pk=numero_orden)  # numero_orden
            # print("Sumin {} ".format(sumin))
            # print("Orden {} ".format(orden))
            context['sumin'] = sumin
            context['orden'] = orden
            # print('Orden1 {}'.format(orden.numero_orden))
            _orden = Desc_Orden.objects.filter(orden_trabajo_id=numero_orden)  # numero_orden
            if _orden.exists():
                context['descorden'] = _orden

                _lect = Desc_Lectura.objects.filter(orden_trabajo_id=numero_orden)
                # print("Desc_lectura {} ".format(_lect))
                context['lecturas'] = _lect
                _anom = Desc_Anomalia.objects.filter(orden_trabajo_id=numero_orden)
                # print("Desc_anomalia {} ".format(_anom))
                context['anomalias'] = _anom

                _foto = Desc_Foto.objects.filter(orden_trabajo=orden)
                # print("Desc_fotos {} ".format(len(_foto)))
                context['fotos'] = _foto
            consumos_anteriores = []
            # print('Ordern ruta {}'.format(orden.ruta.anio))
            rutas = Ruta.objects.filter(anio=orden.ruta.anio, rutasum=orden.ruta.rutasum.idrutasum)[:6]
            # print(rutas)
            for ruta in rutas:
                # print('Ruta {} Punto Suministro {}'.format(ruta.idruta,punto_suministro))
                ordenes_anteriores = OrdenDeTrabajo.objects.filter(ruta=ruta, punto_suministro=punto_suministro)
                # print(ordenes_anteriores)
                for item in ordenes_anteriores:
                    historicocsmo = HistoricoConsumo.objects.filter(consumo=item.consumo)
                    try:
                        lect_anterior = Desc_Lectura.objects.get(orden_trabajo=item)
                    except:
                        lect_anterior = None
                    try:
                        desc_orden_ant = Desc_Orden.objects.get(orden_trabajo=item)
                    except:
                        desc_orden_ant = None

                    for historico in historicocsmo:
                        try:
                            valoreshistorico = HistoricoConsumo.objects.get(codigo=historico.codigo)
                            if valoreshistorico:
                                datos = {
                                    'fecha_lectura': valoreshistorico.fecha_lectura,
                                    'lectura': valoreshistorico.lectura,
                                    'consumo': valoreshistorico.valor_consumo,
                                    'tipo_cmo': valoreshistorico.tipo_consumo
                                }
                                consumos_anteriores.append(datos)
                        except:
                            pass

        context['consumos_anteriores'] = consumos_anteriores

        return render_to_response('ordenes/consulta/_datos_sum.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


###### ------------------------- FORZADO  ------------------------- ######
@login_required(login_url=settings.LOGIN_PAGE)
def forzado_main(request):
    try:
        context = RequestContext(request)
        try:
            semana = SemanaXUser.objects.get(usuario=request.user)
            context['semana'] = semana
        except:
            pass
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)

    return render_to_response('ordenes/forzado/_forzado.html', context)


@login_required(login_url=settings.LOGIN_PAGE)
def forzar_ruta_no_leida(request):
    try:

        context = RequestContext(request)
        id_centro = request.POST['id_oficina']
        semana = request.POST['semana']
        # print(id_centro)
        if id_centro:
            centro = WorkUnit.objects.get(pk=id_centro)

            # rutas = Ruta.objects.filter(oficina=centro,estado__in=STATUS_ENABLED)
            # print('Estado id {}'.format(1))
            if semana == 'TODAS' or semana == '':
                rutas = Ruta.objects.filter(oficina=centro, estado=1)
            else:
                rutas = Ruta.objects.filter(oficina=centro, anio=semana, estado=1)

            context['rutas'] = rutas

        return render_to_response('ordenes/forzado/_table_ruta_no_leida.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def forzar_ruta_leida(request):
    try:
        # print('forzar_ruta_leida')
        context = RequestContext(request)
        id_centro = request.POST['id_oficina']
        semana = request.POST['semana']
        # print(id_centro)
        if id_centro:
            centro = WorkUnit.objects.get(pk=id_centro)

            ordpend = OrdenDeTrabajo.objects.filter(estado=33)
            ordpend.query.group_by = ['ruta']
            rut = []
            for item in ordpend.values_list('ruta'):
                # print(item[0])
                rut.append(item[0])
            # rutas = Ruta.objects.filter(oficina=centro,estado__in=STATUS_ENABLED)
            if semana == 'TODAS' or semana == '':
                rutas = Ruta.objects.filter(oficina=centro, idruta__in=rut)
            else:
                rutas = Ruta.objects.filter(oficina=centro, anio=semana, idruta__in=rut)

            context['rutas_leidas'] = rutas

        return render_to_response('ordenes/forzado/_table_ruta_leida.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


def forzar_rutas(request):
    try:
        context = RequestContext(request)
        desord = []
        deslect = []
        desanom = []
        ids_rutas = eval(request.POST['ids_rutas'])
        # print(ids_rutas)
        if len(ids_rutas) < 1:
            return HttpResponse(status=303)
        tecnico_forazado = Tecnico.objects.get(codigo='999999')
        rutas = Ruta.objects.filter(pk__in=ids_rutas)
        # print(rutas)
        for ruta in rutas:
            ordenes = OrdenDeTrabajo.objects.filter(ruta=ruta, estado__in=STATUS_ENABLED)
            for orden in ordenes:
                desord.append(Desc_Orden(id_descarga='FORZADO',
                                         orden_trabajo=orden,
                                         oficina=ruta.oficina,
                                         fecha_resolucion=datetime.now(),
                                         fh_inicio=datetime.now(),
                                         fh_fin=datetime.now(),
                                         fh_descarga=datetime.now(),
                                         tecnico=tecnico_forazado,
                                         gps_latitud=0,
                                         gps_longitud=0,
                                         secuencia_real=orden.secuencia_teorica,
                                         trabajada_offline=1,
                                         orden_modificada=0,
                                         fh_modificacion=None,
                                         usuario_modifico=None,
                                         orden_forzada=1,
                                         fh_forzado=datetime.now(),
                                         usuario_forzo=request.user))
                # print('Insertó desc_orden')
                deslect.append(Desc_Lectura(id_descarga='FORZADO',
                                            orden_trabajo=orden,
                                            secuencia_registro=orden.secuencia_teorica,

                                            num_serie=orden.punto_suministro.aparato.num_serie,
                                            # tipo_consumo = Consumo.objects.filter(aparato=orden.punto_suministro.aparato)[0].tipo_consumo,
                                            tipo_consumo=Consumo.objects.filter(consumo=orden.consumo_id)[
                                                0].tipo_consumo,
                                            tipo_aparato=orden.punto_suministro.aparato.tipo_aparato,
                                            coef_perdida=orden.punto_suministro.aparato.coef_perdida,
                                            constante=Consumo.objects.filter(aparato=orden.punto_suministro.aparato)[
                                                0].constante,
                                            lectura=0,
                                            consumo=0,
                                            paso_accion='FORZA',
                                            cantidad_intentos=0,
                                            resultado_lectura=0,
                                            consulto_historico=0,
                                            marca=orden.punto_suministro.aparato.marca,
                                            oficina=ruta.oficina))
                # print('Insertó desc_lectura')

                # si nic == 0000000 y marca + serie <> mc999 condir -> anomalia an002
                if orden.punto_suministro.num_contrato == '0000000' and orden.punto_suministro.aparato.marca != 'MC999' and orden.punto_suministro.aparato.num_serie.strip() != 'CONDIR':
                    # import pdb; pdb.set_trace()
                    id_anomalia = 'AN002'

                else:
                    id_anomalia = 'AN099'
                desanom.append(Desc_Anomalia(id_descarga='FORZADO',
                                             orden_trabajo=orden,
                                             id_anomalia=Anomalia.objects.get(id_anomalia=id_anomalia),
                                             id_observacion=None,
                                             fecha_hora_registro=datetime.now(),
                                             paso_accion=None,
                                             oficina=ruta.oficina))

                orden.estado = 401
                orden.save()
            Desc_Orden.objects.bulk_create(desord)
            Desc_Lectura.objects.bulk_create(deslect)
            Desc_Anomalia.objects.bulk_create(desanom)
            ruta.tecnico = tecnico_forazado
            ruta.estado = 265
            ruta.cantidad_leido = ruta.cantidad_leido + len(ordenes)
            # print(ruta.cantidad_leido)
            ruta.save()
            log_rutas.objects.create(estado='Forzado', fecha_log=datetime.now(),
                                     observacion='Se forzó la ruta: ' + str(ruta.ruta) + str(
                                         ruta.itinerario) + ', Cantidad de ordenes ' + str(len(ordenes)),
                                     ruta_id=ruta.idruta, usuario=request.user)
            # actualizar la cantidad de ordenes forzadas en la cabecera de rutas
            # ruta.cantidad_leido = ruta.cantidad_leido + len(ordenes)
            writeAudit('FORZADO', 'FORZADO', request.user,
                       "Ruta: {} se forzaron {} ordenes.".format(ruta, len(ordenes)))
        return HttpResponse("Se forzaron {} órdenes en {} rutas.".format(len(ordenes), len(rutas)), status=200)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse("Error forzando ruta {}".format(e), status=500)


###### ------------------------- CONFIG  ------------------------- ######
@login_required(login_url=settings.LOGIN_PAGE)
def configuracion(request):
    try:
        context = RequestContext(request)
        parametros = Parametro.objects.all();
        form = parametroForm()
        context['form'] = form
        context['parametros'] = parametros
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)

    return render_to_response('config/_config.html', context)


@login_required(login_url=settings.LOGIN_PAGE)
def configuracion_edit(request):
    try:
        context = RequestContext(request)
        # print("ENTRO configuracion_EDIT")
        id = request.POST['id']
        # print(id)
        parametro = Parametro.objects.get(parametro=id)
        context['parametro'] = parametro
        form = parametroForm(instance=parametro)
        context['form'] = form
        return render_to_response('config/_param_edit.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def configuracion_new(request):
    try:
        context = RequestContext(request)
        # print("ENTRO configuracion_NEW")
        form = parametroForm()
        context['form'] = form
        return render_to_response('config/_param_edit.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


def configuracion_delete(request):
    context = RequestContext(request)

    try:
        id = request.POST['id']
        # print("Id "+id)
        parametro = Parametro.objects.get(parametro=id)

        parametro.delete()
        parametros = Parametro.objects.all()

        context['parametros'] = parametros
        form = parametroForm()
        context['form'] = form

        return render_to_response('config/_config.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


def configuracion_save(request):
    context = RequestContext(request)

    try:
        # print("ENTRO configuracion_SAVE")

        accion = request.POST['accion']
        # print(accion)

        if accion == 'edit':
            id = request.POST['id']
            # print("Id "+id)
            parametro = Parametro.objects.get(parametro=id)

            form = parametroForm(request.POST, instance=parametro)

            if form.is_valid():
                form.save()
                writeAudit("configuración", "editar", request.user, form.cleaned_data)

                parametros = Parametro.objects.all()

                context['parametros'] = parametros

                context['form'] = form
                # return HttpResponse("getPage('{% url 'qorder:atp_main' %}')")
                return render_to_response('config/_config.html', context)
            # print('Form no valido')
            # print(form.errors.as_json())
        else:

            form = parametroForm(request.POST)

            if form.is_valid():
                # print("form is valid")
                new_parametro = form.save()
                writeAudit("configuración", "nueva", request.user, form.cleaned_data)

                parametros = Parametro.objects.all()
                context['parametros'] = parametros
                context['form'] = form
                # return HttpResponse("getPage('{% url 'qorder:atp_main' %}')")

                return render_to_response('config/_config.html', context)
            # print('Form no valido')
            # print(form.errors.as_json())
            return HttpResponse('Complete los campos obligatorios', status=301)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)
    form = parametroForm()
    context['parametros'] = parametros
    context['form'] = form

    return render_to_response('config/_param_edit.html', context)


def tecnico_liberarTPL(request):
    context = RequestContext(request)
    _codigo = request.POST['codigo']
    # print(_codigo)
    try:

        tecnico = Tecnico.objects.get(codigo=_codigo)

    except Exception as e:
        log.error(str(e))
        return HttpResponse(status=300)

    try:

        tecnico.liberar('1')

        rutas = Ruta.objects.filter(tecnico=tecnico, estado__in=[7, 3])
        # print('pasa')
        rutas.update(tecnico=None, estado=33, fecha_hora_asignacion=None, usuario_asignacion=None,
                     flag_asignacion_guardada='0')
        ordenes = OrdenDeTrabajo.objects.filter(tecnico=tecnico, estado__in=[7, 3])
        # print('pasa1')
        ordenes.update(tecnico=None, estado=33, fecha_hora_asignacion=None, usuario_asignacion=None,
                       flag_asignacion_guardada='0')
        # print('pasa2')
        tt = TerminalPortatil.objects.filter(numero_serie=tecnico.terminal_portatil_id)
        # print('pasa3')
        tt.update(estado_cargada='0', cantidad_cargada=0)

        writeAudit("gestion tecnicos", "edicion", request.user,
                   "se liberó los datos del técnico {}".format(tecnico.nombre_completo()))

        _mensaje = 'La TPL del lector: {} - {}, {} se liberó correctamente'.format(tecnico.codigo, tecnico.nombre_1,
                                                                                   tecnico.apellido_1)
        return HttpResponse(_mensaje, status=200)

    except Exception as e:
        log.error(str(e))
        return HttpResponse(status=500)


###### ------------------------- MONITOR  ------------------------- ######
@login_required(login_url=settings.LOGIN_PAGE)
def monitor_main(request):
    try:
        context = RequestContext(request)
        context['tecnicos'] = []


    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)

    return render_to_response('ordenes/monitor/_monitor.html', context)


@csrf_exempt
def monitor_tech(request):
    try:
        context = RequestContext(request)
        id_centro = request.POST['id_oficina']
        _result = []
        # print(id_centro)
        if id_centro:
            centro = WorkUnit.objects.get(pk=id_centro)
            tecnicos_oficina = OficinaXTecnico.objects.filter(oficina=id_centro, fecha_baja=None)
            tecs = []
            for item in tecnicos_oficina:
                tecs.append(item.tecnico.codigo)
            # print(tecs)
            tecnicos = Tecnico.objects.select_related('terminal_portatil',
                                                      'terminal_portatil__fh_ultima_conexion').filter(codigo__in=tecs,
                                                                                                      terminal_portatil__isnull=False).values(
                'codigo', 'terminal_portatil', 'terminal_portatil__fh_ultima_conexion', 'nombre_1', 'apellido_1')
            # tecnicos = Tecnico.objects.filter(codigo__in=tecs,terminal_portatil__isnull=False)
            for tec in tecnicos:
                _rutas = []
                strruta = ''
                rutas = Ruta.objects.filter(tecnico=tec['codigo'], estado__in=[3, 7]).values('ruta')
                segmentos = OrdenDeTrabajo.objects.filter(tecnico=tec['codigo'], estado__in=[3, 7],
                                          punto_suministro__segmentosum_id__isnull=False
                                          ).values_list('punto_suministro__segmentosum_id__codigo_segmento',
                                                        flat=True).distinct()

                segmentos_str = ", ".join(segmentos)
                
                for ruta in rutas:
                    _rutas.append(ruta['ruta'])

                    strruta = ','.join(_rutas)

                hora = tec['terminal_portatil__fh_ultima_conexion']
                if hora == None:
                    hora == ''
                else:
                    hora = tec['terminal_portatil__fh_ultima_conexion'].strftime("%d/%m/%Y %H:%M:%S")

                _result.append({'codigo': tec['codigo'],
                                'nombre': tec['nombre_1'],
                                'apellido_1': tec['apellido_1'],
                                'TP': tec['terminal_portatil'],
                                'fh_ultima_conexion': hora,
                                'rutas': strruta,
                                'segmentos': segmentos_str
                                })
            # print(len(tecnicos))
            context['tecnicos'] = _result
            # print(tecnicos)

            estados = []
            datos = {
                'estado': 'Asignadas',
                'cantidad': 0
            }
            estados.append(datos)
            datos = {
                'estado': 'Cargadas',
                'cantidad': 0
            }
            estados.append(datos)
            datos = {
                'estado': 'Trabajadas',
                'cantidad': 0
            }
            estados.append(datos)
            datos = {
                'estado': 'Listas para exportar',
                'cantidad': 0
            }
            estados.append(datos)
            datos = {
                'estado': 'Exportadas',
                'cantidad': 0
            }
            estados.append(datos)
            context['estados'] = estados

        return render_to_response('ordenes/monitor/_table_techs.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


def testBit(int_type, offset):
    # print('Testbit:'+str(int_type)+" offset:"+str(offset))
    mask = 1 << offset
    # print(str(mask))
    # print('Result: '+str(int_type & mask))
    return (int_type & mask)


@csrf_exempt
def monitor_estado(request):
    try:
        # print('entra est')
        context = RequestContext(request)
        id_tecnico = request.POST['id_tecnico']
        # print("MONITOR_ESTADO {}".format(id_tecnico))
        if id_tecnico:
            tecnicos = Tecnico.objects.get(codigo=id_tecnico)

            context['tecnicos'] = tecnicos
            # print(tecnicos)
            hoy = datetime.now().strftime("%Y%m%d000000")
            # print(hoy)
            myOrdersExp = OrdenDeTrabajo.objects.filter(tecnico=tecnicos, fecha_hora_exportacion__gte=hoy).values(
                'estado').annotate(total=Count('estado')).extra(
                where=['estado = 777 OR estado = 785 OR estado= 913 OR estado = 905'])
            # print('myOrdersExp {}'.format(myOrdersExp))

            myOrders = OrdenDeTrabajo.objects.filter(tecnico=tecnicos).values('estado').annotate(
                total=Count('estado')).exclude(estado__in=[777, 785, 913, 905])
            # print('myOrders {}'.format(myOrders))
            estados = []
            datos = {
                'estado': 'Asignadas',
                'cantidad': 0,
                'porcent': 0
            }
            estados.append(datos)
            datos = {
                'estado': 'Cargadas',
                'cantidad': 0,
                'porcent': 0
            }
            estados.append(datos)
            datos = {
                'estado': 'Trabajadas',
                'cantidad': 0,
                'porcent': 0
            }
            estados.append(datos)
            datos = {
                'estado': 'Listas para exportar',
                'cantidad': 0,
                'porcent': 0
            }
            estados.append(datos)
            datos = {
                'estado': 'Exportadas',
                'cantidad': 0,
                'porcent': 0
            }
            estados.append(datos)
            totalGral = 0
            for order in myOrders:
                # print('Test bit: '+str(order.get('estado'))+' '+str(testBit(order.get('estado'),1)))
                if order.get('estado') == 3:
                    total = estados[0].get('cantidad') + order.get('total')
                    totalGral = totalGral + order.get('total')
                    w1 = {"estado": "Asignadas", "cantidad": total}
                    estados[0].update(w1)
                if order.get('estado') == 7:
                    total = estados[1].get('cantidad') + order.get('total')
                    totalGral = totalGral + order.get('total')
                    w1 = {"estado": "Cargadas", "cantidad": total}
                    estados[1].update(w1)
                if order.get('estado') == 9 or order.get('estado') == 17:
                    total = estados[2].get('cantidad') + order.get('total')
                    totalGral = totalGral + order.get('total')

                    w1 = {"estado": "Trabajadas", "cantidad": total}
                    estados[2].update(w1)
                if order.get('estado') == 265 or order.get('estado') == 273:
                    total = estados[3].get('cantidad') + order.get('total')
                    totalGral = totalGral + order.get('total')
                    w1 = {"estado": "Listas para exportar", "cantidad": total}
                    estados[3].update(w1)
            for order in myOrdersExp:
                if testBit(order.get('estado'), 9) > 0:
                    total = estados[4].get('cantidad') + order.get('total')
                    totalGral = totalGral + order.get('total')
                    w1 = {"estado": "Exportadas", "cantidad": total}
                    estados[4].update(w1)
            # print('Estados {}'.format(estados))
            # print('Total gral. {}'.format(totalGral))
            for x in range(0, 5):
                w1 = estados[x]
                # print(w1)
                # print(w1.get('cantidad'))
                b = w1.get('cantidad')
                if totalGral == 0:
                    a = 0
                else:
                    # print('Cantidad {}'.format(b))
                    a = b / totalGral * 100
                    # print('Porcentaje {}'.format(str(round(a))))

                w1 = {"estado": w1.get('estado'), "cantidad": w1.get('cantidad'), "porcent": round(a)}
                estados[x].update(w1)

            # print(estados)
            context['estados'] = estados

        return render_to_response('ordenes/monitor/_table_estado.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@csrf_exempt
def monitor_getorders(request):
    # try:
    #     # print('entra get')
    #     context = RequestContext(request)
    #     ordenes = []
    #     id_tecnico = request.POST['id_tecnico']
    #     if len(id_tecnico) == 0:
    #         return HttpResponse(status=302)

    #     tipo = request.POST['tipo']
    #     # print("Tipo {}".format(tipo))
    #     '''
    #     tecnico = Tecnico.objects.get(pk=id_tecnico)
    #     print("Tipo "+tipo)
    #     if int(tipo) == 0:
    #         ordenes = tecnico.get_asignadas()
    #     elif int(tipo) == 1:
    #         ordenes = tecnico.get_cargadas()
    #     elif int(tipo) == 2:
    #         ordenes = tecnico.get_trabajadas()
    #     elif int(tipo) == 3:
    #         ordenes = tecnico.get_exportadas()
    #     print(ordenes)
    #     if len(ordenes)<1:
    #         return HttpResponse(status=301)
    #     print("Cantidad de ordenes "+str(len(ordenes)))
    #     '''
    #     context['ordenes'] = ordenes
    #     request.session['id_tecnico'] = id_tecnico
    #     request.session['tipo'] = tipo
    #     return render_to_response('ordenes/monitor/_table_ordenes.html', context)
    # except Exception as e:
    #     print("Error {}".format(e))
    #     return HttpResponse(status=500)


    try:
        context = RequestContext(request)
        id_tecnico = request.POST['id_tecnico']
        tipo = request.POST['tipo']
        _resultado = []
        ordenes = []

        if len(id_tecnico) == 0:
            return HttpResponse(status=302)

        tecnico = Tecnico.objects.get(pk=id_tecnico)

        q = Q()

        q.add(Q(tecnico=tecnico), Q.AND)

        if int(tipo) == 0:  # asignadas

            q.add(Q(estado=3), Q.AND)

        elif int(tipo) == 1:  # cargadas

            q.add(Q(estado=7), Q.AND)

        elif int(tipo) == 2:  # trabajadas

            q.add(Q(estado__in=[9,17]), Q.AND)

        elif int(tipo) == 3:  # lista para exportar

            q.add(Q(estado__in=[265,273]), Q.AND)

        elif int(tipo) == 4:  # exportadas

            hoy = datetime.now().strftime("%Y%m%d000000")

            q.add(Q(estado__in=[777,785,913,905]), Q.AND)

            q.add(Q(fecha_hora_exportacion__gte=hoy), Q.AND)


        ordenes = OrdenDeTrabajo.objects.select_related('punto_suministro','punto_suministro__cliente','punto_suministro__aparato').\
            filter(q).\
            values('numero_orden','punto_suministro','punto_suministro__cliente','punto_suministro__secuencia_teorica',\
                'punto_suministro__aparato__num_serie','punto_suministro__cliente__apellido_1',\
                'punto_suministro__calle','punto_suministro__numero_puerta',\
                'punto_suministro__municipio', 'ruta__ruta', 'punto_suministro__segmentosum_id__codigo_segmento')


        for o in ordenes:

            _resultado.append({
                "num_orden": o['numero_orden'],
                "punto_suministro": o['punto_suministro'],
                "nic": o['punto_suministro__cliente'],
                "secuencia": o['punto_suministro__secuencia_teorica'],
                "num_serie": o['punto_suministro__aparato__num_serie'],
                "cliente_nombre": o['punto_suministro__cliente__apellido_1'],
                "cliente_calle": o['punto_suministro__calle'],
                "cliente_num_puerta": o['punto_suministro__numero_puerta'],
                "cliente_municipio": o['punto_suministro__municipio'],
                "ruta": o['ruta__ruta'],
                "segmento": o['punto_suministro__segmentosum_id__codigo_segmento'],
            })

        context['ordenes'] = _resultado

        return render_to_response('ordenes/monitor/_table_ordenes.html', context)


    except Exception as e:

        print("Error {}".format(e))
        return HttpResponse(status=500)
        

@csrf_exempt
def monitor_getorder(request):
    try:
        # print('entra geto')
        context = RequestContext(request)
        numero_orden = request.POST['numero_orden']
        if len(numero_orden) == 0:
            return HttpResponse(status=302)

        _ot = OrdenDeTrabajo.objects.get(numero_orden=numero_orden)
        _pts = _ot.punto_suministro
        # print("{} {}".format(_pts.gps_latitud,_pts.gps_longitud))
        val = eval(_pts.gps_latitud)
        # print('val {}'.format(val))
        val1 = eval(_pts.gps_longitud)
        if val == 0:
            context['lat'] = ''
            context['lon'] = ''
        else:
            context['lat'] = "{}".format(val)
            context['lon'] = "{}".format(val1)
        # context['lat'] = "{}".format(-31.4113406)
        # context['lon'] = "{}".format(-64.168718)
        # print('error')
        try:
            _orden = Desc_Orden.objects.get(orden_trabajo=numero_orden)
            context['lat'] = "{}".format(_orden.gps_latitud)
            context['lon'] = "{}".format(_orden.gps_longitud)
        except:
            print("Sin datos de descarga")

        _lect = Desc_Lectura.objects.filter(orden_trabajo=numero_orden)

        # print('Lecturas {}'.format(len(_lect)))
        context['lecturas'] = _lect
        _anom = Desc_Anomalia.objects.filter(orden_trabajo=numero_orden)
        # print('Anomalias {}'.format(len(_anom)))
        context['anomalias'] = _anom

        _foto = Desc_Foto.objects.filter(orden_trabajo=numero_orden)
        # print('{}'.format(len(_foto)))
        context['fotos'] = _foto
        # print('{}'.format(len(_foto)))

        return render_to_response('ordenes/monitor/_detalle_orden.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


###### ------------------------- MONITOR_RUTAS ------------------------- ######
@login_required(login_url=settings.LOGIN_PAGE)
def monitor_rutas_main(request):
    try:
        context = RequestContext(request)
        context['tecnicos'] = []
        try:
            semana = SemanaXUser.objects.get(usuario=request.user)
            context['semana'] = semana
        except:
            pass

    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)

    return render_to_response('ordenes/monitor_rutas/_monitor.html', context)


@csrf_exempt
def monitor_rutas(request):
    try:
        # print('Monitor_rutas')
        context = RequestContext(request)
        id_centro = request.POST['id_oficina']
        semana = request.POST['semana']
        # print('Oficina {}'.format(id_centro))
        if id_centro:
            centro = WorkUnit.objects.get(pk=id_centro)
            # print(centro)
            hoy = datetime.now().strftime('%Y%m%d000000')
            if semana == 'TODAS' or semana == '':
                rutas = Ruta.objects.filter(oficina=centro).exclude(fecha_hora_exportacion__gt=hoy)
            else:
                rutas = Ruta.objects.filter(oficina=centro, anio=semana).exclude(fecha_hora_exportacion__gt=hoy)
            valor = rutas.count()
            if valor == 0:
                rutas = 0
                context['leidos'] = 0
                context['cantidades'] = 0
                context['cantidad_total'] = 0
                # print('entra')
                return render_to_response('ordenes/monitor_rutas/_table_routes.html', context)
            else:
                context['rutas'] = rutas
                # print(rutas)
                if semana == 'TODAS' or semana == '':
                    leidos = Ruta.objects.filter(oficina=centro).exclude(fecha_hora_exportacion__gt=hoy).aggregate(
                        Sum('cantidad_leido'))
                else:
                    leidos = Ruta.objects.filter(oficina=centro, anio=semana).exclude(
                        fecha_hora_exportacion__gt=hoy).aggregate(Sum('cantidad_leido'))
                # leidos = Ruta.objects.filter(oficina=centro).exclude(fecha_hora_exportacion__lt=hoy).aggregate(Sum('cantidad_leido'))
                # print(leidos)
                context['leidos'] = leidos.get('cantidad_leido__sum')
                if semana == 'TODAS' or semana == '':
                    cantidades = Ruta.objects.filter(oficina=centro).exclude(fecha_hora_exportacion__gt=hoy).aggregate(
                        Sum('cantidad'))
                else:
                    cantidades = Ruta.objects.filter(oficina=centro, anio=semana).exclude(
                        fecha_hora_exportacion__gt=hoy).aggregate(Sum('cantidad'))
                # cantidades = Ruta.objects.filter(oficina=centro).exclude(fecha_hora_exportacion__lt=hoy).aggregate(Sum('cantidad'))
                # print(cantidades)
                context['cantidades'] = cantidades.get('cantidad__sum')
                context['cantidad_total'] = cantidades.get('cantidad__sum')
                estados = []
                datos = {
                    'estado': 'Asignadas',
                    'cantidad': 0
                }
                estados.append(datos)
                datos = {
                    'estado': 'Cargadas',
                    'cantidad': 0
                }
                estados.append(datos)
                datos = {
                    'estado': 'Trabajadas',
                    'cantidad': 0
                }
                estados.append(datos)
                datos = {
                    'estado': 'Exportadas',
                    'cantidad': 0
                }
                estados.append(datos)
                context['estados'] = estados
        return render_to_response('ordenes/monitor_rutas/_table_routes.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


def testBit(int_type, offset):
    # print('Testbit:'+str(int_type)+" offset:"+str(offset))
    mask = 1 << offset
    # print(str(mask))
    # print('Result: '+str(int_type & mask))
    return (int_type & mask)


@csrf_exempt
def monitor_rutas_estado(request):
    try:
        context = RequestContext(request)
        id_tecnico = request.POST['id_tecnico']
        # print("MONITOR_ESTADO {}".format(id_tecnico))
        if id_tecnico:
            tecnicos = Tecnico.objects.get(codigo=id_tecnico)

            context['tecnicos'] = tecnicos
            # print(tecnicos)
            myOrders = tecnicos.myOrdersByEstado()
            # print(myOrders)
            estados = []
            datos = {
                'estado': 'Asignadas',
                'cantidad': 0,
                'porcent': 0
            }
            estados.append(datos)
            datos = {
                'estado': 'Cargadas',
                'cantidad': 0,
                'porcent': 0
            }
            estados.append(datos)
            datos = {
                'estado': 'Trabajadas',
                'cantidad': 0,
                'porcent': 0
            }
            estados.append(datos)
            datos = {
                'estado': 'Exportadas',
                'cantidad': 0,
                'porcent': 0
            }
            estados.append(datos)
            totalGral = 0
            for order in myOrders:
                # print('Test bit: '+str(order.get('estado'))+' '+str(testBit(order.get('estado'),1)))
                if order.get('estado') == 3:
                    total = estados[0].get('cantidad') + order.get('total')
                    totalGral = totalGral + total
                    w1 = {"estado": "Asignadas", "cantidad": total}
                    estados[0].update(w1)
                if order.get('estado') == 7:
                    total = estados[1].get('cantidad') + order.get('total')
                    totalGral = totalGral + total
                    w1 = {"estado": "Cargadas", "cantidad": total}
                    estados[1].update(w1)
                if testBit(order.get('estado'), 3) > 0 or testBit(order.get('estado'), 5) > 0 or testBit(
                        order.get('estado'), 8) > 0:
                    total = estados[2].get('cantidad') + order.get('total')
                    totalGral = totalGral + total
                    w1 = {"estado": "Trabajadas", "cantidad": total}
                    estados[2].update(w1)
                if testBit(order.get('estado'), 9) > 0:
                    total = estados[3].get('cantidad') + order.get('total')
                    totalGral = totalGral + total
                    w1 = {"estado": "Exportadas", "cantidad": total}
                    estados[3].update(w1)

            for x in range(0, 3):
                w1 = estados[x]
                # print(w1)
                # print(w1.get('cantidad'))
                b = w1.get('cantidad')
                a = b / totalGral * 100
                # print(str(round(a)))

                w1 = {"estado": w1.get('estado'), "cantidad": w1.get('cantidad'), "porcent": round(a)}
                estados[x].update(w1)

            # print(estados)
            context['estados'] = estados

        return render_to_response('ordenes/monitor_rutas/_table_estado.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@csrf_exempt
def monitor_rutas_getorders(request):
    try:
        context = RequestContext(request)
        ordenes = []
        id_tecnico = request.POST['id_tecnico']
        if len(id_tecnico) == 0:
            return HttpResponse(status=302)

        tipo = request.POST['tipo']
        '''
        tecnico = Tecnico.objects.get(pk=id_tecnico)
        print("Tipo "+tipo)
        if int(tipo) == 0:
            ordenes = tecnico.get_asignadas()
        elif int(tipo) == 1:
            ordenes = tecnico.get_cargadas()
        elif int(tipo) == 2:
            ordenes = tecnico.get_trabajadas()
        elif int(tipo) == 3:
            ordenes = tecnico.get_exportadas()
        print(ordenes)
        if len(ordenes)<1:
            return HttpResponse(status=301)
        print("Cantidad de ordenes "+str(len(ordenes)))
        '''
        context['ordenes'] = ordenes
        request.session['id_tecnico'] = id_tecnico
        request.session['tipo'] = tipo
        return render_to_response('ordenes/monitor_rutas/_table_ordenes.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@csrf_exempt
def monitor_rutas_getorder(request):
    try:
        context = RequestContext(request)

        numero_orden = request.POST['numero_orden']
        if len(numero_orden) == 0:
            return HttpResponse(status=302)

        _ot = OrdenDeTrabajo.objects.get(numero_orden=numero_orden)
        _pts = _ot.punto_suministro
        # print("{} {}".format(_pts.gps_latitud,_pts.gps_longitud))
        # context['lat'] = "{}".format(_pts.gps_latitud)
        # context['lon'] = "{}".format(gps_longitud)
        context['lat'] = "{}".format(-31.4113406)
        context['lon'] = "{}".format(-64.168718)

        _lect = Desc_Lectura.objects.filter(orden_trabajo=numero_orden)

        # print('Lecturas {}'.format(len(_lect)))
        context['lecturas'] = _lect
        _anom = Desc_Anomalia.objects.filter(orden_trabajo=numero_orden)
        # print('Anomalias {}'.format(len(_anom)))
        context['anomalias'] = _anom

        _foto = Desc_Foto.objects.filter(orden_trabajo=numero_orden)
        # print('{}'.format(len(_foto)))
        context['fotos'] = _foto
        # print('{}'.format(len(_foto)))

        return render_to_response('ordenes/monitor_rutas/_detalle_orden.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


###### ------------------------- MAPS ULTIMA POSICION  ------------------------- ######

@login_required(login_url=settings.LOGIN_PAGE)
def ultima_posicion(request):
    context = RequestContext(request)
    return render_to_response('gps/ultima/_lp_monitor.html', context)


@csrf_exempt
def maps_up_techs(request):
    try:
        context = RequestContext(request)
        id_centro = request.POST['id_centro']
        listatecnicos = []
        for tipoPersonal in request.user.tiposPersonal.all():
            listatecnicos.append(tipoPersonal)
        tecnicos_oficina = OficinaXTecnico.objects.filter(oficina=id_centro, fecha_baja=None)
        tecs = []
        for item in tecnicos_oficina:
            tecs.append(item.tecnico.codigo)
        # print(tecs)
        tecnicos = Tecnico.objects.filter(codigo__in=tecs)

        context['tecnicos'] = tecnicos

        # Tecnico.objects.filter(Q(id_unidad_negocio__id_workunit=id_centro),
        #                                                Q(activo='1'),
        #                                                Q(id_tipo_personal__isnull=True) | Q(id_tipo_personal__in=listatecnicos))
        # print("Tecnicos " + str(tecnicos))
        return render_to_response('gps/ultima/_table_techs.html', context)
    except Exception as e:
        log.error('Error {}'.format(e))
        return HttpResponse(status=500)


@csrf_exempt
def get_map_last_p(request):
    context = RequestContext(request)
    if request.method == 'POST':
        try:
            id_centro = request.POST['id_oficina']
            oficina = WorkUnit.objects.get(pk=id_centro)
            context['center'] = oficina.getHashmap()
            ids_tecnicos = eval(request.POST['ids_tecnicos'])
            ids_tecnicos_sin_puntos = eval(request.POST['ids_tecnicos_sin_puntos'])
            # print('ids_tecnicos {}'.format(ids_tecnicos))

            aprox = request.POST['aproximar']
            if ('true' in aprox):
                context['aprox'] = True
            else:
                context['aprox'] = False
            if len(ids_tecnicos) < 1 and len(ids_tecnicos_sin_puntos) < 1:
                return HttpResponse(status=300)

            if len(ids_tecnicos) < 1 and len(ids_tecnicos_sin_puntos) >= 1:
                return HttpResponse(status=301)

            tecnicos = Tecnico.objects.filter(codigo__in=ids_tecnicos)

            # print("tecnicos = " + str(tecnicos))
            context['tecnicos'] = tecnicos
            context['tsg'] = ids_tecnicos_sin_puntos

            # print( context )

            return render_to_response('gps/ultima/_lp_map.html', context)
        except Exception as e:
            log.error('Error {}'.format(e))
    return HttpResponse(status=500)


###### ------------------------- LISTADO RECORRIDO  ------------------------- ######

@login_required(login_url=settings.LOGIN_PAGE)
def listadorecorrido(request):
    context = RequestContext(request)
    return render_to_response('gps/listadorecorrido/_listadorecorrido.html', context)


@csrf_exempt
def listadorecorrido_techs(request):
    try:
        context = RequestContext(request)
        id_centro = request.POST['id_centro']
        listatecnicos = []
        for tipoPersonal in request.user.tiposPersonal.all():
            listatecnicos.append(tipoPersonal)

        tecnicos_oficina = OficinaXTecnico.objects.filter(oficina=id_centro, fecha_baja=None)
        tecs = []
        for item in tecnicos_oficina:
            tecs.append(item.tecnico.codigo)
        # print(tecs)
        tecnicos = Tecnico.objects.filter(codigo__in=tecs)

        context['tecnicos'] = tecnicos

        # Tecnico.objects.filter(Q(id_unidad_negocio__id_workunit=id_centro),
        #                                                Q(activo='1'),
        #                                                Q(id_tipo_personal__isnull=True) | Q(id_tipo_personal__in=listatecnicos))
        # print("Tecnicos " + str(tecnicos))
        return render_to_response('gps/listadorecorrido/_table_techs.html', context)
    except Exception as e:
        log.error('Error {}'.format(e))
        return HttpResponse(status=500)


@csrf_exempt
def get_listadorecorrido(request):
    try:
        context = RequestContext(request)
        id_tecnico = request.POST['id_tecnico']
        fecha = request.POST['fecha']
        hours_min = int(float(request.POST['hours_min']))
        hours_max = int(float(request.POST['hours_max']))

        puntosGPS = request.POST['puntosGPS']

        aprox = request.POST['aproximar']

        tecnico = Tecnico.objects.filter(codigo=id_tecnico)
        # print("Tecnico "+str(tecnico))

        # dt_from = datetime.datetime.strptime("{}{:02d}0000".format(fecha, hours_min), "%Y%m%d%H%M%S")
        # dt_to = datetime.datetime.strptime("{}{:02d}5959".format(fecha, hours_max), "%Y%m%d%H%M%S")
        dt_from = datetime.strptime("{}{:02d}0000".format(fecha, hours_min), "%Y%m%d%H%M%S")
        dt_from = dt_from.strftime("%Y%m%d%H0000")
        dt_to = datetime.strptime("{}{:02d}5959".format(fecha, hours_max), "%Y%m%d%H%M%S")
        dt_to = dt_to.strftime("%Y%m%d%H5959")

        actividades = GpsActividadesUsuarios.objects.filter(tecnico=tecnico,
                                                            fh_registro__gte=dt_from,
                                                            fh_registro__lte=dt_to,
                                                            latitud__contains='.').order_by('fh_registro')

        ret_pos = []
        # print(puntosGPS)
        if ('true' in puntosGPS):
            posiciones = GpsRegistroPosiciones.objects.filter(tecnico=tecnico,
                                                              hora_registro__gte=hours_min,
                                                              hora_registro__lte=hours_max,
                                                              fecha_registro=fecha).order_by('hora_registro')

            count = 0
            valores = posiciones.values('posiciones')
            last_lat = 0
            last_long = 0
            for p in valores:
                for values in p['posiciones'].split("|"):
                    # print(values)
                    try:
                        lat = values.split(';')[1]
                        lon = values.split(';')[2]
                        hora = values.split(';')[0]

                        datetimeobject = datetime.strptime(hora, '%Y%m%d%H%M%S')

                        newformat2 = datetimeobject.strftime('%d/%m/%Y %H:%M:%S')

                    except Exception as e:
                        log.error('Error {}'.format(e))
                        continue
                    if count == 0:
                        ret_pos.append({'latitud': lat, 'longitud': lon, 'hora': newformat2, 'evento': 'GPS'})
                        last_long = lon
                        last_lat = lat
                    else:
                        dif_lat = float(lat) - float(last_lat)
                        dif_long = float(lon) - float(last_long)
                        # TODO FILTRAR
                        d = 0
                        try:
                            pi = 3.14159265358979323846
                            lat1 = float(lat) * pi / 180
                            lon1 = float(lon) * pi / 180
                            lat2 = float(last_lat) * pi / 180
                            lon2 = float(last_long) * pi / 180

                            d = 6378.137 * math.acos(
                                math.cos(lat1) * math.cos(lat2) * math.cos(lon2 - lon1) + math.sin(lat1) * math.sin(
                                    lat2))
                        except:
                            d = 0
                        # print("distancia: " + str(d))
                        # print( dif_long ** 2)
                        if (d > 0.01):
                            ret_pos.append({'latitud': lat, 'longitud': lon, 'hora': newformat2, 'evento': 'GPS'})
                            last_long = lon
                            last_lat = lat


                        else:
                            print("Eliminado " + lat + "," + lon)
                    count += 1

        for p in actividades:
            try:
                lat = p.latitud
                lon = p.longitud
                hora = p.fh_registro
                datetimeobject = datetime.strptime(hora, '%Y%m%d%H%M%S')

                newformat2 = datetimeobject.strftime('%d/%m/%Y %H:%M:%S')
                evento = "{}-{}".format(p.actividad, p.ref_actividad)
                ret_pos.append({'latitud': lat, 'longitud': lon, 'hora': newformat2, 'evento': evento})
            except:
                continue

        # print(ret_pos)

        ret_pos.sort(key=itemgetter('hora'), reverse=False)
        context['positions'] = ret_pos
        context['actividades'] = actividades
        titulo = '{}_{}_{}_{}'.format(tecnico[0].nombre_1, tecnico[0].apellido_1, dt_from, dt_to)
        context['titulo'] = titulo

        if ('true' in aprox):
            context['aprox'] = True
        else:
            context['aprox'] = False

        return render_to_response('gps/listadorecorrido/_listado.html', context)
    except Exception as e:
        log.error("ERROR: {}".format(e))
        return HttpResponse(status=500)


###### ------------------------- MAPS RECORRIDO  ------------------------- ######

@login_required(login_url=settings.LOGIN_PAGE)
def recorrido(request):
    context = RequestContext(request)
    return render_to_response('gps/recorrido/_route_monitor.html', context)


@csrf_exempt
def maps_route_techs(request):
    try:
        context = RequestContext(request)
        id_centro = request.POST['id_centro']
        listatecnicos = []
        for tipoPersonal in request.user.tiposPersonal.all():
            listatecnicos.append(tipoPersonal)

        tecnicos_oficina = OficinaXTecnico.objects.filter(oficina=id_centro, fecha_baja=None)
        tecs = []
        for item in tecnicos_oficina:
            tecs.append(item.tecnico.codigo)
        # print(tecs)
        tecnicos = Tecnico.objects.filter(codigo__in=tecs)

        context['tecnicos'] = tecnicos

        # Tecnico.objects.filter(Q(id_unidad_negocio__id_workunit=id_centro),
        #                                                Q(activo='1'),
        #                                                Q(id_tipo_personal__isnull=True) | Q(id_tipo_personal__in=listatecnicos))
        # print("Tecnicos " + str(tecnicos))
        return render_to_response('gps/recorrido/_table_techs.html', context)
    except Exception as e:
        log.error('Error {}'.format(e))
        return HttpResponse(status=500)


def get_map_route(request):
    try:
        context = RequestContext(request)
        id_centro = request.POST['id_oficina']
        oficina = WorkUnit.objects.get(pk=id_centro)
        context['center'] = oficina.getHashmap()
        id_tecnico = request.POST['id_tecnico']
        fecha = request.POST['fecha']
        hours_min = int(float(request.POST['hours_min']))
        hours_max = int(float(request.POST['hours_max']))

        aprox = request.POST['aproximar']

        tecnico = Tecnico.objects.filter(codigo=id_tecnico)
        # print("Tecnico "+str(tecnico))
        posiciones = GpsRegistroPosiciones.objects.filter(tecnico=tecnico,
                                                          hora_registro__gte=hours_min,
                                                          hora_registro__lte=hours_max,
                                                          fecha_registro=fecha)

        dt_from = datetime.strptime("{}{:02d}0000".format(fecha, hours_min), "%Y%m%d%H%M%S")
        dt_from = dt_from.strftime("%Y%m%d%H0000")
        dt_to = datetime.strptime("{}{:02d}5959".format(fecha, hours_max), "%Y%m%d%H%M%S")
        dt_to = dt_to.strftime("%Y%m%d%H5959")

        actividades = GpsActividadesUsuarios.objects.filter(tecnico=tecnico,
                                                            fh_registro__gte=dt_from,
                                                            fh_registro__lte=dt_to,
                                                            latitud__contains='.').order_by('fh_registro')

        ret_pos = []
        count = 0
        valores = posiciones.values('posiciones')
        last_lat = 0
        last_long = 0
        for p in valores:
            for values in p['posiciones'].split("|"):
                # print(values)
                try:
                    lat = values.split(';')[1]
                    lon = values.split(';')[2]
                except:
                    continue
                if count == 0:
                    ret_pos.append({'latitud': lat, 'longitud': lon})
                    last_long = lon
                    last_lat = lat
                else:
                    dif_lat = float(lat) - float(last_lat)
                    dif_long = float(lon) - float(last_long)
                    # TODO FILTRAR
                    d = 0
                    try:
                        pi = 3.14159265358979323846
                        lat1 = float(lat) * pi / 180
                        lon1 = float(lon) * pi / 180
                        lat2 = float(last_lat) * pi / 180
                        lon2 = float(last_long) * pi / 180

                        d = 6378.137 * math.acos(
                            math.cos(lat1) * math.cos(lat2) * math.cos(lon2 - lon1) + math.sin(lat1) * math.sin(lat2))
                    except:
                        d = 0
                    # print("distancia: " + str(d))
                    # print( dif_long ** 2)
                    if (d > 0.01):
                        ret_pos.append({'latitud': lat, 'longitud': lon})
                        last_long = lon
                        last_lat = lat
                        # print("Agregado "+lat+","+lon)

                    else:
                        # print("Eliminado "+lat+","+lon)
                        pass
                count += 1

        context['positions'] = ret_pos
        context['actividades'] = actividades

        if ('true' in aprox):
            context['aprox'] = True
        else:
            context['aprox'] = False

        return render_to_response('gps/recorrido/_lp_map.html', context)
    except Exception as e:
        log.error("ERROR: {}".format(e))
        return HttpResponse(status=500)


def true_or_false(val):
    if ('true' in val):
        return True
    else:
        return False


def get_data_activity(request):
    try:
        context = RequestContext(request)
        data_act = request.POST['data_act']
        secuencia = request.POST['secuencia']
        aprox = request.POST['aproximar']

        ref_actividad, id_actividad, fh_registro = data_act.split('~')

        actividad = GpsActividadesUsuarios.objects.filter(ref_actividad=ref_actividad,
                                                          actividad=id_actividad,
                                                          fh_registro=fh_registro).first()
        # print(id_actividad)
        if id_actividad == 'ORDEN':
            try:
                _orden = Desc_Orden.objects.filter(orden_trabajo=ref_actividad)[0]

            except:
                datetimeobject = datetime.strptime(actividad.fh_registro, '%Y%m%d%H%M%S')

                datos = {

                    'fh_inicio': datetimeobject,
                    'fh_fin': datetimeobject,
                }
                _orden = datos

            context['orden'] = _orden
            _lect = Desc_Lectura.objects.filter(orden_trabajo=ref_actividad)

            context['lecturas'] = _lect
            _anom = Desc_Anomalia.objects.filter(orden_trabajo=ref_actividad).order_by('prioridad')

            context['anomalias'] = _anom
            lecturas = []
            for lect in _lect:
                anom = ''
                if _anom:
                    anom = _anom[0]

                datos = {
                    'marca': lect.marca,
                    'numero_serie': lect.num_serie,
                    'lectura': lect.lectura,
                    'consumo': lect.consumo,
                    'anomalia': anom
                }
                lecturas.append(datos)

            context['lecturas'] = lecturas

        context['actividad'] = actividad
        context['secuencia'] = secuencia
        if true_or_false(aprox):
            context['aprox'] = actividad.get_address();
        else:
            context['aprox'] = 'S/D'

        return render_to_response('gps/recorrido/data_act.html', context)
    except Exception as e:
        log.error("ERROR: {}".format(e))
        return HttpResponse(status=500)


###### ------------------------- CLIENTES -------------------------------------- ######
@login_required(login_url=settings.LOGIN_PAGE)
def clientes_main(request):
    context = RequestContext(request)
    # print("clientes main")
    return render_to_response('data_admin/clientes/_clientes.html', context)


@login_required(login_url=settings.LOGIN_PAGE)
def buscar_cliente(request):
    context = RequestContext(request)
    # print("buscar cliente")
    try:

        punto_suministro = request.POST['nis']
        num_contrato = request.POST['nic']
        if punto_suministro:
            sumin = PuntoDeSuministro.objects.get(punto_suministro=punto_suministro)
        elif num_contrato:
            sumin = PuntoDeSuministro.objects.get(num_contrato=num_contrato)
        if sumin.cliente == None:
            return HttpResponse(status=302)

        cliente = sumin.cliente
        form = clienteForm(instance=cliente)
        context['codigo'] = cliente.codigo
        context['sumin'] = sumin
        context['form'] = form
        context['contactos'] = ContactoCliente.objects.filter(cliente=cliente)

        return render_to_response('data_admin/clientes/_datos_cliente.html', context)
    except ObjectDoesNotExist:
        print("no existe")
        return HttpResponse(status=301)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)

    return render_to_response('data_admin/clientes/_clientes.html', context)


@login_required(login_url=settings.LOGIN_PAGE)
def cliente_save(request):
    context = RequestContext(request)

    try:
        # print("ENTRO Cliente_SAVE")
        codigo = request.POST['codigo']
        cliente = Cliente.objects.get(codigo=codigo)

        form = clienteForm(request.POST, instance=cliente)
        # print(form['estado_cliente'].value())

        if form.is_valid():
            form.save()
            writeAudit("Cliente", "edicion", request.user, form.cleaned_data)
            return HttpResponse("Datos grabados correctamente", status=200)
        # print('Form no valido')
        # print(form.errors.as_json())
        return HttpResponse(status=500)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def contacto_edit(request):
    try:
        context = RequestContext(request)
        # print("ENTRO contacto_EDIT")
        id = request.POST['id']
        # print(id)
        contacto = ContactoCliente.objects.get(id=id)
        context['contacto'] = contacto
        form = contactoForm(instance=contacto)
        context['form'] = form
        return render_to_response('data_admin/clientes/_contactos_edit.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def contacto_new(request):
    try:
        context = RequestContext(request)
        # print("ENTRO contacto_NEW")
        client = request.POST['cliente']
        # print(client)
        cliente = Cliente.objects.get(codigo=client)
        form = contactoForm(initial={'cliente': cliente})
        context['form'] = form
        return render_to_response('data_admin/clientes/_contactos_edit.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


def contacto_delete(request):
    context = RequestContext(request)

    try:
        id = request.POST['id']
        # print("Id "+id)
        contacto = ContactoCliente.objects.get(id=id)
        cliente = contacto.cliente
        # print(cliente)
        contacto.delete()
        contactos = ContactoCliente.objects.filter(cliente=cliente)

        context['contactos'] = contactos
        form = contactoForm(initial={'cliente': cliente})
        context['form'] = form

        return render_to_response('data_admin/clientes/_table_contactos.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


def contacto_save(request):
    context = RequestContext(request)

    try:
        # print("ENTRO contacto_SAVE")

        accion = request.POST['accion']
        # print(accion)

        if accion == 'edit':
            id = request.POST['id']
            # print("Id "+id)
            contacto = ContactoCliente.objects.get(id=id)

            form = contactoForm(request.POST, instance=contacto)

            if form.is_valid():
                form.save()
                writeAudit("contactos", "editar", request.user, form.cleaned_data)

                cliente = form.cleaned_data['cliente']
                contactos = ContactoCliente.objects.filter(cliente=cliente)

                context['contactos'] = contactos

                context['form'] = form
                # return HttpResponse("getPage('{% url 'qorder:atp_main' %}')")
                return render_to_response('data_admin/clientes/_table_contactos.html', context)
            # print('Form no valido')
            # print(form.errors.as_json())
        else:

            form = contactoForm(request.POST)

            if form.is_valid():
                # print("form is valid")
                new_contacto = form.save()
                writeAudit("contactos", "nuevo", request.user, form.cleaned_data)
                cliente = form.cleaned_data['cliente']
                contactos = ContactoCliente.objects.filter(cliente=cliente)
                context['contactos'] = contactos
                context['form'] = form
                # return HttpResponse("getPage('{% url 'qorder:atp_main' %}')")

                return render_to_response('data_admin/clientes/_table_contactos.html', context)
            # print('Form no valido')
            # print(form.errors.as_json())
            return HttpResponse('Complete los campos obligatorios', status=301)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)
    form = contactoForm(initial={'cliente': cliente})
    context['contactos'] = contactos
    context['form'] = form

    return render_to_response('data_admin/clientes/_contactos_edit.html', context)


###### ------------------------- REVISION -------------------------------------- ######
@login_required(login_url=settings.LOGIN_PAGE)
def revision_main(request):
    context = RequestContext(request)
    # print("revision main")
    try:
        context = RequestContext(request)
        activa_revision = ''
        try:
            activa_revision = Parametro.objects.get(parametro='P_ACTIVA_REVISION')
            if activa_revision.valor_1 == '0':
                activa_revision = ''
            else:
                activa_revision = '1'
        except:
            print('No tiene revision activa')
        # print(activa_revision)
        context['revision_activada'] = activa_revision
        # print('Datos suministro')

        numero_orden = request.POST['numero_orden']
        # print(numero_orden)
        if numero_orden:
            orden = OrdenDeTrabajo.objects.get(numero_orden=numero_orden)

            sumin = orden.punto_suministro
            aparato = sumin.aparato
            # print("Sumin {}".format(sumin))
            # print(orden)
            context['sumin'] = sumin
            context['orden'] = orden
            context['aparato'] = aparato
            context['contactos'] = ContactoCliente.objects.filter(cliente=sumin.cliente)
            # print("Antes Desc_ORden")
            _orden = Desc_Orden.objects.get(orden_trabajo=numero_orden)
            _consumo = Consumo.objects.filter(aparato=sumin.aparato)
            # print('_consumo {}'.format(_consumo))
            # print("Despues Desc_ORden {}".format(_orden))
            context['lecturista'] = _orden.tecnico
            context['fecha'] = _orden.fh_fin
            context['tope_inferior'] = _consumo[0].tope_lectura_minima
            context['tope_superior'] = _consumo[0].tope_lectura_maxima
            context['lectura_anterior'] = _consumo[0].lectura_anterior
            context['consumo_anterior'] = _consumo[0].consumo_anterior
            context['fecha_anterior'] = _consumo[0].fecha_lectura_anterior
            context['secuencia_real'] = _orden.secuencia_real
            # print('Orden {}'.format(_orden))
            # print('fecha_lectura_anterior {}'.format(_consumo[0].fecha_lectura_anterior))
            _lect = Desc_Lectura.objects.filter(orden_trabajo=numero_orden)
            # print('Lecturas {}'.format(len(_lect)))
            # print(str(_lect))
            context['lecturas'] = _lect
            _anom = Desc_Anomalia.objects.filter(orden_trabajo=numero_orden)
            tt_anom = Anomalia.objects.filter(activo=1).exclude(id_anomalia='ANREV')
            # print('Anomalias {}'.format(len(_anom)))
            # print(_anom)
            context['anomalias'] = _anom
            # print(_orden.oficina)
            _oficina = WorkUnit.objects.get(id_workunit=_orden.oficina.id_workunit)
            # print(_oficina.coords)
            context['center'] = _oficina.getHashmap()
            # context['center'] = getHashmap()
            _foto = Desc_Foto.objects.filter(orden_trabajo=numero_orden)
            # print('{}'.format(len(_foto)))
            context['fotos'] = _foto
            historicocsmo = HistoricoConsumo.objects.filter(consumo=_consumo)
            context['desc_orden'] = _orden
            context['consumos_anteriores'] = historicocsmo
            context['anomalia'] = tt_anom
            context['periodos'] = historicocsmo
            context['consumos'] = historicocsmo
            # print('llega')
        return render_to_response('ordenes/revision/_revision.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)

    return render_to_response('ordenes/revision/_revision.html', context)


@login_required(login_url=settings.LOGIN_PAGE)
def corregir_lectura(request):
    return HttpResponse(status=200)


def setBit(int_type, offset):
    mask = 1 << offset
    return (int_type | mask)


@login_required(login_url=settings.LOGIN_PAGE)
def confirmar_lectura(request):
    context = RequestContext(request)
    numero_orden = request.POST['numero_orden']
    lectura = request.POST['lectura']
    orden = OrdenDeTrabajo.objects.get(pk=numero_orden)
    # hacer save del estado
    # print(orden.estado)
    # print(int('100000000', 2))
    nuevo = setBit(orden.estado, 8)
    orden.estado = nuevo
    orden.save()

    writeAudit("Revisión", "revisión", request.user, 'Confirmó lectura {} orden {}'.format(lectura, numero_orden))
    return HttpResponse(status=200)


@login_required(login_url=settings.LOGIN_PAGE)
def corregir_lectura(request):
    context = RequestContext(request)
    numero_orden = request.POST['numero_orden']
    lectura = request.POST['lectura']
    # print(lectura)
    lectura_nueva = request.POST['lectura_nueva']
    consumo = request.POST['consumo']

    try:

        # Si ya existe una corrección

        if Desc_Anomalia.objects.filter(orden_trabajo=numero_orden,
                                        id_anomalia=Anomalia.objects.get(id_anomalia='ANREV')).exists():

            orden = OrdenDeTrabajo.objects.get(numero_orden=numero_orden)

            nuevo = setBit(orden.estado, 8)

            orden.estado = nuevo

            orden.save()

            _lectura = Desc_Lectura.objects.get(orden_trabajo=numero_orden)

            _lectura.lectura = lectura_nueva

            _lectura.consumo = consumo

            _lectura.save()

            _orden = Desc_Orden.objects.get(orden_trabajo=numero_orden)

            _orden.orden_modificada = 1

            _orden.fh_modificacion = datetime.now()

            _orden.usuario_modifico = str(request.user)

            _orden.save()

            _anom = Desc_Anomalia.objects.get(orden_trabajo=numero_orden,
                                              id_anomalia=Anomalia.objects.get(id_anomalia='ANREV'))

            _anom.id_descarga = _orden.id_descarga

            _anom.orden_trabajo = _orden.orden_trabajo

            _anom.id_anomalia = Anomalia.objects.get(id_anomalia='ANREV')

            _anom.id_observacion = None

            _anom.fecha_hora_registro = datetime.now()

            _anom.paso_accion = None

            _anom.oficina = _orden.oficina

            _anom.save()

            historicocsmo = HistoricoConsumo.objects.get(consumo=orden.consumo.consumo, lectura=lectura)

            historicocsmo.lectura = lectura_nueva

            historicocsmo.valor_consumo = consumo

            historicocsmo.save()

        else:

            # Si no existe una corrección anterior

            orden = OrdenDeTrabajo.objects.get(numero_orden=numero_orden)

            nuevo = setBit(orden.estado, 8)

            orden.estado = nuevo

            orden.save()

            _lectura = Desc_Lectura.objects.get(orden_trabajo=numero_orden)

            _lectura.lectura = lectura_nueva

            _lectura.consumo = consumo

            _lectura.save()

            _orden = Desc_Orden.objects.get(orden_trabajo=numero_orden)

            _orden.orden_modificada = 1

            _orden.fh_modificacion = datetime.now()

            _orden.usuario_modifico = str(request.user)

            _orden.save()

            _anom = Desc_Anomalia.objects.create(id_descarga=_orden.id_descarga,
                                                 orden_trabajo=_orden.orden_trabajo,
                                                 id_anomalia=Anomalia.objects.get(id_anomalia='ANREV'),
                                                 id_observacion=None,
                                                 fecha_hora_registro=datetime.now(),
                                                 paso_accion=None,
                                                 oficina=_orden.oficina)
            _anom.save()

            historicocsmo = HistoricoConsumo.objects.get(consumo=orden.consumo.consumo, lectura=lectura)

            historicocsmo.lectura = lectura_nueva

            historicocsmo.valor_consumo = consumo

            historicocsmo.save()

        # Guardamos el log

        writeAudit("Revisión", "revisión", request.user,
                   'Cambió la lectura {} por {} orden {}'.format(lectura, lectura_nueva, numero_orden))

        return HttpResponse(status=200)

    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
@csrf_exempt
def get_desc_anom(request):
    context = RequestContext(request)
    anomalia = request.POST['anomalia']
    try:

        obt_desc = Anomalia.objects.get(id_anomalia=anomalia)
        _jsonres = json.dumps({'descripcion': str(obt_desc.descripcion)})
        print(_jsonres)
        return HttpResponse(_jsonres, content_type='application/json', status=200)
    except Exception as e:
        log.error('Error {}'.format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def confirmar_anom(request):
    context = RequestContext(request)
    numero_orden = request.POST['numero_orden']
    anom = request.POST['nuevaanom']
    orden = OrdenDeTrabajo.objects.get(pk=numero_orden)
    # hacer save del estado
    # print(orden.estado)
    # print(int('100000000', 2))
    nuevo = setBit(orden.estado, 8)
    orden.estado = nuevo
    orden.save()

    writeAudit("Revisión", "revisión", request.user, 'Confirmó lectura {} orden {}'.format(lectura, numero_orden))
    return HttpResponse(status=200)


@login_required(login_url=settings.LOGIN_PAGE)
@csrf_exempt
def deleteanom(request):
    context = RequestContext(request)
    anomalia = request.POST['anomalia']
    orden = request.POST['numero_orden']

    if anomalia == 'ANREV':
        return HttpResponse(status=300)
    else:
        anomalias = Desc_Anomalia.objects.filter(orden_trabajo=orden, id_anomalia=anomalia).delete()
        return HttpResponse(status=200)


@login_required(login_url=settings.LOGIN_PAGE)
@csrf_exempt
def updateanom(request):
    context = RequestContext(request)
    anomalia = request.POST['anomalia']
    orden = request.POST['numero_orden']
    comentario = request.POST['coment']
    descripcion = request.POST['desc']

    if anomalia == 'ANREV':
        return HttpResponse(status=300)
    else:

        anomalias = Desc_Anomalia.objects.filter(orden_trabajo=orden, id_anomalia=anomalia).update(
            comentario=comentario)

        return HttpResponse(status=200)


@login_required(login_url=settings.LOGIN_PAGE)
@csrf_exempt
def addanomalia(request):
    context = RequestContext(request)
    anomalia = request.POST['anomalia']
    orden = request.POST['numero_orden']
    comentario = request.POST['coment']

    anomalias = Desc_Anomalia.objects.filter(orden_trabajo=orden, id_anomalia=anomalia)
    ord = OrdenDeTrabajo.objects.select_related('ruta').values('ruta__oficina').get(numero_orden=orden)
    if len(anomalias) > 0:
        return HttpResponse(status=300)

    else:
        anom = Anomalia.objects.get(id_anomalia=anomalia)
        print(anom.tipo_resultado)
        anom = Desc_Anomalia.objects.create(id_descarga=orden,
                                            orden_trabajo_id=orden,
                                            id_anomalia_id=anomalia,
                                            id_observacion=None,
                                            fecha_hora_registro=datetime.now(),
                                            paso_accion=None,
                                            oficina_id=ord['ruta__oficina'],
                                            tipo_resultado_id=anom.tipo_resultado_id,
                                            prioridad=anom.prioridad,
                                            comentario=comentario)

    return HttpResponse(status=200)


###### ------------------------- GEOFENCING -------------------------------------- ######
@login_required(login_url=settings.LOGIN_PAGE)
def geofencing_main(request):
    context = RequestContext(request)
    # print("geofencing main")
    return render_to_response('data_admin/geofencing/_geofencing.html', context)


@csrf_exempt
def geofencing_list(request):
    try:
        context = RequestContext(request)
        id_centro = request.POST['id_centro']
        geof = Geofencing.objects.filter(oficina=id_centro)

        context['geof'] = geof

        return render_to_response('data_admin/geofencing/_table_geofencing.html', context)
    except Exception as e:
        log.error('Error {}'.format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def geofencing_new(request):
    try:
        context = RequestContext(request)
        # print("ENTRO geofencing_NEW")
        form = geofencingForm()
        context['form'] = form

        return render_to_response('data_admin/geofencing/_geofencing_edit.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def geofencing_edit(request):
    try:
        context = RequestContext(request)
        # print("ENTRO geofencing_edit")
        id = request.POST['id_geofencing']

        geofencing = Geofencing.objects.get(id=id)
        # print(geofencing)
        form = geofencingForm(instance=geofencing)
        context['geof'] = geofencing
        context['form'] = form
        return render_to_response('data_admin/geofencing/_geofencing_edit.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def geofencing_save(request):
    context = RequestContext(request)

    try:
        # print("ENTRO geofencing_SAVE")
        id = request.POST['id_geofencing']
        accion = request.POST['accion']
        # print("Id "+id)

        if accion == 'edit':
            geofencing = Geofencing.objects.get(id=id)

            form = geofencingForm(request.POST, instance=geofencing)

            if form.is_valid():
                form.save(commit=False)
                oficina = request.POST['id_oficinah']
                # print("Oficina "+oficina)
                form.oficina = oficina

                form.save()
                writeAudit("geofencing", "edicion", request.user, form.cleaned_data)
                # grabar la relacion con oficina si cambió

                geofencing = Geofencing.objects.filter(oficina=oficina)

                context['geof'] = geofencing

                context['form'] = form
                # return HttpResponse("getPage('{% url 'qorder:atp_main' %}')")
                return render_to_response('data_admin/geofencing/_table_geofencing.html', context)
            # print('Form no valido')
            # print(form.errors.as_json())
        else:

            form = geofencingForm(request.POST)

            if form.is_valid():
                # print("form is valid")
                geof = form.save(commit=False)
                oficina = WorkUnit.objects.get(pk=request.POST['id_oficinah'])

                geof.oficina = oficina
                geof.activo = 1
                # print(geof)
                geof.save()
                writeAudit("geofencing", "nueva", request.user, form.cleaned_data)

                geofencing = Geofencing.objects.filter(oficina=oficina)

                context['geof'] = geofencing
                return render_to_response('data_admin/geofencing/_table_geofencing.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)

    context['geof'] = geofencing
    context['form'] = form
    return render_to_response('data_admin/geofencing/_geofencing_edit.html', context)


@login_required(login_url=settings.LOGIN_PAGE)
def geofencing_detail(request):
    context = RequestContext(request)
    id = request.POST['id_geofencing']
    try:
        geofencing = Geofencing.objects.get(id=id)
        id_centro = request.POST['id_oficina']

        oficina = WorkUnit.objects.get(pk=id_centro)
        context['center'] = oficina.getHashmap()
        listarutas = []
        rutas = Ruta.objects.filter(oficina=oficina, estado__in=STATUS_ENABLED)

        listatecnicos = []
        for tipoPersonal in request.user.tiposPersonal.all():
            listatecnicos.append(tipoPersonal)

        tecnicos_oficina = OficinaXTecnico.objects.filter(oficina=id_centro, fecha_baja=None)
        tecs = []
        for item in tecnicos_oficina:
            tecs.append(item.tecnico.id)
        # print(tecs)
        tecnicos = Tecnico.objects.filter(id__in=tecs)

        tec = []
        rut = []

        for tecnico in tecnicos:
            tecxgeof = GeofencingXTecnico.objects.filter(geofencing=geofencing, tecnico=tecnico)
            tp = ""
            if tecnico.terminal_portatil == None:
                tp = '--'
            else:
                tp = tecnico.terminal_portatil.numero_serie
            if tecxgeof:

                datos_tec = {
                    'codigo': tecnico.codigo,
                    'nombre': tecnico.nombre_1,
                    'apellido': tecnico.apellido_1,
                    'tp': tp,
                    'id': tecnico.id,
                    'activo': 1
                }
            else:
                datos_tec = {
                    'codigo': tecnico.codigo,
                    'nombre': tecnico.nombre_1,
                    'apellido': tecnico.apellido_1,
                    'tp': tp,
                    'id': tecnico.id,
                    'activo': 0
                }

            tec.append(datos_tec)

        for ruta in rutas:
            rutaxgeof = GeofencingXRuta.objects.filter(geofencing=geofencing, ruta=ruta)
            if rutaxgeof:
                datos_rut = {
                    'oficina': ruta.oficina,
                    'ciclo': ruta.ciclo,
                    'ruta': ruta.ruta,
                    'itinerario': ruta.itinerario,
                    'id': ruta.id,
                    'activo': 1
                }
            else:
                datos_rut = {
                    'oficina': ruta.oficina,
                    'ciclo': ruta.ciclo,
                    'ruta': ruta.ruta,
                    'itinerario': ruta.itinerario,
                    'id': ruta.id,
                    'activo': 1
                }

            rut.append(datos_rut)
        geofencingdetail = GeofencingDetalle.objects.filter(geofencing=geofencing)

        if geofencingdetail:
            context['form'] = geofencingDetalleForm(instance=geofencingdetail[0])

            context['geofdetalle'] = geofencingdetail[0]
            if len(geofencingdetail[0].geohash_centro_circulo) > 2:
                context['circle'] = SafeString(geofencingdetail[0].geohash_centro_circulo)
            else:
                context['polygon'] = SafeString(geofencingdetail[0].composicion_area)
        else:
            context['form'] = geofencingDetalleForm()
            context['geofdetalle'] = []
            context['circulo'] = ''

        context['rutas'] = rut
        context['tecnicos'] = tec

        context['geofencing'] = geofencing
        return render_to_response('data_admin/geofencing/_configgeo.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def geofencing_savedetail(request):
    context = RequestContext(request)

    try:
        print("ENTRO geofencingdetail_SAVE")
        id = request.POST['id_geofencing']
        tecnicos_geof = eval(request.POST['ids_tecnicos'])
        rutas_geof = eval(request.POST['ids_rutas'])
        circle = request.POST['circle']
        polygon = request.POST['polygon']
        geohash_centro_mapa = request.POST['center']
        zoom = request.POST['zoom']
        valor = request.POST['entrada']

        aver = valor.split("&")

        valores = {}
        for item in aver:
            it = item.split("=")
            if len(it) > 1:
                valores[it[0]] = it[1]
            else:
                valores[it[0]] = None
        try:
            if valores['notifica_email_ingreso']:
                valores['notifica_email_ingreso'] = 1
        except:
            valores['notifica_email_ingreso'] = 0
        try:
            if valores['notifica_email_egreso']:
                valores['notifica_email_egreso'] = 1
        except:
            valores['notifica_email_egreso'] = 0
        try:
            if valores['notifica_pantalla_ingreso']:
                valores['notifica_pantalla_ingreso'] = 1
        except:
            valores['notifica_pantalla_ingreso'] = 0
        try:
            if valores['notifica_pantalla_egreso']:
                valores['notifica_pantalla_egreso'] = 1
        except:
            valores['notifica_pantalla_egreso'] = 0
        try:
            if valores['notifica_sonido_ingreso']:
                valores['notifica_sonido_ingreso'] = 1
        except:
            valores['notifica_sonido_ingreso'] = 0
        try:
            if valores['notifica_sonido_egreso']:
                valores['notifica_sonido_egreso'] = 1
        except:
            valores['notifica_sonido_egreso'] = 0
        try:
            if valores['notifica_ws_ingreso']:
                valores['notifica_ws_ingreso'] = 1
        except:
            valores['notifica_ws_ingreso'] = 0
        try:
            if valores['notifica_ws_egreso']:
                valores['notifica_ws_egreso'] = 1
        except:
            valores['notifica_ws_egreso'] = 0

        valores['id_actividad_ingreso'] = None
        valores['id_actividad_egreso'] = None
        # print("Valores {}".format(valores))

        geofencing = Geofencing.objects.get(id=id)

        radio_circulo = None
        geohash_centro_circulo = None
        composicion_area = None
        print(circle)
        if circle:
            geohash_centro_circulo = circle

        if polygon:
            composicion_area = polygon

        # print(composicion_area)

        try:
            geofencingdetail = GeofencingDetalle.objects.get(geofencing=geofencing).delete()
        except GeofencingDetalle.DoesNotExist:
            geofencingdetail = None

        try:
            GeofencingXTecnico.objects.filter(geofencing=geofencing).delete()
        except Exception as e:
            print(e)

        try:
            GeofencingXRuta.objects.filter(geofencing=geofencing).delete()
        except Exception as e:
            print(e)

        geofencingdetail = GeofencingDetalle.objects.create(
            geofencing=geofencing,
            radio_circulo=radio_circulo,
            composicion_area=composicion_area,
            geohash_centro_circulo=geohash_centro_circulo,
            geohash_centro_mapa=geohash_centro_mapa,
            zoom_mapa=zoom,

            notifica_email_ingreso=valores['notifica_email_ingreso'],
            notifica_email_egreso=valores['notifica_email_egreso'],
            notifica_pantalla_ingreso=valores['notifica_pantalla_ingreso'],
            notifica_pantalla_egreso=valores['notifica_pantalla_egreso'],
            notifica_sonido_ingreso=valores['notifica_sonido_ingreso'],
            notifica_sonido_egreso=valores['notifica_sonido_egreso'],
            notifica_ws_ingreso=valores['notifica_ws_ingreso'],
            notifica_ws_egreso=valores['notifica_ws_egreso'],

            emails_ingreso=urllib.parse.unquote(valores['emails_ingreso']),
            emails_egreso=urllib.parse.unquote(valores['emails_egreso']),
            mensaje_email_ingreso=valores['mensaje_email_ingreso'],
            mensaje_email_egreso=valores['mensaje_email_egreso'],
            mensaje_pantalla_ingreso=valores['mensaje_pantalla_ingreso'],
            mensaje_pantalla_egreso=valores['mensaje_pantalla_egreso'],
            mensaje_ws_ingreso=valores['mensaje_ws_ingreso'],
            mensaje_ws_egreso=valores['mensaje_ws_egreso'],
            id_actividad_ingreso=valores['id_actividad_ingreso'],
            id_actividad_egreso=valores['id_actividad_egreso']
        )
        geofencingdetail.save()
        writeAudit("geofencing", "detalle", request.user, '{}'.format(geofencingdetail))
        if tecnicos_geof:
            # print('Grabando tecnicos')
            # print(tecnicos_geof)
            tecnicos = Tecnico.objects.filter(id__in=tecnicos_geof)
            # print(tecnicos)
            for tecnico in tecnicos:
                tecxgeof = GeofencingXTecnico.objects.create(
                    tecnico=tecnico,
                    geofencing=geofencing,
                    fecha_asignacion=date.today())
                tecxgeof.save()
        if rutas_geof:
            # print('Grabando rutas')
            rutas = Ruta.objects.filter(id__in=rutas_geof)
            # print(rutas)
            for ruta in rutas:
                rutxgeof = GeofencingXRuta.objects.create(
                    ruta=ruta,
                    geofencing=geofencing,
                    fecha_asignacion=date.today())
                rutxgeof.save()
        return HttpResponse(status=200)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


def geofencing_cflags(request):
    context = RequestContext(request)
    try:
        context['form'] = geofencingForm()
        # print(request.user)
        id = request.POST['id']
        # print(id)
        name = request.POST['name']
        # print(name)
        action = request.POST['action']
        # print(action)

        geofencing = Geofencing.objects.get(id=id)
        if name == 'enable':
            geofencing.enable(action)
            return JsonResponse({"activo": str(geofencing.activo)})

    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)
    return HttpResponse(status=300)


###### ------------------------- INTERFAZ EXPORTACION LOG  ------------------------- ######

_fileName = ""
_logfileName = ""

# string del log a retornar
_slogfinal = ""
_spath_log = ""
dato = ''
_file = ''


def generarCabeceraLog(_log):
    _log.info('******************************************')
    _log.info('       Qorder Exportación - V1.0          ')
    _log.info('Proceso iniciado: {}'.format(datetime.today().strftime('%d/%m/%Y %H:%M')))
    _log.info('******************************************')


def getLoggingFileData(filename):
    _file = open(filename, 'r')
    str1 = _file.read()
    # lines = _file.readlines(
    _file.close()

    return str1


def getLoggerFileName(self):
    # print('entra logname')
    logfileName = '{}.txt'.format(datetime.today().strftime('%Y%m%d_%H%M%S'))
    return logfileName


def generarPieLog(_log):
    _log.info('******************************************')
    _log.info('Proceso finalizado: {}'.format(datetime.today().strftime('%d/%m/%Y %H:%M')))
    _log.info('******************************************')


def cerrarLog(_log):
    print('llega a cerrar')
    _handlers = _log.handlers[:]

    for h in _handlers:
        h.close()
        _log.removeHandler(h)


def log():
    _log = logging.getLogger('ImportExport')
    _fileName = getLoggerFileName1('IMP', oficina)
    _logfileName = _spath_log + _fileName
    # print(_logfileName)
    _log.setLevel(logging.INFO)
    handler = logging.FileHandler(filename=_logfileName)
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        fmt='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    _log.addHandler(handler)
    # FIN CREACION LOGGER
    return _log


@login_required(login_url=settings.LOGIN_PAGE)
def exportacion(request):
    context = RequestContext(request)
    try:
        semana = SemanaXUser.objects.get(usuario=request.user)
        context['semana'] = semana
    except:
        pass
    return render_to_response('interfaz/exportar/_export.html', context)


@login_required(login_url=settings.LOGIN_PAGE)
def tables_routes(request):
    try:
        ruta_oficina = []
        rutas_sin_trabajar = []
        _lst_rutas = []
        context = RequestContext(request)
        id_centro = request.POST['id_oficina']
        semana = request.POST['semana']
        checkselect = request.POST['selectexport']
        # print(id_centro)
        # print(checkselect)
        centro = WorkUnit.objects.get(pk=id_centro)
        semana_filter = {} if semana == 'TODAS' or semana == '' else {'anio__exact': semana}
        if checkselect == 'true':

            # ruta_oficina = Ruta.objects.filter(oficina=id_centro, estado=777).filter(**semana_filter)

            ruta_oficina = Ruta.objects.filter(oficina=id_centro).filter(**semana_filter)

            for _ruta in ruta_oficina:

                cant_ordenes = OrdenDeTrabajo.objects.filter(ruta=_ruta,estado__in=[265,777]).count()

                if cant_ordenes > 0:

                    _lst_rutas.append(_ruta)

        # print(ruta_oficina)

        elif checkselect == 'false':
            # print('entra')
            # rutas_oficina = Ruta.objects.filter(oficina=id_centro, estado=265).filter(
            #     **semana_filter) | Ruta.objects.filter(oficina=id_centro, estado__in=[265, 273, 401]).filter(
            #     **semana_filter) | Ruta.objects.filter(oficina=id_centro, estado=33, cantidad_leido__gt=0).filter(
            #     **semana_filter) | Ruta.objects.filter(oficina=id_centro, estado=7, cantidad_leido__gt=0).filter(
            #     **semana_filter)

            rutas_oficina = Ruta.objects.filter(oficina=id_centro).filter(**semana_filter)

            for _ruta in rutas_oficina:

                cant_ordenes = OrdenDeTrabajo.objects.filter(ruta=_ruta,estado=265).count()

                if cant_ordenes > 0:

                    _lst_rutas.append(_ruta)

                # print(rutas)
                # ruta = Ruta.objects.get(oficina=id_centro, idruta=rutas.idruta)
                # if ruta.estado == 265:
                #     ruta_oficina.append(ruta)
                # elif ruta.estado == 7 or ruta.estado == 33:
                #     ruta_oficina.append(ruta)

        # context['rutas'] = ruta_oficina

        context['rutas'] = _lst_rutas

        return render_to_response('interfaz/exportar/table_export.html', context)

    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


def make_export(request):
    # print(request.POST['id_centro'])
    # print(test(request.POST['id_centro']))
    str1 = exportar(request.POST['id_centro'], request.user)
    return HttpResponse(str1.replace('\n', '<br/>').replace('\r', '<br/>'), status=200)


def result_exportacion(request):
    try:

        # print('Obteniendo parametros de directorio log')

        _param = Parametro.objects.get(pk='P_PATH_LOG_IMP_EXP')
        _spath_log = _param.valor_1

        print('P_PATH_LOG_IMP_EXP: ' + _spath_log)

    except Exception as errOf:
        print('Ocurrió un error al obtener parametros de configuración de path log: {}'.format(errOf))

        _spath_log = ".//defLog//"

    lista_resultado = []
    # CREACION DEL LOGGER
    _log = logging.getLogger('ImportExport')
    _fileName = getLoggerFileName('IMP')
    _logfileName = _spath_log + _fileName

    _log.setLevel(logging.INFO)
    handler = logging.FileHandler(filename=_logfileName)
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        fmt='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    _log.addHandler(handler)
    # FIN CREACION LOGGER
    generarCabeceraLog(_log)

    ###### ------------------------- INTERFAZ EXPORTACION  ------------------------- ######

    try:
        context = RequestContext(request)
        id_oficina = request.POST['id_centro']
        checkexportadas = request.POST['selectexport']
        rutas_json = request.POST.get('rutas', None)
        if rutas_json:
            rutas_ciclos_list = json.loads(rutas_json)

        hora = ''
        fecha = ''
        strsuministros = ''
        Codanom = ''
        itinerario = ''
        nota = ''
        total_ordenes = 0
        DataList = []
        strsuministro = ''
        Comentarios = ''
        reescribir = []
        lst_objetos_rutas_export = []
        list_suministros_export = []

        oficina = WorkUnit.objects.get(id_workunit=id_oficina)
        _log.info('Contratista: {}'.format(oficina.name))
        if rutapath(request, id_oficina, _log) == False:
            generarPieLog(_log)
            _slogfinal = str(getLoggingFileData(_logfileName))
            cerrarLog(_log)
            return HttpResponse(_slogfinal.replace('\n', '<br/>').replace('\r', '<br/>'), status=200)
        listaruta = []
        confruta = ConfigParamsImpExp.objects.get(oficina=oficina)
        _ruta1 = str(confruta.path_txt_export).strip(' ')

        anom = ''
        # rutas = rutas.replace('[', '').replace(']', '').rstrip(',').replace("'", "").split(',')
        # print('ruta {}'.format(rutas))

        rutas_list = [ruta_ciclo['ruta'] for ruta_ciclo in rutas_ciclos_list]
        ciclos_list = [ruta_ciclo['ciclo'] for ruta_ciclo in rutas_ciclos_list]
        rutaselec = Ruta.objects.filter(idruta__in=rutas_list,ciclo__in=ciclos_list).values('estado', 'ruta', 'fecha_hora_exportacion', 'idruta',
                                                                 'ciclo', 'anio', 'cantidad_leido')
        try:
            for ruta_ciclo in rutaselec:
                try:
                    with transaction.atomic():

                        r = next((ruta for ruta in rutaselec if ruta['ruta'] == ruta_ciclo['ruta'] and ruta['ciclo'] == ruta_ciclo['ciclo']), None)

                        _parametro_sp = []

                        ordenes = []

                        objeto_ruta = {}

                        cod_unicom = str(id_oficina)
                        rutaexp = r['ruta']
                        anio = r['anio']
                        ciclo = r['ciclo']

                        objeto_ruta['id_ruta'] = rutaexp

                        cantidad_ordenes = 0

                        _log.info('--------------------')
                        _log.info('Iniciando la exportación de la ruta n° : {}'.format(r['ruta']))

                        
                        if r['estado'] == 265:

                            _log.info('Ruta Exportada Completa')

                            estados = "265,273,401"


                        elif r['estado'] == 7:
                            
                            _log.info('Ruta Parcialmente Exportada')

                            if checkexportadas == 'true':

                                estados = "265,777"

                            else:

                                estados = "265"

                        elif r['estado'] == 33:

                            _log.info('Ruta Parcialmente Exportada')

                            if checkexportadas == 'true':

                                estados = "265,777"

                            else:

                                estados = "265"


                        elif r['estado'] == 777:

                            _log.info('Ruta reexportada')

                            estados = "777"

                        else:
                            raise Exception('La ruta tiene un estado incorrecto para su exportación, estado = {}'.format(r['estado']))


                        _parametro_sp = (oficina.pk, r['ruta'], r['anio'], r['ciclo'], estados)

                        with connection.cursor() as cursor:

                            cursor.callproc('sp_export_ruta', _parametro_sp)

                            ordenes = cursor.fetchall()
                                                                    
                        cantidad_ordenes = len(ordenes)
                        total_ordenes = total_ordenes + cantidad_ordenes

                        if cantidad_ordenes > 0:
                            ordenes_ids = [orden[0] for orden in ordenes]                 
                            ordenes_datos = [orden[1] for orden in ordenes]

                        objeto_ruta['datos_ordenes'] = ordenes_datos

                        OrdenDeTrabajo.objects.filter(numero_orden__in=ordenes_ids).update(estado=777, fecha_hora_exportacion=datetime.now().strftime('%Y%m%d%H%M%S'))

                        if r['estado'] == 265:
                            ruta = Ruta.objects.filter(idruta=r['idruta']).values('idruta', 'estado').update(estado=777,
                                                                                                            fecha_hora_exportacion=datetime.now().strftime(
                                                                                                                '%Y%m%d%H%M%S'))
                            log_rutas.objects.create(estado='Exportación', fecha_log=datetime.now(), ruta_id=r['idruta'],
                                                    usuario=request.user)
                        elif r['estado'] == 7:
                            log_rutas.objects.create(estado='Exportación', fecha_log=datetime.now(), ruta_id=r['idruta'],
                                                    usuario=request.user)

                        elif r['estado'] == 33:
                            log_rutas.objects.create(estado='Exportación', fecha_log=datetime.now(), ruta_id=r['idruta'],
                                                    usuario=request.user)

                        else:

                            log_rutas.objects.create(estado='Exportación_anomala_{}'.format(r['estado']), fecha_log=datetime.now(), ruta_id=r['idruta'],
                                                    usuario=request.user)

                        lst_objetos_rutas_export.append(objeto_ruta)

                        _log.info('Plan: {}'.format(itinerario))
                        _log.info('Zona: {}'.format(ciclo))

                        _log.info('Semana: {}'.format(anio))

                        _log.info('Suministros Exportados: {}'.format(str(cantidad_ordenes)))


                except Exception as e:
                    _log.error('Error en el proceso de exportación de la ruta: {}'.format(e))
                    _log.error("Se revertiran los cambios de esta ruta aplicados a la base de datos")
                    total_ordenes = total_ordenes - cantidad_ordenes
                    transaction.rollback()

            for objeto_ruta_export in lst_objetos_rutas_export:

                datos_ordenes = [orden for orden in objeto_ruta_export['datos_ordenes']]

                list_suministros_export.extend(datos_ordenes)
                
        except Exception as e:
            print('ERROR EXPORTACIÓN RECORRIDO RUTAS Y ORDENES Y UPDATES {}'.format(e))
            _log.error(e)

        _log.info('---------------------------------')
        _log.info('Total Suministros Exportados {}'.format(total_ordenes))
        # GENERACIÓN DEL ARCHIVO DE EXPORTACIÓN
        try:
            if oficina.id_workunit == '0001':
                _Name = 'DEV' + oficina.name + '.RLV'
            else:
                _Name = 'DEVRYT.RLV'
            pathruta = _ruta1 + '/'
            if os.path.exists(pathruta):

                files = listdir(pathruta)  # Obtenemos los archivos que contiene la ruta
                if _Name in files:
                    archivo = open(pathruta + _Name, 'r')
                    DataList = archivo.readlines()
                    # print(DataList)

                    DataList = ''.join(DataList)
                    # reescribir.append(DataList + strsuministro)
                    # escribir = ''.join(reescribir)
                    archivo = open(pathruta + _Name, 'w')
                    archivo.write(DataList)
                    for item in list_suministros_export:
                        archivo.write("{}\n".format(item))
                    # print(escribir)
                    archivo.close()
                else:
                    archivo = open(pathruta + _Name, 'w')
                    for item in list_suministros_export:
                        archivo.write("{}\n".format(item))
                    #archivo.write(strsuministro)
                    archivo.close()

            else:
                if not os.path.exists(pathruta):
                    os.makedirs(pathruta)
                archivo = open(pathruta + _Name, 'w')
                for item in list_suministros_export:
                    archivo.write("{}\n".format(item))
                #archivo.write(strsuministro)
                fp.write('\n'.join(names))
                archivo.close()

            # print('estoy aca')
            hasher = hashlib.md5()
            with open(pathruta + _Name, 'rb') as afile:

                buf = afile.read()
                hasher.update(buf)

            bytefile = open(pathruta + 'Control.txt', 'w')
            bytefile.write('md5= ' + hasher.hexdigest())
            bytefile.close()

            generarPieLog(_log)
            _slogfinal = str(getLoggingFileData(_logfileName))
            cerrarLog(_log)
        except Exception as e:
            print('ERROR EXPORTACIÓN GENERACION ARCHIVOS {}').format(e)
            _log.error(e)

        return HttpResponse(_slogfinal.replace('\n', '<br/>').replace('\r', '<br/>'), status=200)
    except Exception as e:
        print('ERROR EXPORTACIÓN GENERAL {}'.format(e))
        _log.error(e)


@csrf_exempt
def archivo_exportacion(request):
    context = RequestContext(request)
    id_oficina = request.POST['id_centro']
    flag = request.POST['flag']
    oficina = WorkUnit.objects.get(id_workunit=id_oficina)
    confruta = ConfigParamsImpExp.objects.get(oficina=id_oficina)
    _ruta1 = str(confruta.path_txt_export).strip(' ')
    name = datetime.today().strftime('%Y%m%d_%H%M%S')
    if oficina.id_workunit == '0001':
        name_file = 'DEV' + oficina.name + '.RLV'
    else:
        name_file = 'DEVRYT.RLV'
    ruta_new = _ruta1 + '/' + name
    if flag == '1':
        search_file = os.path.isfile(_ruta1 + '/' + name_file)
        if search_file == False:
            writeAudit("exportacion", "Exportar", request.user,
                       'No existe el archivo de exportacion {}'.format(name_file))
            return HttpResponse(status=200)
        else:

            os.mkdir(ruta_new)
            shutil.move(_ruta1 + '/' + name_file, ruta_new)
            shutil.move(_ruta1 + '/' + 'Control.txt', ruta_new)
            zip_file = zipfile.ZipFile(ruta_new + '.zip', 'w')
            for folder, subfolders, files in os.walk(ruta_new):

                for file in files:

                    if file.endswith('.txt') or file.endswith('.RLV'):
                        zip_file.write(os.path.join(folder, file),
                                       os.path.relpath(os.path.join(folder, file), ruta_new),
                                       compress_type=zipfile.ZIP_DEFLATED)

            zip_file.close()
            shutil.rmtree(ruta_new)
            writeAudit("exportacion", "Exportar", request.user,
                       'Elimino el archivo de exportacion {}'.format(name_file))
            return HttpResponse(status=200)
    else:
        writeAudit("exportacion", "Exportar", request.user, 'No se elimino archivo exportacion {}'.format(name_file))
        return HttpResponse(status=200)


@csrf_exempt
def send_file(request):
    context = RequestContext(request)
    filenames = []
    files = []
    id_oficina = request.POST['id_centro']
    oficina = WorkUnit.objects.get(id_workunit=id_oficina)
    confruta = ConfigParamsImpExp.objects.get(oficina=id_oficina)
    _ruta1 = str(confruta.path_txt_export).strip(' ')
    if oficina.id_workunit == '0001':
        name_file = 'DEV' + oficina.name + '.RLV'
    else:
        name_file = 'DEVRYT.RLV'
    name_control = 'Control.txt'
    data = {}
    filenames.append(name_file)
    filenames.append(name_control)

    zip_archivo = zipfile.ZipFile((_ruta1 + '/' + name_file) + '.zip', 'w')

    for folder, subfolders, files in os.walk(_ruta1):

        for file in files:
            for filename in filenames:
                if file.endswith(filename):
                    zip_archivo.write(os.path.join(folder, file), os.path.relpath(os.path.join(folder, file), _ruta1),
                                      compress_type=zipfile.ZIP_DEFLATED)
                else:
                    continue
    zip_archivo.close()

    zip_file = open(_ruta1 + '/' + name_file + '.zip', 'rb').read()
    image_64_encode = base64.encodebytes(zip_file)
    data["data"] = image_64_encode.decode('ascii')
    final_data = json.dumps(data)

    # resp = HttpResponse(s.getvalue(), content_type="application/zip")
    # ..and correct content-disposition
    # resp['Content-Disposition'] = 'attachment; filename=%s' % 'file.zip'

    # return resp
    # _jsonres = json.dumps({'zip': zip_file})

    return HttpResponse(final_data, content_type='application/json', status=200)


###### ------------------------- INTERFAZ EXPORTACION ARCHIVO  ------------------------- ######

def rutapath(request, id_oficina, _log):
    # print('entra')
    oficina = id_oficina
    confruta = ConfigParamsImpExp.objects.get(oficina=oficina)
    _ruta1 = str(confruta.path_txt_export).strip(' ')
    if _ruta1 is None or len(_ruta1) == 0:
        _log.info('No está configurado el directorio de Exportación')
        writeAudit("gestion exportacion", "Exportar", request.user, 'No está configurado el directorio de Exportación')
        return False
    else:
        return True


###### ------------------------- INTERFAZ IMPORTACION  ------------------------- ######
@login_required(login_url=settings.LOGIN_PAGE)
def importacion(request):
    context = RequestContext(request)
    return render_to_response('interfaz/importar/_import.html', context)


def make_import(request):
    context = RequestContext(request)
    archivos = ''
    flag_imp = ''
    dia = datetime.now()
    semana = datetime.date(dia).isocalendar()[1]
    strsemana = str(dia.year)[2:4] + str(semana)

    user = request.user
    oficina = request.POST['id_centro']
    listfiles = []
    lista1 = []
    try:
        # print('Obteniendo parametros de directorio log')

        _param = Parametro.objects.get(pk='P_PATH_LOG_IMP_EXP')
        # print(_param)
        _spath_log = _param.valor_1


    except Exception as errOf:
        print('Ocurrió un error al obtener parametros de configuración de path log: {}'.format(errOf))
        _spath_log = ".//defLog//"

    # CREACION DEL LOGGER
    _log = logging.getLogger('ImportExport')
    _fileName = getLoggerFileName1('IMP', oficina)
    _logfileName = _spath_log + _fileName
    try:
        os.remove(_logfileName)
    except OSError:
        pass
    # print(_logfileName)
    _log.setLevel(logging.INFO)
    handler = logging.FileHandler(filename=_logfileName)
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        fmt='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    _log.addHandler(handler)
    # FIN CREACION LOGGER

    generarCabeceraLog1(_log)

    # Verificamos si existe para la oficina una configuracion con los path imp y exp
    try:
        confruta = ConfigParamsImpExp.objects.get(oficina=oficina)
    except Exception as e:
        _log.error("No esta configurado el parametro de importación")
        generarPieLog1(_log)
        _slogfinal = getLoggingFileData1(_logfileName)
        cerrarLog(_log)
        rutas = Ruta.objects.filter(oficina=oficina, anio=strsemana)

        context['str1'] = _slogfinal
        context['rutas'] = rutas
        return render_to_response('interfaz/importar/_tabla_resultado.html', context)

    _log.info("Semana Importada: {}".format(strsemana))

    if confruta.notificar_error == 1:
        return HttpResponse(status=301)
    else:
        # Se cambia la variable para que no se largue una segunda importacion en simultaneo
        confruta.notificar_error = 1
        confruta.save()
        print('print')

    # Eliminar los registros de suministros_gu y suministros_res para no mezclar con importaciones viejas
    sql = "DELETE from qorder_suministros_res where COD_UNICOM={}".format(oficina)
    try:

        with closing(connection.cursor()) as cursor:
            cursor.execute(sql)

    except Exception as e:
        print("Error {}".format(e))

    sql = "DELETE from qorder_suministros_gu where COD_UNICOM={}".format(oficina)
    try:

        with closing(connection.cursor()) as cursor:
            cursor.execute(sql)

    except Exception as e:
        print("Error {}".format(e))

    # Verificamos si existe el path de importacion de la oficina
    path_txt = str(confruta.path_txt_import).strip(' ')

    if path_txt is None or len(path_txt) == 0:
        confruta.notificar_error = 0
        confruta.save()
        _log.error('No está configurado el directorio de Importación')
        generarPieLog1(_log)
        _slogfinal = getLoggingFileData1(_logfileName)
        print(_slogfinal)
        cerrarLog(_log)
        rutas = Ruta.objects.filter(oficina=oficina, anio=strsemana)

        context['str1'] = _slogfinal
        context['rutas'] = rutas

        writeAudit("gestion Importacion", "Importar", request.user, 'No está configurado el directorio de Importación')
        return render_to_response('interfaz/importar/_tabla_resultado.html', context)

    else:
        # Obtenemos los archivos que existen en el path de importacion y lo agregamos a la lista
        directory = os.path.normpath(path_txt)
        for subdir, dirs, files in os.walk(directory):
            for file in files:
                lista1.append(file)

        if lista1 == []:
            confruta.notificar_error = 0
            confruta.save()
            _log.info("No se encontraron archivos en el directorio")
            generarPieLog1(_log)
            # print(_logfileName)
            _slogfinal = getLoggingFileData1(_logfileName)
            # print(_slogfinal)
            cerrarLog(_log)
            rutas = Ruta.objects.filter(oficina=oficina, anio=strsemana)

            context['str1'] = _slogfinal
            context['rutas'] = rutas
            return render_to_response('interfaz/importar/_tabla_resultado.html', context)


        else:
            # print(oficina)
            print(lista1)
            # Realizo un count para ver si se realizo una importacion en la semana
            suministro = suministros.objects.filter(ANIO=strsemana, COD_UNICOM=oficina).count()
            print(suministro)
            if suministro > 0:
                confruta.notificar_ok = 1
                confruta.save()
                flag_imp = confruta.notificar_ok  # Flag que varia segun si se realizo o no la importacion
                for ar in lista1:
                    # Verifico si el archivo se importo en la primera importacion de no ser asi lo agrego a la lista a importar
                    files = ar
                    edit_file = files.replace("MP", "ME")
                    count_suministros = suministros.objects.filter(ANIO=strsemana, COD_UNICOM=oficina,
                                                                   PORCION_ORIGINAL=edit_file).count()
                    if count_suministros > 1:
                        continue
                    else:
                        listfiles.append(ar)
                if len(listfiles) == 0:
                    confruta.notificar_error = 0
                    confruta.save()
                    _log.info("Los archivos ya fueron importados durante la  semana")
                    generarPieLog1(_log)
                    # print(_logfileName)
                    _slogfinal = getLoggingFileData1(_logfileName)
                    # print(_slogfinal)
                    cerrarLog(_log)
                    rutas = Ruta.objects.filter(oficina=oficina, anio=strsemana)

                    context['str1'] = _slogfinal
                    context['rutas'] = rutas
                    return render_to_response('interfaz/importar/_tabla_resultado.html', context)

                else:
                    # Realizo la importacion con los archivos obtenidos.
                    _log.info("Archivos a importar {}".format(', '.join(listfiles)))
                    obtener = parceararchivo(path_txt, listfiles, oficina, user, _log, flag_imp, strsemana)
                    generarPieLog1(_log)
                    cerrarLog1(_log)
                    str1 = getLoggingFileData1(_logfileName)
                    writeAudit("gestion Importacion", "Importar", request.user,
                               'Se Importo el archivo {} para la oficina {}'.format(lista1, oficina))
                    confruta.notificar_error = 0
                    confruta.save()
                    rutas = Ruta.objects.filter(oficina=oficina, anio=strsemana)
                    print(str1)
                    context['str1'] = str1

                    context['rutas'] = rutas
                    return render_to_response('interfaz/importar/_tabla_resultado.html', context)

            else:
                # Si no se realizo la importacion en la semana entonces.
                confruta.notificar_ok = 0
                confruta.save()
                flag_imp = confruta.notificar_ok
                for ar in lista1:
                    files = ar
                    print(files)
                    listfiles.append(ar)
                _log.info("Archivos a importar {}".format(', '.join(listfiles)))
                obtener = parceararchivo(path_txt, listfiles, oficina, user, _log, flag_imp, strsemana)

                generarPieLog1(_log)
                cerrarLog1(_log)
                str1 = getLoggingFileData1(_logfileName)
                writeAudit("gestion Importacion", "Importar", request.user,
                           'Se Importo el archivo {} para la oficina {}'.format(lista1, oficina))
                confruta.notificar_error = 0
                confruta.save()
                rutas = Ruta.objects.filter(oficina=oficina, anio=strsemana)
                print(str1)
                context['str1'] = str1

                context['rutas'] = rutas
                return render_to_response('interfaz/importar/_tabla_resultado.html', context)


@csrf_exempt
def obtener_avance(request):
    context = RequestContext(request)
    oficina = request.POST['oficina']
    user = request.user
    progreso_tabla = ProcesoImpExp.objects.get(oficina=oficina, nombre_proceso='Importación')
    variable = progreso_tabla.estado_proceso
    total_linea = progreso_tabla.total
    if total_linea == 0 or variable == 0:
        porcentaje = 0
    else:
        porcentaje = variable * 100 / total_linea
    _jsonres = json.dumps({'porcentaje': int(porcentaje)})

    return HttpResponse(_jsonres, content_type='application/json', status=200)


@csrf_exempt
def log_import(request):
    context = RequestContext(request)
    oficina = request.POST['id_centro']

    try:
        # print('Obteniendo parametros de directorio log')

        _param = Parametro.objects.get(pk='P_PATH_LOG_IMP_EXP')
        # print(_param)
        _spath_log = _param.valor_1
        # print(_spath_log)

        # print('P_PATH_LOG_IMP_EXP: ' + _spath_log )

    except Exception as errOf:
        _log.info("Configure los parametros de importacion")

        # print('Ocurrió un error al obtener parametros de configuración de path log: {}'.format(errOf))
        _spath_log = ".//defLog//"
    _fileName = getLoggerFileName1('IMP', oficina)
    _logfileName = _spath_log + _fileName
    str1 = getLoggingFileData1(_logfileName)

    param = ProcesoImpExp.objects.get(oficina=oficina, nombre_proceso='Importacion')
    param.estado = 'INICIO'
    param.total = 0
    param.estado_proceso = 0
    param.save()

    return HttpResponse(str1.replace('\n', '<br/>').replace('\r', '<br/>'), status=200)


@csrf_exempt
@login_required(login_url=settings.LOGIN_PAGE)
def Savefiles(request):
    context = RequestContext(request)
    files = request.FILES.getlist('files[]')
    print(files)
    oficina = request.POST["oficina_val"]
    list_file = []
    if files == []:
        return HttpResponse('Seleccione los archivos a subir', status=300)
    else:
        try:
            for file in files:
                if "." in str(file):
                    return HttpResponse('Debe subir archivos con el formato correcto', status=300)
                else:
                    continue
            get_path = ConfigParamsImpExp.objects.get(oficina=oficina)
            print('path {}'.format(get_path.path_txt_import))
            for f in files:

                with open(str(get_path.path_txt_import) + '/' + str(f), 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)

            get_path = ConfigParamsImpExp.objects.get(oficina=oficina)

            mypath = get_path.path_txt_import
            for root, dirs, files in os.walk(mypath):

                for file in files:
                    list_file.append(file)
            archivos = ",".join(str(e) for e in list_file)
            _jsonres = json.dumps({'archivos': str(archivos)})
            return HttpResponse(_jsonres, content_type='application/json', status=200)
        except Exception as e:
            print("Excepcion {}".format(e))


@csrf_exempt
@login_required(login_url=settings.LOGIN_PAGE)
def delete_files(request):
    context = RequestContext(request)
    oficina = request.POST["oficina"]
    get_path = ConfigParamsImpExp.objects.get(oficina=oficina)
    try:
        mypath = get_path.path_txt_import
        for root, dirs, files in os.walk(mypath):
            for file in files:
                os.remove(os.path.join(root, file))
        return HttpResponse(status=200)
    except Exception as e:
        print("Excepcion {}".format(e))
        return HttpResponse(status=300)


@csrf_exempt
@login_required(login_url=settings.LOGIN_PAGE)
def mostrar_archivos(request):
    context = RequestContext(request)
    list_file = []
    oficina = request.POST["oficina"]
    get_path = ConfigParamsImpExp.objects.get(oficina=oficina)
    try:
        mypath = get_path.path_txt_import
        for root, dirs, files in os.walk(mypath):
            for file in files:
                list_file.append(file)
        archivos = ",".join(str(e) for e in list_file)
        _jsonres = json.dumps({'archivos': str(archivos)})
        return HttpResponse(_jsonres, content_type='application/json', status=200)

        return HttpResponse(context, status=200)
    except Exception as e:
        print("Excepcion {}".format(e))
        return HttpResponse(status=300)


###---------------------detalle de la orden -------------------#####


@csrf_exempt
def consulta_orden_detallada(request):
    try:

        # print('Datos suministro')
        context = RequestContext(request)

        numero_orden = request.POST['numos']

        # print(numero_orden)

        if numero_orden:

            orden = OrdenDeTrabajo.objects.get(pk=numero_orden)

            sumin = orden.punto_suministro

            # print("Sumin {} ".format(sumin))
            # print("Orden {} ".format(orden))

            context['sumin'] = sumin
            context['orden'] = orden

            # print('Orden1 {}'.format(orden.numero_orden))

            _orden = Desc_Orden.objects.filter(orden_trabajo_id=numero_orden)
            # print("Desc_orden {} ".format(_orden))
            context['descorden'] = _orden

            _lect = Desc_Lectura.objects.filter(orden_trabajo_id=numero_orden)
            # print("Desc_lectura {} ".format(_lect))
            context['lecturas'] = _lect

            _anom = Desc_Anomalia.objects.filter(orden_trabajo_id=numero_orden)
            # print("Desc_anomalia {} ".format(_anom))
            context['anomalias'] = _anom

            _foto = Desc_Foto.objects.filter(orden_trabajo=orden)
            # print("Desc_fotos {} ".format(len(_foto)))
            context['fotos'] = _foto

            consumos_anteriores = []
            # print('Ordern ruta {}'.format(orden.ruta.anio))

            rutas = Ruta.objects.filter(anio__lt=orden.ruta.anio)[:6]
            # print(rutas)

            for ruta in rutas:
                # print('Ruta {} Punto Suministro {}'.format(ruta,sumin))
                ordenes_anteriores = OrdenDeTrabajo.objects.filter(ruta=ruta, punto_suministro=sumin)
                # print(ordenes_anteriores)

                for item in ordenes_anteriores:
                    lect_anterior = Desc_Lectura.objects.filter(orden_trabajo=item)
                    desc_orden_ant = Desc_Orden.objects.filter(orden_trabajo=item)
                    if lect_anterior:
                        datos = {
                            'fecha_lectura': desc_orden_ant.fh_fin,
                            'lectura': lect_anterior.lectura,
                            'consumo': lect_anterior.consumo,
                            'tipo_cmo': lect_anterior.tipo_consumo
                        }
                        consumos_anteriores.append(datos)

                        datos = {
                            'fecha_lectura': '20/2/2016',
                            'lectura': '2039',
                            'consumo': '101',
                            'tipo_cmo': 'TC015',
                            'latitud': '3.353657',
                            'longitud': '-76.29517'
                        }
                        consumos_anteriores.append(datos)
                        datos = {
                            'fecha_lectura': '19/3/2016',
                            'lectura': '2130',
                            'consumo': '91',
                            'tipo_cmo': 'TC015',
                            'latitud': '3.353657',
                            'longitud': '-76.29517'
                        }
                        consumos_anteriores.append(datos)
                        datos = {
                            'fecha_lectura': '21/4/2016',
                            'lectura': '2215',
                            'consumo': '85',
                            'tipo_cmo': 'TC015',
                            'latitud': '3.353657',
                            'longitud': '-76.29517'
                        }
                        consumos_anteriores.append(datos)
                        datos = {
                            'fecha_lectura': '20/5/2016',
                            'lectura': '2308',
                            'consumo': '93',
                            'tipo_cmo': 'TC015',
                            'latitud': '3.353657',
                            'longitud': '-76.29517'

                        }
                        consumos_anteriores.append(datos)
                        datos = {
                            'fecha_lectura': '20/6/2016',
                            'lectura': '2378',
                            'consumo': '70',
                            'tipo_cmo': 'TC015',
                            'latitud': '3.353657',
                            'longitud': '-76.29517'
                        }
                        consumos_anteriores.append(datos)
                        datos = {
                            'fecha_lectura': '22/7/2016',
                            'lectura': '2453',
                            'consumo': '75',
                            'tipo_cmo': 'TC015',
                            'latitud': '3.353657',
                            'longitud': '-76.29517'

                        }
                        consumos_anteriores.append(datos)

            context['consumos_anteriores'] = consumos_anteriores
            # print('FIN')
        return render_to_response('reportes/_consulta_orden.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


##################### REPORETE SUMINISTROS NUEVOS / MODIF  #################################

@login_required(login_url=settings.LOGIN_PAGE)
def rpt_sum_alta_modif(request):
    context = RequestContext(request)
    try:
        semana = SemanaXUser.objects.get(usuario=request.user)
        context['semana'] = semana
    except:
        pass
    return render_to_response('reportes/reporte_suministros_alta_modif/Reporte.html', context)


@login_required(login_url=settings.LOGIN_PAGE)
def rpt_sum_alta_modif_getrutassum(request):
    try:
        context = RequestContext(request)
        id_centro = request.POST['id_oficina']
        incluye_exportadas = request.POST['exportadas']
        semana = request.POST['semana']

        semana_filter = {} if semana == 'TODAS' or semana == '' else {'anio__exact': semana}
        ruta_oficina = None
        if id_centro:

            centro = WorkUnit.objects.get(pk=id_centro)
            # print(centro)
            if incluye_exportadas == "1":
                print('entra')
                ruta_oficina = Ruta.objects.select_related('rutasum').filter(oficina=id_centro).filter(
                    **semana_filter).exclude(fecha_hora_exportacion__isnull=True).values('rutasum', 'rutasum__rutasum',
                                                                                         'rutasum__itinerario',
                                                                                         'anio').distinct()
                print(ruta_oficina)
            else:
                ruta_oficina = Ruta.objects.select_related('rutasum').filter(oficina=id_centro).filter(
                    **semana_filter).values('rutasum', 'rutasum__rutasum', 'rutasum__itinerario', 'anio').distinct()
            # print(ruta_oficina)

        context['rutasum'] = ruta_oficina
        return render_to_response('reportes/reporte_suministros_alta_modif/tabla_rutasuministro.html', context)
    except Exception as e:
        # print ("Error {}".format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def rpt_sum_alta_modif_getreporte(request):
    context = RequestContext(request)

    incluye_exportadas = request.POST['exportadas']

    _sfechadesde = request.POST['f_desde']
    _sfechahasta = request.POST['f_hasta']

    _sfechadesde += "000000"
    _sfechahasta += "595959"

    rutsum = eval(request.POST['id_rutasum'])
    # print(rutsum)
    _result = []

    try:

        # obtengo las rutas de los rutasum
        if (incluye_exportadas == "1"):
            _rutas = Ruta.objects.filter(rutasum__in=rutsum, fecha_hora_exportacion__gte=_sfechadesde,
                                         fecha_hora_exportacion__lte=_sfechahasta).exclude(
                fecha_hora_exportacion__isnull=True)
            # print(_rutas)
        else:
            _rutas = Ruta.objects.filter(rutasum__in=rutsum)

        for ruta in _rutas:

            _sRuta = ""
            _sCiclo = ""
            _sItineario = ""
            _nSecuenciaregistro = 0

            _stipo = ""
            _sNumOs = ""
            _sNumSerie = ""
            _sMarca = ""
            _sNumRuedas = ""
            _sObservacion = ""
            _sLectura = ""
            _sFechaHoraRegistros = ""
            _sNumSerieAnt = ""
            _sNumSeriePost = ""
            _sNifAnt = ""
            _sNifPost = ""

            ordenes = OrdenDeTrabajo.objects.filter(ruta=ruta).order_by('secuencia_teorica').values('numero_orden')
            # print('ordenes mod{}'.format(ordenes))
            lstOrd = []

            for o in ordenes:
                lstOrd.append(o['numero_orden'])
            apaAltas = Desc_AparatoAlta.objects.filter(orden_trabajo__in=lstOrd)

            for apa in apaAltas:
                _sRuta = str(ruta.ruta).ljust(2)
                _sCiclo = str(ruta.ciclo).ljust(2)
                _sItineario = str(ruta.itinerario).ljust(4)

                _nSecuenciaregistro = str(apa.secuencia_registro).zfill(4)

                _stipo = "ALTA"
                _sNumOs = apa.orden_trabajo
                _sNumSerie = apa.num_serie
                _sMarca = apa.marca.codigo + " - " + apa.marca.descripcion
                _nNumruedas = apa.num_ruedas
                _sObservacion = apa.observacion
                _sLectura = apa.lectura
                _sFechaHoraRegistros = apa.fecha_hora_registro.strftime("%d/%m/%Y %H:%M")
                _sNumSerieAnt = apa.num_serie_anterior
                _sNumSeriePost = apa.num_serie_posterior
                _sNifAnt = apa.nif_anterior
                _sNifPost = apa.nif_posterior

                _result.append({'tipo': _stipo,
                                'ciclo': _sCiclo,
                                'ruta': _sRuta,
                                'itinerario': _sItineario,
                                'secuencia': _nSecuenciaregistro,
                                'numos': _sNumOs,
                                'marca': _sMarca,
                                'num_serie': _sNumSerie,
                                'num_ruedas': _nNumruedas,
                                'observacion': _sObservacion,
                                'lectura': _sLectura,
                                'fecha_hora_registro': _sFechaHoraRegistros,
                                'num_serie_ant': _sNumSerieAnt,
                                'num_serie_post': _sNumSeriePost,
                                'nif_ant': _sNifAnt,
                                'nif_post': _sNifPost,
                                })

            apaModifs = Desc_AparatoModif.objects.filter(orden_trabajo__in=lstOrd)

            for apa in apaModifs:
                _sRuta = str(ruta.ruta).ljust(2)
                _sCiclo = str(ruta.ciclo).ljust(2)
                _sItineario = str(ruta.itinerario).ljust(4)

                _nSecuenciaregistro = str(apa.secuencia_registro).zfill(4)

                _stipo = "MODIF"
                _sNumOs = apa.orden_trabajo
                _sNumSerie = apa.num_serie
                _sMarca = apa.marca.codigo + " - " + apa.marca.descripcion
                _nNumruedas = "--"
                _sObservacion = apa.observacion
                _sLectura = apa.lectura
                _sFechaHoraRegistros = "--"
                _sNumSerieAnt = "--"
                _sNumSeriePost = "--"
                _sNifAnt = "--"
                _sNifPost = "--"

                _result.append({'tipo': _stipo,
                                'ciclo': _sCiclo,
                                'ruta': _sRuta,
                                'itinerario': _sItineario,
                                'secuencia': _nSecuenciaregistro,
                                'numos': _sNumOs,
                                'marca': _sMarca,
                                'num_serie': _sNumSerie,
                                'num_ruedas': _nNumruedas,
                                'observacion': _sObservacion,
                                'lectura': _sLectura,
                                'fecha_hora_registro': _sFechaHoraRegistros,
                                'num_serie_ant': _sNumSerieAnt,
                                'num_serie_post': _sNumSeriePost,
                                'nif_ant': _sNifAnt,
                                'nif_post': _sNifPost,
                                })

        context['result'] = _result

        return render_to_response('reportes/reporte_suministros_alta_modif/tabla_resultado.html', context)

    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


########################################################

###### REPORTE LECTURA DE LAS RUTAS ####

@login_required(login_url=settings.LOGIN_PAGE)
def rpt_lecturas_rutas(request):
    context = RequestContext(request)
    semana = ''
    try:
        semana = SemanaXUser.objects.get(usuario=request.user)
        context['semana'] = semana
    except:
        pass
    context['semana'] = semana
    return render_to_response('reportes/reporte_lecturas_rutas/Reporte.html', context)


@login_required(login_url=settings.LOGIN_PAGE)
def rpt_lecturas_rutas_getrutassum(request):
    # print('rpt_anomalias_rutas_getrutassum')
    try:
        context = RequestContext(request)
        id_centro = request.POST['id_oficina']
        semana = request.POST['semana']
        incluye_exportadas = request.POST['exportadas']

        ruta_oficina = None

        if id_centro:

            centro = WorkUnit.objects.get(pk=id_centro)
            semana_filter = {} if semana == 'TODAS' or semana == '' else {'anio__exact': semana}

            if incluye_exportadas == "1":

                ruta_oficina = Ruta.objects.select_related('rutasum').filter(oficina=id_centro).filter(
                    **semana_filter).exclude(fecha_hora_exportacion__isnull=True).values('rutasum', 'rutasum__rutasum',
                                                                                         'rutasum__itinerario',
                                                                                         'anio').distinct()

            else:

                ruta_oficina = Ruta.objects.select_related('rutasum').filter(oficina=id_centro).filter(
                    **semana_filter).values('rutasum', 'rutasum__rutasum', 'rutasum__itinerario', 'anio').distinct()

            # print(ruta_oficina)

        context['rutasum'] = ruta_oficina
        return render_to_response('reportes/reporte_lecturas_rutas/tabla_rutasuministro.html', context)
    except Exception as e:
        # print ("Error {}".format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def rpt_lecturas_rutas_getreporte(request):
    # print('entra reportes lec')
    context = RequestContext(request)

    # id_centro = request.POST['id_oficina']
    # centro = WorkUnit.objects.get(pk=id_centro)

    incluye_exportadas = request.POST['exportadas']

    _sfechadesde = request.POST['f_desde']
    _sfechahasta = request.POST['f_hasta']
    semana = request.POST['semana']
    _sfechadesde += "000000"
    _sfechahasta += "235959"

    rutsum = eval(request.POST['id_rutasum'])
    _lstrutas = []
    _result = []

    # print("incluye exportadas " + incluye_exportadas)
    # print("fecha desde " + _sfechadesde)
    # print("fecha hasta " + _sfechahasta)
    # print("rutas " + str(rutsum))

    # obtengo las rutas de los rutasum
    if (incluye_exportadas == "1"):
        _rutas = Ruta.objects.filter(rutasum__in=rutsum, fecha_hora_exportacion__gte=_sfechadesde,
                                     fecha_hora_exportacion__lte=_sfechahasta).exclude(
            fecha_hora_exportacion__isnull=True)
        print(_rutas)
    else:
        _rutas = Ruta.objects.filter(rutasum__in=rutsum, anio=semana)

    if len(_rutas) > 0:
        for r in _rutas:
            _lstrutas.append(r)

    else:
        return HttpResponse('No se encontraron resultado para el ciclo seleccionado', status=301)
    # print('rutas obtenidas ******')
    # print(_rutas)
    # print(_rutas.query)
    if len(_lstrutas) > 0:
        _sNumOs = ""
        _sRuta = ""
        _sCiclo = ""
        _sItineario = ""
        _nSecuenciaregistro = 0

        _sIdanomalia = ""
        _sDescripcionanomalia = ""

        _sCodtecnico = ""
        _sTecnico = ""

        _sNumSerie = ""
        _sMarca = ""
        _nNumruedas = 0

        _nLecturaant = 0
        _sFechalectant = ""
        _nConsumoant = 0

        _nlectura_actual = 0
        # alto, bajo, cero
        _sTiporesultadoLect = ""

        _sPuntosuministro = ""
        _sCalle = ""
        _sNumpuerta = ""
        _sPiso = ""
        _sDuplicador = ""
        _sDepartamento = ""
        _sMunicipio = ""
        _sLocalidad = ""

        _sLatitud = ""
        _sLongitud = ""

        _sFecharesolucion = ""
        _nForzada = 0
        _sUsuarioforzo = ""
        _sFechaforzado = ""
        nombre = ""
        _resultlect = 0

        # desc_ordem,desc_lectura obtenidas por las sclaves foraneas de ordenes fitradas
        ordenes = OrdenDeTrabajo.objects.select_related('ruta', 'consumo__aparato', 'consumo', 'punto_suministro',
                                                        'punto_suministro__aparato', 'desc_orden',
                                                        'desc_orden__tecnico', 'desc_lectura',
                                                        'desc_lectura__marca').filter(
            ruta__in=_lstrutas, estado__in=[265, 777, 401]).order_by('ruta__ciclo', 'ruta__ruta', 'ruta__itinerario',
                                                                     'secuencia_teorica', ).values('ruta__ruta',
                                                                                                   'ruta__itinerario',
                                                                                                   'ruta__ciclo',
                                                                                                   'numero_orden',
                                                                                                   'secuencial_registro',
                                                                                                   'punto_suministro',
                                                                                                   'consumo',
                                                                                                   'desc_orden',
                                                                                                   'desc_orden__fecha_resolucion',
                                                                                                   'desc_orden__tecnico',
                                                                                                   'desc_orden__tecnico__codigo',
                                                                                                   'desc_orden__orden_forzada',
                                                                                                   'desc_orden__usuario_forzo',
                                                                                                   'desc_orden__fh_forzado',
                                                                                                   'desc_lectura__cantidad_intentos',
                                                                                                   'desc_lectura',
                                                                                                   'desc_lectura__marca',
                                                                                                   'desc_lectura__num_serie',
                                                                                                   'punto_suministro__aparato__num_ruedas',
                                                                                                   'punto_suministro__calle',
                                                                                                   'punto_suministro__numero_puerta',
                                                                                                   'punto_suministro__piso',
                                                                                                   'punto_suministro__duplicador',
                                                                                                   'punto_suministro__departamento',
                                                                                                   'punto_suministro__municipio',
                                                                                                   'punto_suministro__localidad',
                                                                                                   'consumo__lectura_anterior',
                                                                                                   'consumo__fecha_lectura_anterior',
                                                                                                   'consumo__consumo_anterior',
                                                                                                   'desc_lectura__lectura',
                                                                                                   'desc_lectura__consulto_historico',
                                                                                                   'desc_orden__tecnico__nombre_1',
                                                                                                   'desc_orden__tecnico__apellido_1',
                                                                                                   'desc_orden__tecnico__apellido_2',
                                                                                                   'desc_lectura__resultado_lectura',
                                                                                                   'desc_orden__fh_fin')
        # lecturas = Desc_Lectura.objects.filter(orden_trabajo__in=ordenes)

        print(str(ordenes.query))

        for _ord in ordenes:
            # -------------------------------------------------AQUELLAS LINEAS COMENDAS EN #-- EXISTE PROBLEMAS CON STRFTIME QUE NO QUIERO TOCAR POR COMPATIBILIDAD.
            _sRuta = str(_ord['ruta__ruta']).ljust(2)
            _sCiclo = str(_ord['ruta__ciclo']).ljust(2)
            # print(_sCiclo)
            _sItineario = str(_ord['ruta__itinerario']).ljust(4)
            # print(_sItineario)

            # desc_orden = Desc_Orden.objects.get(orden_trabajo = lect.orden_trabajo)
            if _ord['desc_orden__fecha_resolucion'] is not None and _ord['desc_orden__fecha_resolucion'] != '':
                _sFecharesolucion = str(_ord['desc_orden__fecha_resolucion'].strftime("%d/%m/%Y"))[:10].ljust(10)
            else:
                _sFecharesolucion = ''

            _sCodtecnico = _ord['desc_orden__tecnico__codigo']
            if _ord['desc_orden__tecnico__nombre_1'] is not None and _ord['desc_orden__tecnico__nombre_1'] != '' and \
                    _ord['desc_orden__tecnico__apellido_1'] is not None and _ord[
                'desc_orden__tecnico__apellido_1'] != '':
                _sTecnico = _ord['desc_orden__tecnico__nombre_1'] + _ord['desc_orden__tecnico__apellido_1']
            elif _ord['desc_orden__tecnico__nombre_1'] is not None and _ord['desc_orden__tecnico__nombre_1'] != '':
                _sTecnico = _ord['desc_orden__tecnico__nombre_1']
            else:
                _sTecnico = ''

            if _ord['desc_orden__orden_forzada'] == 1:
                _nForzada = "Si"
            else:
                _nForzada = "No"

            _sUsuarioforzo = _ord['desc_orden__usuario_forzo']
            _sFechaforzado = _ord['desc_orden__fh_forzado']

            # for orden in ordenes:

            # if str(orden.numero_orden) == str(lect.orden_trabajo):

            _sNumOs = _ord['numero_orden']
            _nSecuenciaregistro = str(_ord['secuencial_registro']).zfill(4)

            # marca - descripcion
            _sMarca = _ord['desc_lectura__marca']
            _sNumSerie = _ord['desc_lectura__num_serie']
            _nNumruedas = _ord['punto_suministro__aparato__num_ruedas']

            # codigo anomalia
            try:
                anom = \
                Desc_Anomalia.objects.select_related('id_anomalia').filter(orden_trabajo=_ord['numero_orden']).values(
                    'id_anomalia_id', 'id_anomalia__descripcion')[0]
                # print(anom)
                _sIdanomalia = anom['id_anomalia_id']
                _sDescripcionanomalia = anom['id_anomalia__descripcion']

            except:

                _sIdanomalia = ""
                _sDescripcionanomalia = ""

            _sPuntosuministro = _ord['punto_suministro']
            _sCalle = _ord['punto_suministro__calle']
            _sNumpuerta = _ord['punto_suministro__numero_puerta']
            _sPiso = _ord['punto_suministro__piso']
            _sDuplicador = _ord['punto_suministro__duplicador']
            _sDepartamento = _ord['punto_suministro__departamento']
            _sMunicipio = _ord['punto_suministro__municipio']
            _sLocalidad = _ord['punto_suministro__localidad']

            _nlectura_actual = _ord['desc_lectura__lectura']

            if _ord['desc_lectura__resultado_lectura'] is not None and _ord['desc_lectura__resultado_lectura'] != '':
                _resultlect = int(_ord['desc_lectura__resultado_lectura'])
            else:
                _resultlect = 0
            _s_cant_intentos = _ord['desc_lectura__cantidad_intentos']
            _s_cant_historico = _ord['desc_lectura__consulto_historico']
            if _ord['desc_orden__fh_fin'] is not None and _ord['desc_orden__fh_fin'] != '':
                _orden = _ord['desc_orden__fh_fin'].strftime('%d/%m/%Y %H:%M:%S')
                _fecha = _orden[0:10]
                _hora = _orden[10:]
            else:
                _fecha = ''
                _hora = ''
            try:
                lat = \
                Desc_Orden.objects.select_related('gps_latitud').filter(orden_trabajo=_ord['numero_orden']).values(
                    'gps_latitud')[0]
                _sLatitud = lat['gps_latitud']
                long = \
                Desc_Orden.objects.select_related('gps_longitud').filter(orden_trabajo=_ord['numero_orden']).values(
                    'gps_longitud')[0]
                _sLongitud = long['gps_longitud']
            except:
                _sLatitud = ''
                _sLongitud = ''
            if _resultlect == 2:
                nombre = 'Alto consumo'
            elif _resultlect == 1:
                nombre = 'Lectura normal'
            elif _resultlect == 3:
                nombre = 'Bajo consumo'
            elif _resultlect == 4:
                nombre = 'Sin Lectura'
            elif _resultlect == 5:
                nombre = 'Lectura sin Controles'
            elif _resultlect == 6:
                nombre = 'Consumo cero'
            elif _resultlect == 7:
                nombre = 'Consumo negativo'

            registrosHc = {'consumoAnt': 'No existen registros', 'fechaLectAnt': 'No existen registros',
                           'lectAnt': 'No existen registros'}

            try:

                fechParse = datetime.strptime(_fecha, '%d/%m/%Y').strftime('%Y-%m-%d')

                cantRegistrosHc = HistoricoConsumo.objects.filter(consumo=_ord['consumo'],
                                                                  fecha_lectura__lt=fechParse).count()

                if int(cantRegistrosHc) > 0:

                    regs = HistoricoConsumo.objects.filter(consumo=_ord['consumo'], fecha_lectura__lt=fechParse).values(
                        'valor_consumo', 'fecha_lectura', 'lectura').order_by('-fecha_lectura').first()

                    registrosHc = {'consumoAnt': regs['valor_consumo'],
                                   'fechaLectAnt': datetime.strftime(regs['fecha_lectura'], '%d/%m/%Y'),
                                   'lectAnt': regs['lectura']}

                else:

                    cantRegistrosDl = Desc_Lectura.objects.filter(num_serie=_sNumSerie).count()

                    orders = []

                    orders_Request = None

                    if int(cantRegistrosDl) > 0:

                        regs = Desc_Lectura.objects.filter(num_serie=_sNumSerie).values('orden_trabajo')

                        for r in regs:
                            orders.append(r['orden_trabajo'])

                        orders_Request = Desc_Orden.objects.filter(orden_trabajo__in=orders,
                                                                   fecha_resolucion__lt=fechParse).values(
                            'fecha_resolucion', 'orden_trabajo').order_by('-fecha_resolucion').first()

                        if orders_Request:
                            order_Filtered = orders_Request['orden_trabajo']

                            fec_res = orders_Request['fecha_resolucion']

                            registros = Desc_Lectura.objects.filter(orden_trabajo=order_Filtered).values('lectura',
                                                                                                         'consumo').first()

                            registrosHc = {'consumoAnt': registros['consumo'],
                                           'fechaLectAnt': datetime.strftime(fec_res, '%d/%m/%Y'),
                                           'lectAnt': registros['lectura']}

            except Exception as e:
                print("Error {}".format(e))
                pass
            # _nLecturaant=_ord['consumo__lectura_anterior']
            # _sFechalectant=_ord['consumo__fecha_lectura_anterior']
            # _nConsumoant=_ord['consumo__consumo_anterior']

            _nLecturaant = registrosHc['lectAnt']
            _sFechalectant = registrosHc['fechaLectAnt']
            _nConsumoant = registrosHc['consumoAnt']

            _result.append({'numos': _sNumOs,
                            'ciclo': _sCiclo,
                            'fecha': _fecha,
                            'hora': _hora,
                            'ruta': _sRuta,
                            'itinerario': _sItineario,
                            'sec_reg': _nSecuenciaregistro,
                            'id_anomalia': _sIdanomalia,
                            'desc_anomalia': _sDescripcionanomalia,

                            'cod_tecnico': _sCodtecnico,
                            'nombre_tecnico': _sTecnico,

                            'marca': _sMarca,
                            'num_serie': _sNumSerie,
                            'num_ruedas': _nNumruedas,

                            'lectura_ant': _nLecturaant,
                            'consumo_ant': _nConsumoant,
                            'fecha_lect_ant': _sFechalectant,

                            'lectura': _nlectura_actual,
                            'tipo_resultado': nombre,

                            'pto_suministro': _sPuntosuministro,
                            'calle': _sCalle,
                            'num_puerta': _sNumpuerta,
                            'piso': _sPiso,
                            'duplicador': _sDuplicador,
                            'departamento': _sDepartamento,
                            'municipio': _sMunicipio,
                            'localidad': _sLocalidad,
                            'latitud': _sLatitud,
                            'longitud': _sLongitud,

                            'fecha_resolucion': _sFecharesolucion,
                            'forzada': _nForzada,
                            'usuario_forzo': _sUsuarioforzo,
                            'fecha_forzo': _sFechaforzado,
                            'cant_intentos': _s_cant_intentos,
                            'cant_historico': _s_cant_historico

                            })

    # print(_result);
    # print("cantidad reg: "+ str(len(_result)))

    context['result'] = _result

    return render_to_response('reportes/reporte_lecturas_rutas/tabla_resultado.html', context)


###### -------------- REPORTE ANOMALIAS DE LAS RUTAS ------------------------####

@login_required(login_url=settings.LOGIN_PAGE)
def rpt_anomalias_rutas(request):
    # print('entro rpt_anomalias_rutas')
    context = RequestContext(request)
    anomalias = Anomalia.objects.all()
    try:
        semana = SemanaXUser.objects.get(usuario=request.user)
        context['semana'] = semana
    except:
        pass
    context['anomalias'] = anomalias
    return render_to_response('reportes/reporte_anomalias_rutas/Reporte.html', context)


@login_required(login_url=settings.LOGIN_PAGE)
def rpt_anomalias_rutas_getrutassum(request):
    # print('rpt_anomalias_rutas_getrutassum')
    try:
        context = RequestContext(request)
        id_centro = request.POST['id_oficina']
        semana = request.POST['semana']
        incluye_exportadas = request.POST['exportadas']

        ruta_oficina = None

        if id_centro:

            centro = WorkUnit.objects.get(pk=id_centro)
            semana_filter = {} if semana == 'TODAS' or semana == '' else {'anio__exact': semana}
            if incluye_exportadas == "1":

                ruta_oficina = Ruta.objects.select_related('rutasum').filter(oficina=id_centro).filter(
                    **semana_filter).exclude(fecha_hora_exportacion__isnull=True).values('rutasum', 'rutasum__rutasum',
                                                                                         'rutasum__itinerario',
                                                                                         'anio').distinct()

            else:

                ruta_oficina = Ruta.objects.select_related('rutasum').filter(oficina=id_centro).filter(
                    **semana_filter).values('rutasum', 'rutasum__rutasum', 'rutasum__itinerario', 'anio').distinct()

            # print('ruta_oficina {}'.format(ruta_oficina))

        context['rutasum'] = ruta_oficina
        return render_to_response('reportes/reporte_anomalias_rutas/tabla_rutasuministro.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


def rpt_anomalias_rutas_getreporte(request):
    context = RequestContext(request)

    # id_centro = request.POST['id_oficina']
    # centro = WorkUnit.objects.get(pk=id_centro)

    incluye_exportadas = request.POST['exportadas']
    anomalias = request.POST['anomalias']
    _sfechadesde = request.POST['f_desde']
    _sfechahasta = request.POST['f_hasta']

    _sfechadesde += "000000"
    _sfechahasta += "595959"
    semana = request.POST['semana']
    rutsum = eval(request.POST['id_rutasum'])
    # print(rutsum)
    # print(anomalias)
    _result = []
    lstanomalias = []
    _lstrutas = []
    # print("incluye exportadas " + incluye_exportadas)
    # print("fecha desde " + _sfechadesde)
    # print("fecha hasta " + _sfechahasta)
    # print("rutas " + str(rutsum))

    # obtengo las rutas de los rutasum
    if (incluye_exportadas == "1"):
        _rutas = Ruta.objects.filter(rutasum__in=rutsum, fecha_hora_exportacion__gte=_sfechadesde,
                                     fecha_hora_exportacion__lte=_sfechahasta).exclude(
            fecha_hora_exportacion__isnull=True)
        # print(_rutas)
    else:
        _rutas = Ruta.objects.filter(rutasum__in=rutsum, anio=semana)

    if len(_rutas) > 0:
        for r in _rutas:
            _lstrutas.append(r)

    else:
        return HttpResponse('No se encontraron resultado para las rutas  seleccionadas', status=301)
    # print('rutas obtenidas ******')
    # print(_rutas)
    # print(_rutas.query)
    if len(_lstrutas) > 0:
        anomalia = anomalias.replace('[', '').replace(']', '').rstrip(',').replace("'", "").split(',')
        # print(anomalia)
        # print('rutas obtenidas ******')
        # print(_rutas)
        # print(_rutas.query)

        # obtengo la lista de ordenes trabajadas
        # ordenes =OrdenDeTrabajo.objects.filter(ruta=_rutas)
        anomalias = Desc_Anomalia.objects.select_related('orden_trabajo', 'orden_trabajo__desc_orden',
                                                         'orden_trabajo__consumo', 'orden_trabajo__ruta',
                                                         'orden_trabajo__consumo_aparato',
                                                         'orden_trabajo__consumo__aparato_marca',
                                                         'orden_trabajo__punto_suministro', 'id_anomalia',
                                                         'id_observacion', 'tipo_resultado').filter(
            orden_trabajo__ruta_id__in=_lstrutas, id_anomalia__in=anomalia).values('id_anomalia_id',
                                                                                   'id_anomalia__descripcion',
                                                                                   'orden_trabajo__ruta__ruta',
                                                                                   'orden_trabajo__ruta__ciclo',
                                                                                   'orden_trabajo__ruta__itinerario',
                                                                                   'orden_trabajo__ruta__oficina_id',
                                                                                   'orden_trabajo__numero_orden',
                                                                                   'orden_trabajo__secuencial_registro',
                                                                                   'tipo_resultado_id',
                                                                                   'tipo_resultado__descripcion',
                                                                                   'orden_trabajo__desc_orden__fecha_resolucion',
                                                                                   'orden_trabajo__desc_orden__fh_fin',
                                                                                   'orden_trabajo__punto_suministro__num_contrato',
                                                                                   'orden_trabajo__punto_suministro_id',
                                                                                   'orden_trabajo__punto_suministro__nif',
                                                                                   'orden_trabajo__punto_suministro__numero_puerta',
                                                                                   'orden_trabajo__punto_suministro__piso',
                                                                                   'orden_trabajo__consumo__aparato__marca_id',
                                                                                   'orden_trabajo__consumo__aparato__marca__descripcion',
                                                                                   'orden_trabajo__consumo__aparato__num_serie',
                                                                                   'orden_trabajo__punto_suministro__duplicador',
                                                                                   'orden_trabajo__punto_suministro__calle',
                                                                                   'orden_trabajo__punto_suministro__municipio',
                                                                                   'orden_trabajo__punto_suministro__localidad',
                                                                                   'id_observacion_id',
                                                                                   'id_observacion__descripcion',
                                                                                   'comentario')
    # for orden in ordenes:
    #  print(orden)
    #  anom = Desc_Anomalia.objects.filter(orden_trabajo=orden,id_anomalia__in=anomalia)
    #  print(anom)
    #  if len(anom)==0:
    #    continue
    #  else:
    #    for n in anom:
    #      print('entra')
    # print('{}'.format(n))
    # lstanomalias.append(n.id_anomalia.id_anomalia)
    # print('lst{}'.format(lstanomalias))
    # lstanomalias=list(set(lstanomalias))
    # variables
    # _sFechaemision=datetime.datetime.now().strftime("%Y/%m/%d")
    # _sOficina = centro.id_workunit

    #
    ########## Por cada anomalia de la ruta ################################

    _sRuta = ""
    _sCiclo = ""
    _sItineario = ""
    _nSecuenciaregistro = 0
    _sTiporesultado = ""
    _sIdanomalia = ""
    _sDescripcionanomalia = ""
    _sPuntosuministro = ""
    _sNif = ""
    _sCalle = ""
    _sNumpuerta = ""
    _sPiso = ""
    _sNumSerie = ""
    _sMarca = ""
    _sDuplicador = ""
    _sApamodif_numserie = ""
    _sApamodif_marca = ""
    _sIdObservacionAdicional = ""
    _sDescripcionObsAdicional = ""
    _sComentarioAnom = ""
    _sNumOs = ""

    for anom in anomalias:

        if anom['id_anomalia_id'] != 'ANREV':

            _sRuta = str(anom['orden_trabajo__ruta__ruta']).ljust(2)
            _sCiclo = str(anom['orden_trabajo__ruta__ciclo']).ljust(2)
            _sItineario = str(anom['orden_trabajo__ruta__itinerario']).ljust(4)

            _nSecuenciaregistro = str(anom['orden_trabajo__secuencial_registro']).zfill(4)

            if anom['tipo_resultado_id'] is not None:
                _sTiporesultado = str(anom['tipo_resultado_id']).ljust(5)
            else:
                _sTiporesultado = ''.ljust(5)

            _sNumOs = anom['orden_trabajo__numero_orden']
            _sIdanomalia = anom['id_anomalia_id']
            _sDescripcionanomalia = anom['id_anomalia__descripcion']
            _sPuntosuministro = anom['orden_trabajo__punto_suministro_id']
            _sNif = anom['orden_trabajo__punto_suministro__nif']
            _sCalle = anom['orden_trabajo__punto_suministro__calle']
            _sNumpuerta = anom['orden_trabajo__punto_suministro__numero_puerta']
            _sPiso = anom['orden_trabajo__punto_suministro__piso']
            _sNumSerie = anom['orden_trabajo__consumo__aparato__num_serie']
            _sMarca = str(anom['orden_trabajo__consumo__aparato__marca_id'])
            _sDuplicador = anom['orden_trabajo__punto_suministro__duplicador']
            _sCalle = anom['orden_trabajo__punto_suministro__calle']
            _orden = anom['orden_trabajo__desc_orden__fh_fin'].strftime('%d/%m/%Y %H:%M:%S')
            _fecha = _orden[0:10]
            _hora = _orden[10:]

            if anom['id_anomalia_id'] == 'AN066  ':
                try:

                    apaModif = Desc_AparatoModif.objects.get(orden_trabajo=anom['orden_trabajo__numero_orden'])

                    _sApamodif_numserie = apaModif.num_serie
                    _sApamodif_marca = apaModif.marca.descripcion
                except Exception as e:
                    pass

            if anom['id_observacion_id'] is not None:
                _sIdObservacionAdicional = anom['id_observacion_id']
                _sDescripcionObsAdicional = anom['id_observacion__descripcion']

            _sComentarioAnom = anom['comentario']

            _result.append({'numos': _sNumOs,
                            'fecha': _fecha,
                            'hora': _hora,
                            'ciclo': _sCiclo,
                            'ruta': _sRuta,
                            'itinerario': _sItineario,
                            'sec_reg': _nSecuenciaregistro,
                            'tipo_resultado': _sTiporesultado,
                            'id_anomalia': _sIdanomalia,
                            'desc_anomalia': _sDescripcionanomalia,
                            'pto_suministro': _sPuntosuministro,
                            'nif': _sNif,
                            'calle': _sCalle,
                            'num_puerta': _sNumpuerta,
                            'piso': _sPiso,
                            'num_serie': _sNumSerie,
                            'marca': _sMarca,
                            'duplicador': _sDuplicador,
                            'id_obs_adicional': _sIdObservacionAdicional,
                            'desc_obs_adicional': _sDescripcionObsAdicional,
                            'comentario_anom': _sComentarioAnom,
                            'apa_modif_num_serie': _sApamodif_numserie,
                            'apa_modif_marca': _sApamodif_marca,
                            })  # #print(_result)
    # print(_result);
    # print("cantidad reg: "+ str(len(_result)))

    context['result'] = _result

    return render_to_response('reportes/reporte_anomalias_rutas/tabla_resultado.html', context)


###### REPORTE EXPORTACION DE LAS RUTAS ####

@login_required(login_url=settings.LOGIN_PAGE)
def rpt_exportacion_rutas(request):
    context = RequestContext(request)
    semana = ''
    try:
        semana = SemanaXUser.objects.get(usuario=request.user)
        context['semana'] = semana
    except:
        pass
    context['semana'] = semana
    return render_to_response('reportes/reporte_exportacion_semana/Reporte.html', context)


@login_required(login_url=settings.LOGIN_PAGE)
def rpt_exportadas_rutas_getreporte(request):
    # print('entra reportes lec')
    context = RequestContext(request)

    id_centro = request.POST['id_oficina']
    semana = request.POST['semana']
    centro = WorkUnit.objects.get(pk=id_centro)

    _lstrutas = []
    _result = []

    _rutas = Ruta.objects.filter(anio=semana, oficina=centro, estado__in=[7, 33, 777], cantidad_leido__gt=0)

    if len(_rutas) > 0:
        for r in _rutas:
            _lstrutas.append(r)
            # print("incluye exportadas " + incluye_exportadas)
            # print("fecha desde " + _sfechadesde)
            # print("fecha hasta " + _sfechahasta)
            # print("rutas " + str(rutsum))

            # obtengo las rutas de los rutasum
    # print('rutas obtenidas ******')
    # print(_rutas)
    # print(_rutas.query)
    cantidad_total = 0
    cantidad_leidos = 0
    for ruta in _lstrutas:
        if ruta.estado == 7 or ruta.estado == 33:
            ordenes = OrdenDeTrabajo.objects.filter(ruta=ruta.idruta, estado=777).count()
            if ordenes > 0:
                cantidad_total = cantidad_total + ruta.cantidad
                cantidad_leidos = cantidad_leidos + ordenes
                _result.append({'ruta': ruta.ruta,
                                'itinerario': ruta.itinerario,
                                'cantidad': ruta.cantidad,
                                'cantidad_leido': ordenes,
                                })
            else:
                continue
        else:

            cantidad_total = cantidad_total + ruta.cantidad
            cantidad_leidos = cantidad_leidos + ruta.cantidad_leido
            _result.append({'ruta': ruta.ruta,
                            'itinerario': ruta.itinerario,
                            'cantidad': ruta.cantidad,
                            'cantidad_leido': ruta.cantidad_leido,

                            })

    # print(_result);
    # print("cantidad reg: "+ str(len(_result)))
    context['cantidad_total'] = cantidad_total
    context['cantidad_exp'] = cantidad_leidos
    context['result'] = _result

    return render_to_response('reportes/reporte_exportacion_semana/tabla_resultado.html', context)


###### ------------------------- REPORTE ANOMALIA  ------------------------- ######

@login_required(login_url=settings.LOGIN_PAGE)
def reporte_anomalia(request):
    context = RequestContext(request)
    anomalias = Anomalia.objects.filter(activo=1)
    context['anomalias'] = anomalias
    return render_to_response('reportes/reporte_anomalia/_reporte_anomalia.html', context)


@login_required(login_url=settings.LOGIN_PAGE)
def table_routes(request):
    context = RequestContext(request)
    oficina = request.POST['id_oficina']
    rutas = Ruta.objects.filter(oficina=oficina)
    context['rutas'] = rutas
    return render_to_response('reportes/reporte_anomalia/_table_routes.html', context)


@login_required(login_url=settings.LOGIN_PAGE)
def get_listadoanomalia(request):
    context = RequestContext(request)
    rutas = eval(request.POST['id_ruta'])
    # print(rutas)
    anomalias = eval(request.POST['id_anomalia'])

    # ordenes = OrdenDeTrabajo.objects.filter(ruta_id__in = rutas)
    # print(len(ordenes))
    desc_anomalia = Desc_Anomalia.objects.filter(orden_trabajo__ruta__in=rutas, id_anomalia__in=anomalias)
    # print(desc_anomalia)
    context['desc_anomalia'] = desc_anomalia

    return render_to_response('reportes/reporte_anomalia/_table_reporte.html', context)


###### ------------------------- REPORTE FRANJA HORARIA  ------------------------- ######

@login_required(login_url=settings.LOGIN_PAGE)
def reporte_fh(request):
    # print('entro reporte_fh')
    context = RequestContext(request)
    # try:
    #    semana = SemanaXUser.objects.get(usuario=request.user)
    #    context['semana'] = semana
    # except:
    #    pass
    return render_to_response('reportes/reporte_franja_horaria/Reporte.html', context)


@login_required(login_url=settings.LOGIN_PAGE)
def obtener_lecturistas(request):
    try:
        context = RequestContext(request)
        id_centro = request.POST['id_oficina']

        if id_centro:

            centro = WorkUnit.objects.get(pk=id_centro)
            # print(centro)
            if id_centro:
                centro = WorkUnit.objects.get(pk=id_centro)
                # print(centro)

                tecnico = OficinaXTecnico.objects.filter(oficina=centro)
                # print(tecnico)

        context['lecturistas'] = tecnico
        return render_to_response('reportes/reporte_franja_horaria/tabla_lecturistas.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def rpt_hora_rutas_getrutassum(request):
    # print('rpt_anomalias_rutas_getrutassum')
    try:
        context = RequestContext(request)
        id_centro = request.POST['id_oficina']
        tecnicos = request.POST['tecnicos']
        # semana=request.POST['semana']
        # incluye_exportadas = request.POST['exportadas']
        listrutas = []
        # print(tecnicos)
        # print(incluye_exportadas)

        ruta_oficina = None

        tecnicos = tecnicos.replace('[', '').replace(']', '').rstrip(',').replace("'", "").split(',')
        # print(tecnicos)
        # semana_filter = {} if semana == 'TODAS' or semana == '' else {'anio__exact': semana}
        for t in tecnicos:

            # print(t.split('-')[0])
            tecnico = Tecnico.objects.get(codigo=t.split('-')[0])
            # print(tecnico.codigo)
            ruta_oficina = Ruta.objects.select_related('rutasum').filter(oficina=id_centro,
                                                                         tecnico=tecnico.codigo).values(
                'idruta', 'rutasum', 'rutasum__rutasum', 'rutasum__itinerario', 'anio').distinct()
            print(str(ruta_oficina))
            for r in ruta_oficina:
                listrutas.append(r)

        context['rutasum'] = listrutas
        return render_to_response('reportes/reporte_franja_horaria/tabla_rutasuministro.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


'''
    if incluye_exportadas == "1":
        for t in tecnicos:
          #print(t.split('-')[0])
          tecnico=Tecnico.objects.get(codigo=t.split('-')[0])

          ruta_oficina = Ruta.objects.select_related('rutasum').filter(oficina=id_centro,tecnico=tecnico.codigo).filter(
                  **semana_filter).exclude(fecha_hora_exportacion__isnull=True).values('rutasum','rutasum__rutasum','rutasum__itinerario','anio').distinct()
          for r in ruta_oficina:

            listrutas.append(r)

    else:
        for t in tecnicos:
          #print(t.split('-')[0])
          tecnico=Tecnico.objects.get(codigo=t.split('-')[0])
          #print(tecnico.codigo)
          ruta_oficina = Ruta.objects.select_related('rutasum').filter(
                  **semana_filter).filter(oficina=id_centro,tecnico=tecnico.codigo).values('rutasum','rutasum__rutasum','rutasum__itinerario','anio').distinct()
          for r in ruta_oficina:

            listrutas.append(r)
'''


@login_required(login_url=settings.LOGIN_PAGE)
def rpt_hora_rutas_getreporte(request):
    context = RequestContext(request)

    # id_centro = request.POST['id_oficina']
    # centro = WorkUnit.objects.get(pk=id_centro)
    _sfechadesde = request.POST['f_desde']
    fechadesde = _sfechadesde[8:10] + '-' + _sfechadesde[5:7] + '-' + _sfechadesde[0:4]
    _sfechahasta = request.POST['f_hasta']
    fechahasta = _sfechahasta[8:10] + '-' + _sfechahasta[5:7] + '-' + _sfechahasta[0:4]

    rutsum = request.POST['id_rutasum']
    # print(rutsum)
    cantidad_leida = 0
    cantidad_total = 0
    _result = []
    rutsum = rutsum.replace('[', '').replace(']', '').rstrip(',').replace("'", "").split(',')
    # print("incluye exportadas " + incluye_exportadas)
    # print("fecha desde " + _sfechadesde)
    # print("fecha hasta " + _sfechahasta)
    # print("rutas " + str(rutsum))
    # obtengo las rutas de los rutasum

    _rutas = Ruta.objects.filter(idruta__in=rutsum)

    print(_rutas)
    listord = []
    listord1 = []
    listord2 = []
    listord3 = []
    listord4 = []
    listord5 = []
    listord6 = []
    listord7 = []
    listord8 = []
    listord9 = []
    listord10 = []
    listord11 = []
    listord12 = []

    _sRuta = ""
    _sFechalectant = ""
    _sFecharesolucion = ""
    ########## Por cada lectura de la ruta ################################

    ordenes = OrdenDeTrabajo.objects.filter(ruta__in=_rutas).values('numero_orden').order_by('secuencia_teorica')
    # print(ordenes.count())
    lecturas = Desc_Orden.objects.filter(orden_trabajo__in=ordenes, fh_fin__range=[_sfechadesde, _sfechahasta]).values(
        'fh_fin', 'orden_trabajo')
    # print(lecturas.count())
    # print(ordenes.query)

    for lect in lecturas:

        desc_orden = lect['orden_trabajo']
        orden = lect['fh_fin'].strftime('%Y%m%d%H:%M:%S')
        hora = orden[8:16]
        # print(hora)
        if hora > '07:00' and hora < '07:59:59':
            listord.append(desc_orden)
        elif hora > '08:00' and hora < '08:59:59':
            listord1.append(desc_orden)
        elif hora > '09:00' and hora < '09:59:59':
            listord2.append(desc_orden)
        elif hora > '10:00' and hora < '10:59:59':
            listord3.append(desc_orden)
        elif hora > '11:00' and hora < '11:59:59':
            listord4.append(desc_orden)
        elif hora > '12:00' and hora < '12:59:59':
            listord5.append(desc_orden)
        elif hora > '13:00' and hora < '13:59:59':
            listord6.append(desc_orden)
        elif hora > '14:00' and hora < '14:59:59':
            listord7.append(desc_orden)
        elif hora > '15:00' and hora < '15:59:59':
            listord8.append(desc_orden)
        elif hora > '16:00' and hora < '16:59:59':
            listord9.append(desc_orden)
        elif hora > '17:00' and hora < '17:59:59':
            listord10.append(desc_orden)
        elif hora > '18:00' and hora < '18:59:59':
            listord11.append(desc_orden)
        elif hora > '19:00' and hora < '06:59:59':
            listord12.append(desc_orden)
        elif hora < '06:59:59':
            listord12.append(desc_orden)
    # print(_result);
    # print("cantidad reg: "+ str(len(_result)))

    _result.append({
        'fecha_desde': str(fechadesde),
        'fecha_hasta': str(fechahasta),
        '07000800': str(len(listord)),
        '08000900': str(len(listord1)),
        '09001000': str(len(listord2)),
        '10001100': str(len(listord3)),
        '11001200': str(len(listord4)),
        '12001300': str(len(listord5)),
        '13001400': str(len(listord6)),
        '14001500': str(len(listord7)),
        '15001600': str(len(listord8)),
        '16001700': str(len(listord9)),
        '17001800': str(len(listord10)),
        '18001900': str(len(listord11)),
        '19000700': str(len(listord12)),
        'cant_leida': len(listord) + len(listord1) + len(listord2) + len(listord3) + len(listord4) + len(
            listord5) + len(
            listord6) + len(listord7) + len(listord8) + len(listord9) + len(listord10) + len(listord11) + len(listord12)

    })

    # print(_result)
    context['result'] = _result
    return render_to_response('reportes/reporte_franja_horaria/tabla_resultado.html', context)


'''
  incluye_exportadas = request.POST['exportadas']

  _sfechadesde =request.POST['f_desde']
  _sfechahasta =request.POST['f_hasta']
  semana=request.POST['semana']
  _sfechadesde +="000000"
  _sfechahasta +="595959"

  rutsum =request.POST['id_rutasum']
  #print(rutsum)

  _result = []
  rutsum=rutsum.replace('[','').replace(']','').rstrip(',').replace("'","").split(',')
  #print("incluye exportadas " + incluye_exportadas)
  #print("fecha desde " + _sfechadesde)
  #print("fecha hasta " + _sfechahasta)
  #print("rutas " + str(rutsum))
  #obtengo las rutas de los rutasum
  if(incluye_exportadas== "1"):
    _rutas = Ruta.objects.filter(rutasum__in = rutsum, fecha_hora_exportacion__gte=_sfechadesde,fecha_hora_exportacion__lte=_sfechahasta).exclude(fecha_hora_exportacion__isnull=True)
  else:
    _rutas = Ruta.objects.filter(rutasum__in = rutsum,anio=semana)



  ########## Por cada lectura de la ruta ################################
  for ruta in _rutas:
    listord=[]
    listord1=[]
    listord2=[]
    listord3=[]
    listord4=[]
    listord5=[]
    listord6=[]
    listord7=[]
    listord8=[]
    listord9=[]
    listord10=[]
    listord11=[]
    listord12=[]

    _sRuta = ""
    _sFechalectant=""
    _sFecharesolucion=""



    ordenes = OrdenDeTrabajo.objects.filter(ruta=ruta).order_by('secuencia_teorica')
    #print(ordenes.count())
    lecturas = Desc_Orden.objects.filter(orden_trabajo__in=ordenes)
    #print(lecturas.count())
    #print(ordenes.query)

    for lect in lecturas:

      _sRuta = str(ruta.ruta).ljust(2)
      desc_orden = Desc_Orden.objects.get(orden_trabajo = lect.orden_trabajo)
      orden=desc_orden.fh_fin.strftime('%Y%m%d%H:%M:%S')
      hora=orden[8:16]
      #print(hora)
      if hora>'07:00' and hora<'07:59:59':
        listord.append(desc_orden)
      elif hora>'08:00' and hora<'08:59:59':
        listord1.append(desc_orden)
      elif hora>'09:00' and hora<'09:59:59':
        listord2.append(desc_orden)
      elif hora>'10:00' and hora<'10:59:59':
        listord3.append(desc_orden)
      elif hora>'11:00' and hora<'11:59:59':
        listord4.append(desc_orden)
      elif hora>'12:00' and hora<'12:59:59':
        listord5.append(desc_orden)
      elif hora>'13:00' and hora<'13:59:59':
        listord6.append(desc_orden)
      elif hora>'14:00' and hora<'14:59:59':
        listord7.append(desc_orden)
      elif hora>'15:00' and hora<'15:59:59':
        listord8.append(desc_orden)
      elif hora>'16:00' and hora<'16:59:59':
        listord9.append(desc_orden)
      elif hora>'17:00' and hora<'17:59:59':
        listord10.append(desc_orden)
      elif hora>'18:00' and hora<'18:59:59':
        listord11.append(desc_orden)
      elif hora>'19:00' and hora<'06:59:59':
        listord12.append(desc_orden)
  #print(_result);
  #print("cantidad reg: "+ str(len(_result)))


    _result.append({
                      'Ruta':_sRuta,
                      '07000800':str(len(listord)),
                      '08000900':str(len(listord1)),
                      '09001000':str(len(listord2)),
                      '10001100':str(len(listord3)),
                      '11001200':str(len(listord4)),
                      '12001300':str(len(listord5)),
                      '13001400':str(len(listord6)),
                      '14001500':str(len(listord7)),
                      '15001600':str(len(listord8)),
                      '16001700':str(len(listord9)),
                      '17001800':str(len(listord10)),
                      '18001900':str(len(listord11)),
                      '19000700':str(len(listord12)),
                      'cant_leida':ruta.cantidad_leido,
                      'cant_total':ruta.cantidad
        })

  #print(_result)
  context['result'] = _result
'''


@login_required(login_url=settings.LOGIN_PAGE)
def reporte_consumo(request):
    # print('entro reporte_fh')
    context = RequestContext(request)
    try:
        semana = SemanaXUser.objects.get(usuario=request.user)
        context['semana'] = semana
    except:
        pass
    return render_to_response('reportes/reporte_consumo_rutas/Reporte.html', context)


@login_required(login_url=settings.LOGIN_PAGE)
def rpt_consumo_rutas_getrutassum(request):
    # print('rpt_anomalias_rutas_getrutassum')
    try:
        context = RequestContext(request)
        id_centro = request.POST['id_oficina']
        semana = request.POST['semana']
        incluye_exportadas = request.POST['exportadas']

        # print(incluye_exportadas)

        ruta_oficina = None

        if id_centro:

            centro = WorkUnit.objects.get(pk=id_centro)
            # print(centro)
            semana_filter = {} if semana == 'TODAS' or semana == '' else {'anio__exact': semana}
            if incluye_exportadas == "1":

                ruta_oficina = Ruta.objects.select_related('rutasum').filter(oficina=id_centro).filter(
                    **semana_filter).exclude(fecha_hora_exportacion__isnull=True).values('rutasum', 'rutasum__rutasum',
                                                                                         'rutasum__itinerario',
                                                                                         'anio').distinct()

            else:

                ruta_oficina = Ruta.objects.select_related('rutasum').filter(oficina=id_centro).filter(
                    **semana_filter).values('rutasum', 'rutasum__rutasum', 'rutasum__itinerario', 'anio').distinct()

            # print(ruta_oficina)

        context['rutasum'] = ruta_oficina
        return render_to_response('reportes/reporte_consumo_rutas/tabla_rutasuministro.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


def rpt_consumo_rutas_getreporte(request):
    context = RequestContext(request)

    # id_centro = request.POST['id_oficina']
    # centro = WorkUnit.objects.get(pk=id_centro)
    lstconsumo = []
    incluye_exportadas = request.POST['exportadas']
    id_centro = request.POST['id_oficina']
    print(id_centro)
    _sfechadesde = request.POST['f_desde']
    _sfechahasta = request.POST['f_hasta']
    semana = request.POST['semana']
    _sfechadesde += "000000"
    _sfechahasta += "595959"
    consumo = request.POST.getlist('consumos[]')
    rutsum = eval(request.POST['id_rutasum'])
    print(rutsum)
    _result = []
    print('llega')
    # print("incluye exportadas " + incluye_exportadas)
    # print("fecha desde " + _sfechadesde)
    # print("fecha hasta " + _sfechahasta)
    # print("rutas " + str(rutsum))
    # print('Consumo'.format(consumo))
    for c in consumo:
        if c == 'NaN':
            continue
        else:
            lstconsumo.append(c)
    # print(lstconsumo)
    # print(len(lstconsumo))
    semana_filter = {} if semana == 'TODAS' or semana == '' else {'anio__exact': semana}
    print(semana_filter)
    if incluye_exportadas == "1":
        _rutas = Ruta.objects.select_related('rutasum').filter(oficina=id_centro, rutasum__in=rutsum).filter(
            **semana_filter).exclude(fecha_hora_exportacion__isnull=True).values('idruta', 'ruta', 'rutasum',
                                                                                 'rutasum__rutasum',
                                                                                 'rutasum__itinerario',
                                                                                 'anio').distinct()

    else:
        _rutas = Ruta.objects.filter(rutasum__in=rutsum).filter(**semana_filter).values('idruta', 'ruta', 'rutasum',
                                                                                        'rutasum__rutasum',
                                                                                        'rutasum__itinerario',
                                                                                        'anio').distinct()

    print(_rutas)
    ########## Por cada lectura de la ruta ################################
    for ruta in _rutas:
        _sRuta = str(ruta['ruta']).ljust(2)
        ordenes = OrdenDeTrabajo.objects.select_related('consumo', 'punto_suministro',
                                                        'punto_suministro__aparato').filter(
            ruta=ruta['idruta']).order_by('secuencia_teorica')
        if len(lstconsumo) == 2:
            lecturas = Desc_Lectura.objects.filter(orden_trabajo__in=ordenes,
                                                   consumo__range=(lstconsumo[0], lstconsumo[1])).count()
            YTH = Desc_Lectura.objects.filter(orden_trabajo__in=ordenes, consumo__range=(lstconsumo[0], lstconsumo[1]))
            # print(YTH)
            # print(lecturas)
            _result.append({
                'Ruta': _sRuta,
                'Rango': str(lstconsumo[0]),
                'Hasta': str(lstconsumo[1]),
                'Cantidad': str(lecturas),

            })


        elif len(lstconsumo) == 4:
            lecturas = Desc_Lectura.objects.filter(orden_trabajo__in=ordenes,
                                                   consumo__range=(lstconsumo[0], lstconsumo[1])).count()
            # print(lecturas)
            _result.append({
                'Ruta': _sRuta,
                'Rango': str(lstconsumo[0]),
                'Hasta': str(lstconsumo[1]),
                'Cantidad': str(lecturas),

            })

            lecturas1 = Desc_Lectura.objects.filter(orden_trabajo__in=ordenes,
                                                    consumo__range=(lstconsumo[2], lstconsumo[3])).count()
            # print('llega')
            # print(lecturas1)
            _result.append({
                'Ruta': _sRuta,
                'Rango': str(lstconsumo[2]),
                'Hasta': str(lstconsumo[3]),
                'Cantidad': str(lecturas1),

            })

        elif len(lstconsumo) == 6:
            lecturas = Desc_Lectura.objects.filter(orden_trabajo__in=ordenes,
                                                   consumo__range=(lstconsumo[0], lstconsumo[1])).count()
            # print(lecturas)
            _result.append({
                'Ruta': _sRuta,
                'Rango': str(lstconsumo[0]),
                'Hasta': str(lstconsumo[1]),
                'Cantidad': str(lecturas),

            })
            lecturas1 = Desc_Lectura.objects.filter(orden_trabajo__in=ordenes,
                                                    consumo__range=(lstconsumo[2], lstconsumo[3])).count()
            # print(lecturas1)
            _result.append({
                'Ruta': _sRuta,
                'Rango': str(lstconsumo[2]),
                'Hasta': str(lstconsumo[3]),
                'Cantidad': str(lecturas1),

            })
            lecturas2 = Desc_Lectura.objects.filter(orden_trabajo__in=ordenes,
                                                    consumo__range=(lstconsumo[4], lstconsumo[5])).count()
            # print(lecturas2)
            _result.append({
                'Ruta': _sRuta,
                'Rango': str(lstconsumo[4]),
                'Hasta': str(lstconsumo[5]),
                'Cantidad': str(lecturas2),

            })


        # print(ordenes.query)
        else:
            lecturas = Desc_Lectura.objects.filter(orden_trabajo__in=ordenes,
                                                   consumo__range=(lstconsumo[0], lstconsumo[1])).count()
            # print(lecturas)
            _result.append({
                'Ruta': _sRuta,
                'Rango': str(lstconsumo[0]),
                'Hasta': str(lstconsumo[1]),
                'Cantidad': str(lecturas),

            })
            lecturas1 = Desc_Lectura.objects.filter(orden_trabajo__in=ordenes,
                                                    consumo__range=(lstconsumo[2], lstconsumo[3])).count()
            # print(lecturas1)
            _result.append({
                'Ruta': _sRuta,
                'Rango': str(lstconsumo[2]),
                'Hasta': str(lstconsumo[3]),
                'Cantidad': str(lecturas1),

            })
            lecturas2 = Desc_Lectura.objects.filter(orden_trabajo__in=ordenes,
                                                    consumo__range=(lstconsumo[4], lstconsumo[5])).count()
            # print(lecturas2)
            _result.append({
                'Ruta': _sRuta,
                'Rango': str(lstconsumo[4]),
                'Hasta': str(lstconsumo[5]),
                'Cantidad': str(lecturas2),

            })
            lecturas3 = Desc_Lectura.objects.filter(orden_trabajo__in=ordenes,
                                                    consumo__range=(lstconsumo[6], lstconsumo[7])).count()
            # print(lecturas3)
            _result.append({
                'Ruta': _sRuta,
                'Rango': str(lstconsumo[6]),
                'Hasta': str(lstconsumo[7]),
                'Cantidad': str(lecturas3),

            })

    # print(_result);
    # print("cantidad reg: "+ str(len(_result)))

    context['result'] = _result

    return render_to_response('reportes/reporte_consumo_rutas/tabla_resultado.html', context)


def reporte_desemp_lect(request):
    # print('entro reporte_fh')
    context = RequestContext(request)
    # try:
    #    semana = SemanaXUser.objects.get(usuario=request.user)
    #    context['semana'] = semana
    # except:
    #    pass

    return render_to_response('reportes/reporte_desempeño_lect/Reporte.html', context)


@login_required(login_url=settings.LOGIN_PAGE)
def obtener_desemp_lect(request):
    try:
        context = RequestContext(request)
        id_centro = request.POST['id_oficina']

        if id_centro:

            centro = WorkUnit.objects.get(pk=id_centro)
            # print(centro)
            if id_centro:
                centro = WorkUnit.objects.get(pk=id_centro)
                # print(centro)

                tecnico = OficinaXTecnico.objects.filter(oficina=centro)
                # print(tecnico)

        context['lecturistas'] = tecnico
        return render_to_response('reportes/reporte_desempeño_lect/tabla_lecturistas.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def rpt_desemp_rutas_getrutassum(request):
    try:
        context = RequestContext(request)
        id_centro = request.POST['id_oficina']
        tecnicos = request.POST['tecnicos']
        listrutas = []

        ruta_oficina = None

        tecnicos = tecnicos.replace('[', '').replace(']', '').rstrip(',').replace("'", "").split(',')

        for t in tecnicos:

            # print(t.split('-')[0])
            tecnico = Tecnico.objects.get(codigo=t.split('-')[0])
            # print(tecnico.codigo)
            ruta_oficina = Ruta.objects.select_related('rutasum').filter(oficina=id_centro,
                                                                         tecnico=tecnico.codigo).values('idruta',
                                                                                                        'rutasum',
                                                                                                        'rutasum__rutasum',
                                                                                                        'rutasum__itinerario',
                                                                                                        'anio')
            for r in ruta_oficina:
                listrutas.append(r)

        context['rutasum'] = listrutas
        return render_to_response('reportes/reporte_desempeño_lect/tabla_rutasuministro.html', context)
    except Exception as e:
        log.error("Error {}".format(e))
        return HttpResponse(status=500)


# print('rpt_anomalias_rutas_getrutassum')
'''
  try:
    context = RequestContext(request)
    id_centro = request.POST['id_oficina']
    tecnicos=request.POST['tecnicos']
    incluye_exportadas = request.POST['exportadas']
    semana = request.POST['semana']
    listrutas=[]

    ruta_oficina = None

    tecnicos=tecnicos.replace('[','').replace(']','').rstrip(',').replace("'","").split(',')
    semana_filter = {} if semana == 'TODAS' or semana == '' else {'anio__exact': semana}
    if incluye_exportadas == "1":
        for t in tecnicos:
          #print(t.split('-')[0])
          tecnico=Tecnico.objects.get(codigo=t.split('-')[0])
          #print(tecnico.codigo)
          ruta_oficina = Ruta.objects.select_related('rutasum').filter(oficina=id_centro,tecnico=tecnico.codigo).filter(
          **semana_filter).exclude(fecha_hora_exportacion__isnull=True).values('rutasum','rutasum__rutasum','rutasum__itinerario','anio').distinct()
          for r in ruta_oficina:

            listrutas.append(r)

    else:
        for t in tecnicos:
          #print(t.split('-')[0])
          tecnico=Tecnico.objects.get(codigo=t.split('-')[0])
          #print(tecnico.codigo)
          ruta_oficina = Ruta.objects.select_related('rutasum').filter(oficina=id_centro,tecnico=tecnico.codigo).filter(
          **semana_filter).values('rutasum','rutasum__rutasum','rutasum__itinerario','anio').distinct()
          for r in ruta_oficina:

            listrutas.append(r)

    context['rutasum'] = listrutas
'''


@login_required(login_url=settings.LOGIN_PAGE)
def rpt_desemp_lect_getreporte(request):
    context = RequestContext(request)
    _sfechadesde = request.POST['f_desde']
    _sfechahasta = request.POST['f_hasta']

    rutsum = eval(request.POST['id_rutasum'])
    # print(rutsum)

    _result = []

    # print("incluye exportadas " + incluye_exportadas)
    # print("fecha desde " + _sfechadesde)
    # print("fecha hasta " + _sfechahasta)
    # print("rutas " + str(rutsum))
    # obtengo las rutas de los rutasum

    _rutas = Ruta.objects.filter(rutasum__in=rutsum)

    ########## Por cada lectura de la ruta ################################
    for ruta in _rutas:
        ordenes = OrdenDeTrabajo.objects.filter(ruta=ruta).order_by('secuencia_teorica')
        # print(ordenes.count())
        lecturas = Desc_Orden.objects.select_related('orden_trabajo', 'tecnico', 'id').filter(orden_trabajo__in=ordenes,
                                                                                              fh_fin__range=[
                                                                                                  _sfechadesde,
                                                                                                  _sfechahasta]).values(
            'orden_trabajo', 'tecnico', 'secuencia_real', 'orden_trabajo__punto_suministro__aparato__num_serie',
            'orden_trabajo__punto_suministro__cliente__apellido_1', 'tecnico__terminal_portatil', 'tecnico__nombre_1',
            'tecnico__apellido_1', 'orden_trabajo__punto_suministro__calle',
            'orden_trabajo__punto_suministro__num_contrato', 'orden_trabajo__punto_suministro__cliente__numero_puerta',
            'orden_trabajo__secuencia_teorica', 'fh_fin').order_by('fh_fin')
        # print(ordenes.query)

        for lect in lecturas:
            _sRuta = str(ruta.ruta).ljust(2)
            sec_real = str(lect['secuencia_real'])
            nroaparato = str(lect['orden_trabajo__punto_suministro__aparato__num_serie'])
            _sCliente = str(lect['orden_trabajo__punto_suministro__cliente__apellido_1'])
            _stp = str(lect['tecnico__terminal_portatil'])
            direccion = str(lect['orden_trabajo__punto_suministro__calle'])
            nrocuenta = str(lect['orden_trabajo__punto_suministro__num_contrato'])
            nropuerta = str(lect['orden_trabajo__punto_suministro__cliente__numero_puerta'])
            sec_teorica = str(lect['orden_trabajo__secuencia_teorica'])

            nombretec = str(lect['tecnico__nombre_1']) + ',' + str(lect['tecnico__apellido_1'])
            orden = lect['fh_fin'].strftime('%d/%m/%Y %H:%M:%S')
            fecha = orden[0:10]
            hora = orden[10:]

            # print(_result);
            # print("cantidad reg: "+ str(len(_result)))

            _result.append({
                'Ruta': _sRuta,
                'Cliente': _sCliente,
                'Fecha': fecha,
                'Hora': hora,
                'tp': _stp,
                'direccion': direccion,
                'num_serie': nroaparato,
                'num_cuenta': nrocuenta,
                'nro_puerta': nropuerta,
                'sec_teorica': sec_teorica,
                'sec_real': sec_real,
                'nombre': nombretec

            })

    # print(_result)
    context['result'] = _result
    return render_to_response('reportes/reporte_desempeño_lect/tabla_resultado.html', context)

    # id_centro = request.POST['id_oficina']
    # centro = WorkUnit.objects.get(pk=id_centro)


'''
  incluye_exportadas = request.POST['exportadas']

  _sfechadesde =request.POST['f_desde']
  _sfechahasta =request.POST['f_hasta']

  _sfechadesde +="000000"
  _sfechahasta +="595959"

  rutsum = eval(request.POST['id_rutasum'])
  #print(rutsum)


  _result = []

  #print("incluye exportadas " + incluye_exportadas)
  #print("fecha desde " + _sfechadesde)
  #print("fecha hasta " + _sfechahasta)
  #print("rutas " + str(rutsum))
  #obtengo las rutas de los rutasum
  if(incluye_exportadas== "1"):
    _rutas = Ruta.objects.filter(rutasum__in = rutsum, fecha_hora_exportacion__gte=_sfechadesde,fecha_hora_exportacion__lte=_sfechahasta).exclude(fecha_hora_exportacion__isnull=True)
  else:
    _rutas = Ruta.objects.filter(rutasum__in = rutsum)



  ########## Por cada lectura de la ruta ################################
  for ruta in _rutas:
    ordenes = OrdenDeTrabajo.objects.filter(ruta=ruta).order_by('secuencia_teorica')
    #print(ordenes.count())
    lecturas = Desc_Orden.objects.select_related('orden_trabajo','tecnico','id').filter(orden_trabajo__in=ordenes).values('orden_trabajo','tecnico','secuencia_real','orden_trabajo__punto_suministro__aparato__num_serie','orden_trabajo__punto_suministro__cliente__apellido_1','tecnico__terminal_portatil','tecnico__nombre_1','tecnico__apellido_1','orden_trabajo__punto_suministro__calle','orden_trabajo__punto_suministro__num_contrato','orden_trabajo__punto_suministro__cliente__numero_puerta','orden_trabajo__secuencia_teorica','fh_fin').order_by('fh_fin')
    #print(ordenes.query)

    for lect in lecturas:
      _sRuta = str(ruta.ruta).ljust(2)
      sec_real=str(lect['secuencia_real'])
      nroaparato=str(lect['orden_trabajo__punto_suministro__aparato__num_serie'])
      _sCliente=str(lect['orden_trabajo__punto_suministro__cliente__apellido_1'])
      _stp=str(lect['tecnico__terminal_portatil'])
      direccion=str(lect['orden_trabajo__punto_suministro__calle'])
      nrocuenta=str(lect['orden_trabajo__punto_suministro__num_contrato'])
      nropuerta=str(lect['orden_trabajo__punto_suministro__cliente__numero_puerta'])
      sec_teorica=str(lect['orden_trabajo__secuencia_teorica'])
      nombretec=str(lect['tecnico__nombre_1'])+','+str(lect['tecnico__apellido_1'])
      orden=lect['fh_fin'].strftime('%d/%m/%Y %H:%M:%S')

      fecha=orden[0:10]
      hora=orden[10:]

  #print(_result);
  #print("cantidad reg: "+ str(len(_result)))


      _result.append({
                      'Ruta':_sRuta,
                      'Cliente':_sCliente,
                      'Fecha':fecha,
                      'Hora':hora,
                      'tp':_stp,
                      'direccion':direccion,
                      'num_serie':nroaparato,
                      'num_cuenta':nrocuenta,
                      'nro_puerta':nropuerta,
                      'sec_teorica':sec_teorica,
                      'nombre':nombretec,
                      'sec_real':sec_real

        })

  #print(_result)
  context['result'] = _result
'''


@login_required(login_url=settings.LOGIN_PAGE)
def reorganizcion_gu_main(request):
    context = RequestContext(request)

    return render_to_response('ordenes/reorganizacion_gu/_reorganizacion_gu.html', context)


def obtener_rutas(request):
    context = RequestContext(request)
    oficina = request.POST['id_oficina']
    semanas = request.POST['num_semana']

    rutas = Ruta.objects.filter(oficina=oficina, anio=semanas)
    print(rutas)

    context['ruta'] = rutas

    return render_to_response('ordenes/reorganizacion_gu/_load_rutas.html', context)




def cargar_suministros(request):
    context = RequestContext(request)
    ruta = request.POST['ruta']
    oficina = request.POST['id_oficina']
    _result = []
    ruta = Ruta.objects.values('idruta').get(idruta=ruta)
    ordenes = OrdenDeTrabajo.objects.select_related('punto_suministro', 'ruta').filter(ruta=ruta['idruta']).values(
        'ruta__ruta', 'numero_orden', 'punto_suministro', 'punto_suministro__secuencia_teorica',
        'punto_suministro__localidad', 'punto_suministro__calle', 'punto_suministro__numero_puerta',
        'punto_suministro__aparato', 'punto_suministro__cliente')

    for orden in ordenes:
        _result.append({
            'Ruta': orden['ruta__ruta'],
            'Suministro': orden['punto_suministro'],
            'Localidad': orden['punto_suministro__localidad'],
            'Direccion': orden['punto_suministro__calle'],
            'Numero_Calle': orden['punto_suministro__numero_puerta'],
            'Aparato': orden['punto_suministro__aparato'],
            'Cliente': orden['punto_suministro__cliente'],
            'Orden': orden['numero_orden']

        })
    sumin_gu = reubicacion_suministro.objects.all();
    context['reubicar_suministros'] = sumin_gu
    print(_result)
    context['suministros'] = _result
    return render_to_response('ordenes/reorganizacion_gu/_table_suministros.html', context)


def insertar_suministro(request):
    context = RequestContext(request)
    cp = []
    oficina = request.POST['id_oficina']
    orden_trabajo = request.POST['id_orden']
    orden_trabajo = orden_trabajo.replace('[', '').replace(']', '').rstrip(',').split(',')
    print(orden_trabajo)
    for orden in orden_trabajo:
        orden = orden.replace("'", "")
        print(orden)
        ord_trabajo = OrdenDeTrabajo.objects.select_related('punto_suministro', 'ruta').filter(
            numero_orden=orden).values('punto_suministro', 'ruta', 'ruta__ruta')
        print(ord_trabajo)
        datos_suministro = suministros.objects.select_related('SEG_REG').get(
            SEG_REG=ord_trabajo['punto_suministro']).values('SEG_REG', 'RUTA', 'ITINERARIO', 'CICLO',
                                                            'PORCION_ORIGINAL', 'SEC_ORIGINAL', 'UNIDAD_ORIGINAL',
                                                            'SECUENCIA', 'DIRECCION', 'NRO_PUERTA')
        print(datos_suministro)
        cp.append(reubicacion_suministro(ruta=datos_suministro['RUTA'],
                                         itinerario=datos_suministro['ITINERARIO'],
                                         punto_suministro=datos_suministro['SEG_REG'],
                                         secuencia_teorica=int(datos_suministro['SECUENCIA']),
                                         direccion=datos_suministro['DIRECCION'],
                                         numero_puerta=int(datos_suministro['NRO_PUERTA']),
                                         porcion_original=datos_suministro['PORCION_ORIGINAL'],
                                         sec_original=int(datos_suministro['SEC_ORIGINAL']),
                                         unidad_original=datos_suministro['UNIDAD_ORIGINAL']
                                         ))
        # print(cp)

        datos_suministro.update(rutasum=None)
        count_ordenes = OrdenDeTrabajo.objects.filter(ruta=ord_trabajo['ruta']).values('punto_suministro').count()
        ruta = Ruta.objects.filter(idruta=ord_trabajo['ruta']).update(cantidad=count_ordenes)
        ord_trabajo.delete()

    reubicacion_suministro.objects.bulk_create(cp)

    sumin_gu = reubicacion_suministro.objects.all();
    context['reubicar_suministros'] = sumin_gu
    return render_to_response('ordenes/reorganizacion_gu/_table_change.html', context)


def reinsertar_suministro(request):
    context = RequestContext(request)
    oficina = request.POST['id_oficina']
    id_suministros = request.POST['id_suministros']
    ruta = request.POST['ruta']
    date = datetime.now().strftime('%Y%m%d')
    orden_ruta = ''
    ptosuministro = ''
    id_suministros = id_suministros.replace('[', '').replace(']', '').rstrip(',').split(',')

    for sumin in id_suministros:
        sumin = sumin.replace("'", "")

        # Obtengo ruta nueva para cambiar la orden.
        get_ruta = Ruta.objects.get(idruta=ruta)

        # numero de ordenes para actualizar la orden y luego la cantidad total en la ruta.
        cant_ord_nva = OrdenDeTrabajo.objects.filter(ruta=ruta).values('numero_orden').count()

        # actualizo rutasum del punto de suministro a actualizar.
        upd_pto_sumin = PuntoDeSuministro.objects.filter(punto_suministro=pto_upd).update(rutasum=get_ruta.rutasum)

        # actualizo datos del suministro , sin tocar los originales.
        upd_sumin = suministros.objects.filter(SEG_REG=pto_upd).update(RUTA=get_ruta.ruta, CICLO=get_ruta.ciclo,
                                                                       ITINERARIO=get_ruta.itinerario)

        # Genero nueva orden con nueva ruta.
        sql = "INSERT INTO aysa_qorder.qorder_ordendetrabajo(numero_orden, prioridad, estado, secuencial_registro, secuencia_teorica, orden_terreno, generada_desde_num_os, flag_asignacion_guardada, fecha_hora_asignacion, fecha_hora_importacion, fecha_hora_exportacion, fecha_hora_anulacion, fecha_hora_ult_modificacion, fecha_hora_carga, consumo_id, punto_suministro_id, ruta_id, tecnico_id, tipo_orden_id, usuario_asignacion_id)\
    select concat(COD_UNICOM,{},RUTA,lpad(ITINERARIO,5,'0'),CICLO,@rownum:=@rownum+1),1,1,SECUENCIA,SECUENCIA,0,null,0,null,null,null,null,null,null,concat(COD_MARCA,NRO_APARTO,'CO011'),SEG_REG,concat(COD_UNICOM,RUTA,lpad(ITINERARIO,5,'0'),CICLO,lpad(ANIO,4,'0')),null,{},null from (SELECT @rownum:={}) r, qorder_suministros where COD_UNICOM='{}' and SEG_REG={}".format(
            date, tipo_orden.id, cant_ord_nva, oficina, sumin)
        try:
            # print('aca')
            with closing(connection.cursor()) as cursor:
                cursor.execute(sql)

        except Exception as e:
            print('Error {}'.format(e))

        get_ruta_nva = Ruta.objects.get(idruta=ruta).update(
            cantidad=OrdenDeTrabajo.objects.filter(ruta=ruta).values('numero_orden').count())

        ordenes = OrdenDeTrabajo.objects.select_related('punto_suministro', 'ruta').filter(ruta=get_ruta.idruta).values(
            'ruta__ruta', 'numero_orden', 'punto_suministro', 'punto_suministro__secuencia_teorica',
            'punto_suministro__localidad', 'punto_suministro__calle', 'punto_suministro__numero_puerta',
            'punto_suministro__aparato', 'punto_suministro__cliente')

        reubicacion = reubicacion_suministro.objects.filter(punto_suministro=sumin).update(ruta=get_ruta.ruta,
                                                                                           itinerario=get_ruta.itinerario)

        for orden in ordenes:
            _result.append({
                'Ruta': orden['ruta__ruta'],
                'Suministro': orden['punto_suministro'],
                'Localidad': orden['punto_suministro__localidad'],
                'Direccion': orden['punto_suministro__calle'],
                'Numero_Calle': orden['punto_suministro__numero_puerta'],
                'Aparato': orden['punto_suministro__aparato'],
                'Cliente': orden['punto_suministro__cliente'],
                'Orden': orden['numero_orden']

            })
        context['suministros'] = _result
        return render_to_response('ordenes/reorganizacion_gu/_table_suministros.html', context)


'''
@login_required(login_url=settings.LOGIN_PAGE)
def atp_terminal(request):
    context = RequestContext(request)
    id_tp = request.POST['id_tp']
    context['terminal'] = TerminalPortatil.objects.get(id_tp=id_tp)
    return render_to_response('data_admin/_data_terminal.html', context)

@login_required(login_url=settings.LOGIN_PAGE)
def atp_save(request):
    context = RequestContext(request)
    id_tp = request.POST['id_tp']
    alias = request.POST['alias']
    mail = request.POST['mail']
    android_id = request.POST['android_id']
    ct = request.POST['ct']
    centro= WorkUnit.objects.get(pk=ct)
    activo = request.POST['activo']
    tp = TerminalPortatil.objects.get(id_tp=id_tp)
    tp.alias_tp = alias
    tp.email_tp = mail
    tp.android_id = android_id
    print (tp.get_tecnico())
    cant_ord = QwOrdenes.objects.filter(estado__in=[3,7],
                                        id_tecnico= tp.get_tecnico()).count()
    print (cant_ord)
    if tp.id_unidad_negocio != centro:
        if cant_ord == 0:
            tp.id_unidad_negocio = centro
        else:
            context['tiene_ordenes'] = True
    if tp.activo != if_1_True(true_or_false(activo)):
        if cant_ord == 0:
            tp.activo = if_1_True(true_or_false(activo))
        else:
            context['tiene_ordenes'] = True
    tp.save()
    context['terminal'] = tp
    context['terminales'] = QwTerminalesPortatiles.objects.all()
    return render_to_response('data_admin/_terminales.html', context)
'''


def config_acciones_cliente_main(request):
    context = RequestContext(request)

    _lst_config = []
    _lst_acciones = []

    _configuraciones = ConfigAccion_Cabe.objects.all().values('codigo',
                                                              'descripcion',
                                                              'activo',
                                                              'fecha_vigencia')

    _acciones = Codigo.objects.filter(prefijo='AC', activo=1).values('codigo',
                                                                     'descripcion')

    _rutasum = RutaSum.objects.all().values('oficina', 'rutasum', 'itinerario', 'pk').order_by('oficina', 'rutasum',
                                                                                               'itinerario')

    if len(_configuraciones) > 0:

        for conf in _configuraciones:
            _codigo = conf['codigo']
            _descrip = conf['descripcion']

            _activo = ''
            if str(conf['activo']) == '1':
                _activo = 'Si'
            else:
                _activo = 'No'

            if conf['fecha_vigencia'] is not None:
                _fecha_vig = conf['fecha_vigencia'].strftime('%d/%m/%Y')

            else:
                _fecha_vig = ''

            _lst_config.append({'codigo': _codigo,
                                'descripcion': _descrip,
                                'activo': _activo,
                                'fecha_vigencia': _fecha_vig
                                })

    if len(_acciones) > 0:
        for acc in _acciones:
            _codigo = acc['codigo']
            _descrip = acc['descripcion']

            _lst_acciones.append({'codigo': _codigo,
                                  'descripcion': _descrip
                                  })

    units = WorkUnit.objects.all().values('id_workunit', 'name')

    o = []

    for u in units:
        o.append({'contratista_id': u['id_workunit'], 'contratista_nombre': u['name']})

    context['configuraciones'] = _lst_config
    context['acciones'] = _lst_acciones
    context['rutasum'] = _rutasum
    context['oficinas'] = o

    return render_to_response('data_admin/accion_clientes/_config_acciones_cli_main.html', context)


def get_configuraciones(request):
    context = RequestContext(request)

    _lst_config = []
    _lst_acciones = []

    _configuraciones = ConfigAccion_Cabe.objects.all().values('codigo',
                                                              'descripcion',
                                                              'activo',
                                                              'fecha_vigencia')

    if len(_configuraciones) > 0:

        for conf in _configuraciones:
            _codigo = conf['codigo']
            _descrip = conf['descripcion']

            _activo = ''
            if str(conf['activo']) == '1':
                _activo = 'Si'
            else:
                _activo = 'No'

            if conf['fecha_vigencia'] is not None:
                _fecha_vig = conf['fecha_vigencia'].strftime('%d/%m/%Y')

            else:
                _fecha_vig = ''

            _lst_config.append({'codigo': _codigo,
                                'descripcion': _descrip,
                                'activo': _activo,
                                'fecha_vigencia': _fecha_vig
                                })

    context['configuraciones'] = _lst_config

    return render_to_response('data_admin/accion_clientes/_table_configuraciones_resumida.html', context)


def nueva_configuracion(request):
    context = RequestContext(request)

    _codigo = request.POST['codigo_config']
    _descrip = request.POST['descrip_config']
    _activo = request.POST['estado_config']
    _fecha_vigencia = request.POST['fechavigencia_config']

    _usuario = request.user

    _lst_config = []

    _new_config = ConfigAccion_Cabe()
    _new_config.codigo = _codigo
    _new_config.descripcion = _descrip
    _new_config.activo = _activo
    _new_config.fecha_vigencia = datetime.strptime(_fecha_vigencia, '%d/%m/%Y').strftime('%Y-%m-%d')

    _new_config.usuario_modif = _usuario
    _new_config.ultima_modif = datetime.now()

    try:
        _new_config.save(force_insert=True)

        _configuraciones = ConfigAccion_Cabe.objects.all().values('codigo',
                                                                  'descripcion',
                                                                  'activo',
                                                                  'fecha_vigencia')

        if len(_configuraciones) > 0:

            for conf in _configuraciones:
                _codigo = conf['codigo']
                _descrip = conf['descripcion']

                _activo = ''
                if str(conf['activo']) == '1':
                    _activo = 'Si'
                else:
                    _activo = 'No'

                if conf['fecha_vigencia'] is not None:
                    _fecha_vig = conf['fecha_vigencia'].strftime('%d/%m/%Y')

                else:
                    _fecha_vig = ''

                _lst_config.append({'codigo': _codigo,
                                    'descripcion': _descrip,
                                    'activo': _activo,
                                    'fecha_vigencia': _fecha_vig
                                    })

        context['configuraciones'] = _lst_config

        return render_to_response('data_admin/accion_clientes/_table_configuraciones.html', context)


    except IntegrityError as ie:

        return HttpResponse(status=300)

    except Exception as e:

        return HttpResponse(status=500)


def getconfiguracion_edit(request):
    context = RequestContext(request)

    _codigo = request.POST['codigo_config']

    try:

        _configuraciones = ConfigAccion_Cabe.objects.filter(codigo=_codigo).values('codigo',
                                                                                   'descripcion',
                                                                                   'activo',
                                                                                   'fecha_vigencia')

        if len(_configuraciones) > 0:

            conf = _configuraciones[0]

            _codigo = conf['codigo']
            _descrip = conf['descripcion']

            _activo = str(conf['activo'])

            if conf['fecha_vigencia'] is not None:
                _fecha_vig = conf['fecha_vigencia'].strftime('%d/%m/%Y')

            else:
                _fecha_vig = ''

            _jsonres = json.dumps({'codigo': _codigo,
                                   'descripcion': _descrip,
                                   'activo': _activo,
                                   'fecha_vigencia': _fecha_vig})

            return HttpResponse(_jsonres, content_type='application/json', status=200)

        else:
            return HttpResponse(status=500)


    except IntegrityError as ie:

        return HttpResponse(status=300)

    except Exception as e:

        return HttpResponse(status=500)


def editar_configuracion(request):
    context = RequestContext(request)

    _codigo = request.POST['codigo_config']
    _descrip = request.POST['descrip_config']
    _activo = request.POST['estado_config']
    _fecha_vigencia = request.POST['fechavigencia_config']

    _usuario = request.user

    _lst_config = []

    try:

        _config = ConfigAccion_Cabe.objects.get(codigo=_codigo)

        _config.descripcion = _descrip
        _config.activo = _activo
        _config.fecha_vigencia = datetime.strptime(_fecha_vigencia, '%d/%m/%Y').strftime('%Y-%m-%d')
        _config.usuario_modif = _usuario.username
        _config.ultima_modif = datetime.now()

        _config.save()

        _configuraciones = ConfigAccion_Cabe.objects.all().values('codigo',
                                                                  'descripcion',
                                                                  'activo',
                                                                  'fecha_vigencia')

        if len(_configuraciones) > 0:

            for conf in _configuraciones:
                _codigo = conf['codigo']
                _descrip = conf['descripcion']

                _activo = ''
                if str(conf['activo']) == '1':
                    _activo = 'Si'
                else:
                    _activo = 'No'

                if conf['fecha_vigencia'] is not None:
                    _fecha_vig = conf['fecha_vigencia'].strftime('%d/%m/%Y')

                else:
                    _fecha_vig = ''

                _lst_config.append({'codigo': _codigo,
                                    'descripcion': _descrip,
                                    'activo': _activo,
                                    'fecha_vigencia': _fecha_vig
                                    })

            context['configuraciones'] = _lst_config

            return render_to_response('data_admin/accion_clientes/_table_configuraciones.html', context)

    except IntegrityError as ie:

        return HttpResponse(status=300)

    except Exception as e:

        return HttpResponse(status=500)


def delete_configuracion(request):
    context = RequestContext(request)

    _codigo = request.POST['codigo_config']

    _lst_config = []
    _configuraciones = []
    try:

        _config = ConfigAccion_Cabe.objects.get(codigo=_codigo)

        _config.delete()

        _configuraciones = ConfigAccion_Cabe.objects.all().values('codigo',
                                                                  'descripcion',
                                                                  'activo',
                                                                  'fecha_vigencia')

        if len(_configuraciones) > 0 or len(_configuraciones) == 0:

            for conf in _configuraciones:
                _codigo = conf['codigo']
                _descrip = conf['descripcion']

                _activo = ''
                if str(conf['activo']) == '1':
                    _activo = 'Si'
                else:
                    _activo = 'No'

                if conf['fecha_vigencia'] is not None:
                    _fecha_vig = conf['fecha_vigencia'].strftime('%d/%m/%Y')

                else:
                    _fecha_vig = ''

                _lst_config.append({'codigo': _codigo,
                                    'descripcion': _descrip,
                                    'activo': _activo,
                                    'fecha_vigencia': _fecha_vig
                                    })

            context['configuraciones'] = _lst_config

            return render_to_response('data_admin/accion_clientes/_table_configuraciones.html', context)

        # else:
        #      return HttpResponse(status=500)


    except IntegrityError as ie:

        return HttpResponse(status=300)

    except Exception as e:

        return HttpResponse(status=500)


def asig_accion_config(request):
    context = RequestContext(request)

    _codigo = request.POST['codigo_config']
    _codigo_acc = request.POST['codigo_accion']
    _orden = request.POST['orden']
    _param_add = request.POST['param_add']
    _obligatorio = request.POST['obligatorio']
    _tipo_acc = request.POST['tipo_accion']

    _lst_acciones_config = []

    try:

        _cod_config_get = ConfigAccion_Cabe.objects.get(codigo=_codigo)
        _cod_accion_get = Codigo.objects.get(codigo=_codigo_acc)

        _acc_config = ConfigAccion_Deta()
        _acc_config.codigo_config_accion = _cod_config_get
        _acc_config.codigo_accion = _cod_accion_get
        _acc_config.orden_ejecucion = int(_orden)
        _acc_config.parametro_adicional = _param_add.upper()
        _acc_config.obligatorio = _obligatorio
        _acc_config.tipo_accion = _tipo_acc

        _acc_config.save()

        _accionesconfig = ConfigAccion_Deta.objects \
            .select_related('codigo_accion') \
            .filter(codigo_config_accion=_codigo) \
            .values('codigo_accion',
                    'codigo_accion__descripcion',
                    'codigo_config_accion',
                    'orden_ejecucion',
                    'parametro_adicional',
                    'obligatorio', 'tipo_accion').order_by('orden_ejecucion')

        if len(_accionesconfig) > 0:

            for acc in _accionesconfig:
                _codigo_accion = acc['codigo_accion']
                _codigo_acc_conf = acc['codigo_config_accion']
                _codigo_acc_descrip = acc['codigo_accion__descripcion']
                _codigo_acc_ordenejec = acc['orden_ejecucion']
                _codigo_acc_paramadic = acc['parametro_adicional']
                _codigo_acc_oblig = acc['obligatorio']
                _codigo_acc_tipo = acc['tipo_accion']

                _lst_acciones_config.append({
                    'codigo_accion': _codigo_accion,
                    'codigo_config_accion': _codigo_acc_conf,
                    'descripcion': _codigo_acc_descrip,
                    'orden_ejecucion': _codigo_acc_ordenejec,
                    'parametro_adicional': _codigo_acc_paramadic,
                    'obligatorio': _codigo_acc_oblig,
                    'tipo_accion': _codigo_acc_tipo
                })

        context['acc_config'] = _lst_acciones_config

        return render_to_response('data_admin/accion_clientes/_table_acciones_config.html', context)

    except IntegrityError as ie:

        return HttpResponse(status=300)

    except Exception as e:

        return HttpResponse(status=500)


def cargar_acciones_config(request):
    context = RequestContext(request)
    _codigo = request.POST['codigo_config']

    _lst_acciones_config = []

    _accionesconfig = ConfigAccion_Deta.objects \
        .select_related('codigo_accion') \
        .filter(codigo_config_accion=_codigo) \
        .values('codigo_accion',
                'codigo_accion__descripcion',
                'codigo_config_accion',
                'orden_ejecucion',
                'parametro_adicional',
                'obligatorio', 'tipo_accion').order_by('orden_ejecucion')

    if len(_accionesconfig) > 0:

        for acc in _accionesconfig:
            _codigo_accion = acc['codigo_accion']
            _codigo_acc_conf = acc['codigo_config_accion']
            _codigo_acc_descrip = acc['codigo_accion__descripcion']
            _codigo_acc_ordenejec = acc['orden_ejecucion']
            _codigo_acc_paramadic = acc['parametro_adicional']
            _codigo_acc_oblig = acc['obligatorio']
            _codigo_acc_tipo = acc['tipo_accion']

            _lst_acciones_config.append({
                'codigo_accion': _codigo_accion,
                'codigo_config_accion': _codigo_acc_conf,
                'descripcion': _codigo_acc_descrip,
                'orden_ejecucion': _codigo_acc_ordenejec,
                'parametro_adicional': _codigo_acc_paramadic,
                'obligatorio': _codigo_acc_oblig,
                'tipo_accion': _codigo_acc_tipo
            })

    context['acc_config'] = _lst_acciones_config
    return render_to_response('data_admin/accion_clientes/_table_acciones_config.html', context)


def get_clientes_config(request):
    context = RequestContext(request)

    _codigo = request.POST['codigo_config']

    _lstclientes = []

    try:

        cont_clientes_cfg = ConfigAccion_Cliente.objects.filter(codigo_config_accion_cabe=_codigo).count()
        # if cont_clientes_cfg < 1000:

        # _cliconfig = ConfigAccion_Cliente.objects.\
        #     select_related('codigo_cliente').\
        #     filter(codigo_config_accion_cabe = _codigo).values_list('codigo_cliente_id' ,flat=True)

        _psum_configurados = ConfigAccion_Cliente.objects. \
            select_related('codigo_punto_suministro'). \
            filter(codigo_config_accion_cabe=_codigo).values_list('codigo_punto_suministro_id', flat=True)

        # _psum = PuntoDeSuministro.objects.\
        #     select_related('rutasum').\
        #     filter(cliente__in=_cliconfig).\
        #     values('punto_suministro',
        #           'num_contrato',
        #           'localidad',
        #           'rutasum__rutasum',
        #           'rutasum__itinerario',
        #           'rutasum__oficina',
        #           'rutasum_id',
        #           'cliente__nombre',
        #           'cliente__apellido_1',
        #           'cliente_id')

        _psum = PuntoDeSuministro.objects. \
            select_related('rutasum', 'cliente'). \
            filter(punto_suministro__in=_psum_configurados). \
            values('punto_suministro',
                   'num_contrato',
                   'rutasum__rutasum',
                   'rutasum__itinerario',
                   'rutasum__oficina',
                   'rutasum__oficina__name',
                   'rutasum_id',
                   'cliente__nombre',
                   'cliente__apellido_1',
                   'cliente_id')

        if len(_psum) > 0:

            for p in _psum:
                _punto_suministro = p['punto_suministro']
                _num_contrato = p['num_contrato']
                _ruta = str(p['rutasum__rutasum'])
                _itinerario = str(p['rutasum__itinerario'])
                _contratista = str(p['rutasum__oficina']) + ' - ' + str(p['rutasum__oficina__name'])
                _rutasum_id = str(p['rutasum_id'])
                _nombre = p['cliente__apellido_1']
                _cliente_id = p['cliente_id']

                _lstclientes.append({'nis': _punto_suministro,
                                     'nic': _num_contrato,
                                     'nombre': _nombre,
                                     'ruta': _ruta,
                                     'itinerario': _itinerario,
                                     'contratista': _contratista,
                                     'rutasum_id': _rutasum_id,
                                     'cod_config': _codigo,
                                     'cod_cliente': _cliente_id})

        context['asig_conf_cli'] = _lstclientes

        return render_to_response('data_admin/accion_clientes/_table_clientes_configurados.html', context)

        # else:
        # context['asig_conf_cli'] = []
        # return render(request,'data_admin/accion_clientes/_table_clientes_configurados.html', context,status=201)

    except Exception as e:

        return HttpResponse(status=500)


def get_clientes_filtro(request):
    context = RequestContext(request)

    _rutasum_id = request.POST['rutasum_id']
    _nis = request.POST['nis']
    _nic = request.POST['nic']
    _nombre = request.POST['nombre']  # porcentaje cambiar nim
    _cantidad = request.POST['cantidad']  # no se usa
    _codigo = request.POST['codigo_config']

    _lstclientes = []
    _lst_rutas = []
    _clientes = []
    try:

        _cliconfig = ConfigAccion_Cliente.objects. \
            filter(codigo_config_accion_cabe=_codigo).values_list('codigo_cliente_id', flat=True)
        _lst_rutas = _rutasum_id.split(',')

        if _nis:

            _clientes = PuntoDeSuministro.objects.select_related('cliente','rutasum'). \
                filter(punto_suministro=_nis).exclude(cliente__in=_cliconfig). \
                values('punto_suministro', 'num_contrato',
                       'cliente__nombre', 'cliente__apellido_1', 'cliente__apellido_2',
                       'calle', 'numero_puerta', 'cliente__codigo', 'rutasum__rutasum', 'rutasum__itinerario').distinct()

        elif _nic:

            _clientes = PuntoDeSuministro.objects.select_related('cliente','rutasum') \
                .filter(num_contrato=_nic).exclude(cliente__in=_cliconfig) \
                .values('punto_suministro', 'num_contrato',
                        'cliente__nombre', 'cliente__apellido_1', 'cliente__apellido_2',
                        'calle', 'numero_puerta', 'cliente__codigo', 'rutasum__rutasum', 'rutasum__itinerario').distinct()
        else:
            for e in _lst_rutas:
                if e != '':
                    _clientes += PuntoDeSuministro.objects.select_related('cliente','rutasum') \
                        .filter(rutasum__itinerario=e).exclude(cliente__in=_cliconfig) \
                        .values('punto_suministro', 'num_contrato',
                                'cliente__nombre', 'cliente__apellido_1', 'cliente__apellido_2',
                                'calle', 'numero_puerta', 'cliente__codigo', 'rutasum__rutasum', 'rutasum__itinerario').distinct()

        for c in _clientes:
            _lstclientes.append({'id': c['cliente__codigo'],
                                 'nis': c['punto_suministro'],
                                 'nic': c['num_contrato'],
                                 'nombre': '{} {} {}'.format(c['cliente__nombre'].strip(' '),
                                                             c['cliente__apellido_1'].strip(' '),
                                                             c['cliente__apellido_2']).strip(' '),
                                 'direccion': '{} #{}'.format(c['calle'].strip(' '),
                                                              str(c['numero_puerta']).strip(' ')),
                                 'ruta': c['rutasum__rutasum'],
                                 'itinerario': c['rutasum__itinerario']})

        if _nombre != "" and int(_nombre) and len(_clientes) > 0:  # porcentaje cambiasr variable nombre jeje
            _l_new = []
            _l_new = sorted(_lstclientes, key=lambda i: i['id'])
            sort_l = list(_l_new)
            random.shuffle(sort_l)
            context['clientes'] = busqueda_lista_aleatoria(sort_l, _nombre)
            context['cant_res'] = len(sort_l)
            context['cant_res_porc'] = len(busqueda_lista_aleatoria(sort_l, _nombre))
        elif _cantidad != "" and int(_cantidad) and len(_clientes) > 0:  # cantidad
            _l_new = []
            _l_new = sorted(_lstclientes, key=lambda i: i['id'])
            sort_l = list(_l_new)
            random.shuffle(sort_l)
            context['clientes'] = busqueda_lista_aleatoria_cantidad(sort_l, _cantidad)
            context['cant_res'] = len(sort_l)
            context['cant_res_porc'] = len(busqueda_lista_aleatoria_cantidad(sort_l, _cantidad))
        else:
            context['clientes'] = _lstclientes
            context['cant_res'] = len(_lstclientes)
            context['cant_res_porc'] = len(_lstclientes)

    except Exception as e:
        log.error(str(e))
        pass

    return render_to_response('data_admin/accion_clientes/_table_resultado_clientes.html', context)


def busqueda_lista_aleatoria(lista, valor_porcentaje):
    if len(lista) == 0:
        return False
    else:
        cantidadreturn = len(lista)
        porc = int(valor_porcentaje)
        ce = porc * cantidadreturn
        ce2 = ce * 0.01
        ce2_converted = int(ce2)
        lista_nueva = []
        for l in lista:
            if len(lista_nueva) < ce2_converted:
                lista_nueva.append(l)
        return lista_nueva


def asignar_clientes_config(request):

    context = RequestContext(request)

    _codigo = request.POST['codigo_config']
    # _codigos_cli = request.POST['codigos_cliente']
    _codigos_puntos_sum = request.POST['codigos_punto_sum']

    _rutasum_id = request.POST['rutasum_id']
    _nis = request.POST['nis']
    _nic = request.POST['nic']
    _nombre = request.POST['nombre']

    _lstclientes = []
    _lstcli_insert = []
    _lst_hist_cli_insert = []
    _cliconf = None
    _clientes = []

    _fecha_hoy = datetime.today()

    _usuario_asignacion = request.user

    # filtros select:
    tipo_filtro = request.POST['tipo_filtro']
    contratista = request.POST['contratista']
    porc = request.POST['porc']
    cant = request.POST['cant']

    try:

        # _lst_cli = _codigos_cli.split(',')
        _lst_puntos_sum = _codigos_puntos_sum.split(',')
        _cod = ConfigAccion_Cabe.objects.get(pk=_codigo)
        _lst_rutas = _rutasum_id.split(',')
        # _lstclientesInsert = Cliente.objects.filter(codigo__in=_lst_cli).distinct()
        _lst_puntos_sum_insert = PuntoDeSuministro.objects.filter(punto_suministro__in=_lst_puntos_sum).distinct()

        if tipo_filtro == "0":
            tipo_filtro = 'Filtro particular'
        else:
            tipo_filtro = 'Asignacion Masiva'

        rutas_filter = '('

        for l in _lst_rutas:

            if l == '':

                rutas_filter += "'" + str(l) + "'"

            else:

                rutas_filter += "'" + str(l) + "',"

        rutas_filter += ')'

        filtros = {'tipo_filtro': tipo_filtro, 'contratista': contratista, 'nis': _nis, 'nic': _nic,
                   'porcentaje': porc, 'cantidad': len(_lst_puntos_sum_insert), 'itinerarios seleccionados': rutas_filter}

        json_object = json.dumps(filtros)

        ConfigAccion_Cabe.objects.filter(codigo=_codigo).update(filtros_clientes=str(json_object))

        # for c in _lstclientesInsert:
        for p_sum in _lst_puntos_sum_insert:
            _cliconf = ConfigAccion_Cliente()
            _cliconf.codigo_config_accion_cabe = _cod
            _cliconf.codigo_punto_suministro = p_sum
            _cliconf.codigo_cliente = p_sum.cliente

            _lstcli_insert.append(_cliconf)


        # Borramos todos los clientes configurados a esta acción

        clientes_configurados = ConfigAccion_Cliente.objects.filter(codigo_config_accion_cabe=_cod)

        if len(clientes_configurados) > 0:

            clientes_configurados.delete()


        ConfigAccion_Cliente.objects.bulk_create(_lstcli_insert)

        for p_sum in _lst_puntos_sum_insert:
            _hist_cliconf = HistoricoConfigAccion_Cliente()

            _hist_cliconf.codigo_config_accion_cabe = _cod
            _hist_cliconf.codigo_punto_suministro = p_sum
            _hist_cliconf.codigo_cliente = p_sum.cliente
            _hist_cliconf.fecha = _fecha_hoy
            _hist_cliconf.usuario_asignacion = _usuario_asignacion

            _lst_hist_cli_insert.append(_hist_cliconf)

        HistoricoConfigAccion_Cliente.objects.bulk_create(_lst_hist_cli_insert)

        # _cliconfig = ConfigAccion_Cliente.objects.\
        #     filter(codigo_config_accion_cabe = _codigo).values_list('codigo_cliente_id' ,flat=True)

        # if _nis:

        #     _clientes = PuntoDeSuministro.objects.select_related('cliente').\
        #         filter(punto_suministro = _nis).exclude(cliente__in = _cliconfig).\
        #         values('punto_suministro','num_contrato',
        #                                  'cliente__nombre','cliente__apellido_1','cliente__apellido_2',
        #                                  'calle','numero_puerta', 'cliente__codigo', 'localidad').distinct()

        # elif _nic:

        #     _clientes = PuntoDeSuministro.objects.select_related('cliente')\
        #         .filter(num_contrato = _nic).exclude(cliente__in = _cliconfig)\
        #         .values('punto_suministro','num_contrato',
        #                                  'cliente__nombre','cliente__apellido_1','cliente__apellido_2',
        #                                  'calle','numero_puerta', 'cliente__codigo', 'localidad').distinct()
        # else:
        #     for e in _lst_rutas:
        #       if e != '':
        #         _clientes += PuntoDeSuministro.objects.select_related('cliente')\
        #             .filter(rutasum__itinerario = e).exclude(cliente__in = _cliconfig)\
        #             .values('punto_suministro','num_contrato',
        #                                     'cliente__nombre','cliente__apellido_1','cliente__apellido_2',
        #                                     'calle','numero_puerta', 'cliente__codigo', 'localidad','municipio').distinct()

        # for c in _clientes:

        #     _lstclientes.append({'id': c['cliente__codigo'],
        #                          'nis':c['punto_suministro'],
        #                          'nic':c['num_contrato'],
        #                          'nombre':'{} {} {}'.format( c['cliente__nombre'].strip(' '),
        #                                                      c['cliente__apellido_1'].strip(' '),
        #                                                      c['cliente__apellido_2']).strip(' '),
        #                          'direccion': '{} #{}'.format(c['calle'].strip(' '),str(c['numero_puerta']).strip(' ')),
        #                          'localidad':c['localidad'].strip(' ')})

        # context['clientes'] = _lstclientes

    except Exception as e:
        log.error(str(e))
        pass

    return render_to_response('data_admin/accion_clientes/_table_resultado_clientes.html', context)


def delete_cli_indiv_config(request):
    context = RequestContext(request)

    _codigo = request.POST['codigo_config']
    # _codigo_cli = request.POST['codigo_cliente']
    _codigo_punto_sum = request.POST['codigo_punto_sum']

    _lstclientes = []

    try:

        _cli = ConfigAccion_Cliente.objects. \
            get(codigo_config_accion_cabe=_codigo, codigo_punto_suministro=_codigo_punto_sum)

        _cli.delete()


        # Se actualiza la cantidad de suministros asignados en los filtros

        _conf = ConfigAccion_Cabe.objects.get(codigo=_codigo)

        _filtros = json.loads(_conf.filtros_clientes)

        _cantidad = _filtros['cantidad']

        _cantidad = _cantidad - 1

        _filtros['cantidad'] = _cantidad

        _filtros_actualizados = json.dumps(_filtros)

        _conf.filtros_clientes = _filtros_actualizados

        _conf.save()

        # _cliconfig = ConfigAccion_Cliente.objects.\
        #     select_related('codigo_cliente').\
        #     filter(codigo_config_accion_cabe = _codigo).values_list('codigo_cliente_id' ,flat=True)

        # _psum = PuntoDeSuministro.objects.\
        #     select_related('rutasum').\
        #     filter(cliente__in=_cliconfig).\
        #     values('punto_suministro',
        #            'num_contrato',
        #            'municipio',
        #            'rutasum__rutasum',
        #            'rutasum__itinerario',
        #            'rutasum__oficina',
        #            'rutasum_id',
        #            'cliente__nombre',
        #            'cliente__apellido_1',
        #            'cliente_id')

        # if len(_psum)>0:

        #     for p in _psum:

        #         _punto_suministro = p['punto_suministro']
        #         _num_contrato = p['num_contrato']
        #         _municipio = p['municipio']
        #         _rutasum__ruta = str(p['rutasum__oficina']) + '-' + str(p['rutasum__rutasum']) + '-' + str(p['rutasum__itinerario'])
        #         _rutasum_id = str(p['rutasum_id'])
        #         _nombre = p['cliente__nombre'] + ' - ' + p['cliente__apellido_1']
        #         _cliente_id = p['cliente_id']

        #         _lstclientes.append({'nis': _punto_suministro,
        #                              'nic': _num_contrato,
        #                              'nombre': _nombre,
        #                              'municipio': _municipio,
        #                              'rutasum':_rutasum__ruta,
        #                              'rutasum_id': _rutasum_id,
        #                              'cod_config': _codigo,
        #                              'cod_cliente': _cliente_id})

        # context['asig_conf_cli']= _lstclientes

        return HttpResponse(status=200)


    except Exception as e:

        return HttpResponse(status=500)


def delete_accion_config(request):
    context = RequestContext(request)

    _codigo = request.POST['codigo_config']
    _codigo_acc = request.POST['codigo_accion']
    _orden = request.POST['orden_ejecucion']

    _lst_acciones_config = []

    try:
        _cod_accion_cfg_get = ConfigAccion_Deta.objects.get(codigo_config_accion=_codigo, codigo_accion=_codigo_acc,
                                                            orden_ejecucion=_orden)
        _cod_accion_cfg_get.delete()

        _accionesconfig = ConfigAccion_Deta.objects \
            .select_related('codigo_accion') \
            .filter(codigo_config_accion=_codigo) \
            .values('codigo_accion',
                    'codigo_accion__descripcion',
                    'codigo_config_accion',
                    'orden_ejecucion',
                    'parametro_adicional',
                    'obligatorio', 'tipo_accion').order_by('orden_ejecucion')

        if len(_accionesconfig) > 0:

            for acc in _accionesconfig:
                _codigo_accion = acc['codigo_accion']
                _codigo_acc_conf = acc['codigo_config_accion']
                _codigo_acc_descrip = acc['codigo_accion__descripcion']
                _codigo_acc_ordenejec = acc['orden_ejecucion']
                _codigo_acc_paramadic = acc['parametro_adicional']
                _codigo_acc_oblig = acc['obligatorio']
                _codigo_acc_tipo = acc['tipo_accion']

                _lst_acciones_config.append({
                    'codigo_accion': _codigo_accion,
                    'codigo_config_accion': _codigo_acc_conf,
                    'descripcion': _codigo_acc_descrip,
                    'orden_ejecucion': _codigo_acc_ordenejec,
                    'parametro_adicional': _codigo_acc_paramadic,
                    'obligatorio': _codigo_acc_oblig,
                    'tipo_accion': _codigo_acc_tipo
                })

        context['acc_config'] = _lst_acciones_config

        return render_to_response('data_admin/accion_clientes/_table_acciones_config.html', context)

    except IntegrityError as ie:

        return HttpResponse(status=300)

    except Exception as e:

        return HttpResponse(status=500)


def del_all_cfg(req):  # retocar

    try:

        context = RequestContext(req)

        cuenta_config = ConfigAccion_Cabe.objects.count()

        if (cuenta_config > 0):

            _config = ConfigAccion_Cabe.objects.all()

            _config.delete()  # borra todas las cfgs en cascada [retocado en modelos]

            _configuraciones = ConfigAccion_Cabe.objects.all().values('codigo',
                                                                      'descripcion',
                                                                      'activo',
                                                                      'fecha_vigencia')
            context['configuraciones'] = _configuraciones

            return render_to_response('data_admin/accion_clientes/_table_configuraciones.html', context)  # not working

        else:

            return HttpResponse(status=300)

    except:

        return HttpResponse(status=500)


def get_rutas_per_oficina(request):
    context = RequestContext(request)

    _codigo = request.POST['codigo_of']

    try:

        _rutas = RutaSum.objects.filter(oficina=_codigo).values('itinerario').distinct()

        context['rutas'] = _rutas  # aca guardamos las rutas no hace falta usar context

        list_rutas = []

        if len(_rutas) > 0:

            for e in _rutas:
                list_rutas.append({'itinerario': e[
                    'itinerario']})  # agrego las rutas a la lista. aca se agregan las rutas que tengan el codigo de oficina que se trae desde el html

        _jsonres = json.dumps(list_rutas)  # dumps codifica la lista en archivo JSON

        return HttpResponse(_jsonres, content_type='application/json', status=200)


    except IntegrityError as ie:

        return HttpResponse(status=300)

    except Exception as e:

        return HttpResponse(status=500)


def busqueda_lista_aleatoria_cantidad(lista, valor_cantidad):
    if len(lista) == 0:

        return False

    else:

        cant = int(valor_cantidad)

        lista_nueva = []

        for l in lista:

            if len(lista_nueva) < cant:
                lista_nueva.append(l)  # se debe hacer un metodo para porcentaje y cantidad de forma polimorfico..

        return lista_nueva


def asign_config_bulk(request):
    context = RequestContext(request)

    _codigo = request.POST['codigo_config']

    _of = request.POST['_of']

    try:

        nulleable = None

        count = 0  # cuenta los registros de la tabla configaccion_cleintes, no los insertados ahora mismo.

        with connection.cursor() as cursor:

            cursor.callproc('sp_insert_clientesconfig', params=[_of, _codigo, nulleable])  # llamo al sp

        count = ConfigAccion_Cliente.objects.all().count()

        return HttpResponse(count, content_type='application/json', status=200)  # envio el count hacia el html

    except Exception as e:

        log.error(str(e))

        pass


def asign_cliente_aleatorio(request):  # limpiar codigo

    context = RequestContext(request)

    _codigo = request.POST['codigo_config']

    _cantidad = request.POST['cantidad']

    _rutasum_id = request.POST['rutasum_id']

    _nis = request.POST['nis']

    _nic = request.POST['nic']

    _nombre = request.POST['nombre']  # PORCENTAJE

    _lstclientes = []

    _lstcli_insert = []

    _cliconf = None

    _clientes = []

    _lstclientesInsert = []

    try:

        _cod = ConfigAccion_Cabe.objects.get(pk=_codigo)

        _lst_rutas = _rutasum_id.split(',')

        _cliconfig = ConfigAccion_Cliente.objects. \
            filter(codigo_config_accion_cabe=_codigo).values_list('codigo_cliente_id', flat=True)

        if _nis:

            _clientes = PuntoDeSuministro.objects.select_related('cliente'). \
                filter(punto_suministro=_nis).exclude(cliente__in=_cliconfig). \
                values('cliente__codigo').distinct()
        elif _nic:

            _clientes = PuntoDeSuministro.objects.select_related('cliente') \
                .filter(num_contrato=_nic).exclude(cliente__in=_cliconfig) \
                .values('cliente__codigo').distinct()
        else:
            for e in _lst_rutas:
                if e != '':
                    _clientes += PuntoDeSuministro.objects.select_related('cliente') \
                        .filter(rutasum__itinerario=e).exclude(cliente__in=_cliconfig) \
                        .values('cliente__codigo').distinct()

        for c in _clientes:
            _lstclientes.append({'id': c['cliente__codigo']})

        # -------------------------------------------------------SORTEO

        if _nombre != "" and int(_nombre) and len(_clientes) > 0:

            _l_new = []

            _l_new = sorted(_lstclientes, key=lambda i: i['id'])

            sort_l = list(_l_new)

            random.shuffle(sort_l)

            lista_nueva = busqueda_lista_aleatoria(sort_l, _nombre)  # _nombre es el procentaje

            for c in lista_nueva:
                _lstclientesInsert.append(c)

            for c in _lstclientesInsert:
                _cliconf = ConfigAccion_Cliente()

                _cliconf.codigo_config_accion_cabe = _cod

                c1 = Cliente()

                c1.codigo = c['id']

                _cliconf.codigo_cliente = c1

                _lstcli_insert.append(_cliconf)

        elif _cantidad != "" and int(_cantidad) and len(_clientes) > 0:  # cantidad

            _l_new = []

            _l_new = sorted(_lstclientes, key=lambda i: i['id'])

            sort_l = list(_l_new)

            random.shuffle(sort_l)

            lista_nueva = busqueda_lista_aleatoria_cantidad(sort_l, _cantidad)

            for c in lista_nueva:
                _cliconf = ConfigAccion_Cliente()

                _cliconf.codigo_config_accion_cabe = _cod

                c1 = Cliente()

                c1.codigo = c['id']

                _cliconf.codigo_cliente = c1

                _lstcli_insert.append(_cliconf)

        ConfigAccion_Cliente.objects.bulk_create(_lstcli_insert)  # insert
        # -------------------------------------------------------ENVIAR RESULTADOS DE BUSQUEDA A LA TABLA DE RESULTADOS
        list_cliente_research = []
        _clientes = []
        if _nis:
            _clientes = PuntoDeSuministro.objects.all().select_related('cliente'). \
                filter(punto_suministro=_nis).exclude(cliente__in=_cliconfig). \
                values('punto_suministro', 'num_contrato',
                       'cliente__nombre', 'cliente__apellido_1', 'cliente__apellido_2',
                       'calle', 'numero_puerta', 'cliente__codigo', 'localidad').distinct()
        elif _nic:
            _clientes = PuntoDeSuministro.objects.all().select_related('cliente') \
                .filter(num_contrato=_nic).exclude(cliente__in=_cliconfig) \
                .values('punto_suministro', 'num_contrato',
                        'cliente__nombre', 'cliente__apellido_1', 'cliente__apellido_2',
                        'calle', 'numero_puerta', 'cliente__codigo', 'localidad').distinct()
        else:
            for e in _lst_rutas:
                if e != '':
                    _clientes += PuntoDeSuministro.objects.all().select_related('cliente') \
                        .filter(rutasum__itinerario=e).exclude(cliente__in=_cliconfig) \
                        .values('punto_suministro', 'num_contrato',
                                'cliente__nombre', 'cliente__apellido_1', 'cliente__apellido_2',
                                'calle', 'numero_puerta', 'cliente__codigo', 'localidad', 'municipio').distinct()
        for c in _clientes:
            list_cliente_research.append({'id': c['cliente__codigo'],
                                          'nis': c['punto_suministro'],
                                          'nic': c['num_contrato'],
                                          'nombre': '{} {} {}'.format(c['cliente__nombre'].strip(' '),
                                                                      c['cliente__apellido_1'].strip(' '),
                                                                      c['cliente__apellido_2']).strip(' '),
                                          'direccion': '{} #{}'.format(c['calle'].strip(' '),
                                                                       str(c['numero_puerta']).strip(' ')),
                                          'localidad': c['localidad'].strip(' ')})
        context['clientes'] = list_cliente_research
        context['cant_res'] = len(list_cliente_research)
        context['cant_res_porc'] = len(list_cliente_research)

    except Exception as e:
        log.error(str(e))
        pass
    return render_to_response('data_admin/accion_clientes/_table_resultado_clientes.html', context)


def del_allclientes_cfg(request):
    context = RequestContext(request)

    _codigo = request.POST['codigo_config']

    _cli = []

    try:

        _cli = ConfigAccion_Cliente.objects. \
            filter(codigo_config_accion_cabe=_codigo)

        if len(_cli) > 0:

            _cli.delete()

            # Se borran los filtros asignados a la acción

            _conf = ConfigAccion_Cabe.objects.get(codigo=_codigo)

            _conf.filtros_clientes = None

            _conf.save()

            return HttpResponse(status=200)

        else:

            return HttpResponse(status=300)

    except Exception as e:

        log.error(str(e))

        pass

    # return HttpResponse(status=500)


def asign_masivo_clien_aleatorio(request):
    _codigo = request.POST['codigo_config']
    _cantidad = request.POST['cantidad']
    _porcentaje = request.POST['porcentaje']
    _oficina = request.POST['oficina']
    _tipo_filtro = request.POST['tipo_filtro']
    _fecha_hoy = datetime.today()
    _usuario_asignacion = request.user
    filtros = {}
    try:

        if _tipo_filtro == "0":

            _tipo_filtro = 'Filtro particular'

        else:

            _tipo_filtro = 'Asignacion Masiva'

        if _porcentaje:
            of = PuntoDeSuministro.objects.filter(rutasum_id__oficina=_oficina).values('cliente').distinct().count()
            porc = float(of) * float(_porcentaje) * 0.01
            porc_final = int(porc)
            filtros = {'tipo_filtro': _tipo_filtro, 'contratista': _oficina, 'nis': '', 'nic': '',
                       'porcentaje': porc_final, 'cantidad': '', 'itinerarios seleccionados': ''}

            json_object = json.dumps(filtros)

            ConfigAccion_Cabe.objects.filter(codigo=_codigo).update(filtros_clientes=str(json_object))

            i = 0
            while porc_final != 0:

                if porc_final > 10000:
                    i = 10000
                else:
                    i = porc_final

                with connection.cursor() as cursor:
                    cursor.callproc('sp_insert_clientesconfig',
                                    params=[_oficina, _codigo, i, _fecha_hoy, _usuario_asignacion.pk])

                porc_final -= i

            return HttpResponse(status=200)  # envio el count hacia el html
        else:
            cantidad = int(_cantidad)
            filtros = {'tipo_filtro': _tipo_filtro, 'contratista': _oficina, 'nis': '', 'nic': '',
                       'porcentaje': '', 'cantidad': cantidad, 'itinerarios seleccionados': ''}

            i = 0
            while cantidad != 0:

                if cantidad > 10000:
                    i = 10000
                else:
                    i = cantidad

                with connection.cursor() as cursor:
                    cursor.callproc('sp_insert_clientesconfig',
                                    params=[_oficina, _codigo, i, _fecha_hoy, _usuario_asignacion.pk])

                cantidad -= i

        json_object = json.dumps(filtros)

        ConfigAccion_Cabe.objects.filter(codigo=_codigo).update(filtros_clientes=str(json_object))

        return HttpResponse(status=200)  # envio el count hacia el html

    except Exception as e:
        log.error(str(e))
        pass


# REPORTE DE AUDITORIA DE LECTURA--------------------------------------------------------
@login_required(login_url=settings.LOGIN_PAGE)
def reporte_auditoria_lect(request):  # main page
    context = RequestContext(request)

    cfgs = ConfigAccion_Cabe.objects.values('codigo', 'descripcion')

    configuraciones = []

    for c in cfgs:
        configuraciones.append({'id_config': c['codigo'], 'desc': c['descripcion']})

    context['configs'] = configuraciones

    return render_to_response('reportes/reporte_auditoria_lect/Reporte.html', context)


def reporte_auditoria_lect_getreporte(request):
    context = RequestContext(request)
    of = request.POST['id_oficina']  # ema o bat
    ptosum = request.POST['ptosum']
    ods_no_trabajadas = request.POST['ods_no_trab']
    fecha_d = request.POST['fh_desde']
    fecha_h = request.POST['fh_hasta']
    tecnico = request.POST['tecnico']
    _rutasum_id = request.POST['rutasum_id']
    cant_filtro = request.POST['filtros[cant]']
    porc_filtro = request.POST['filtros[porc]']
    cfg = request.POST['cfg']
    url = request.POST['url']
    try:
        _lst_rutas = ''
        if _rutasum_id != '':
            _lst_rutas = _rutasum_id.split(',')
        _reporte = reporte_controller()
        _reporte.oficina = of
        _reporte.ods_no_trabajadas = ods_no_trabajadas
        _reporte.fecha_desde = fecha_d
        _reporte.fecha_hasta = fecha_h
        _reporte.ptosum = ptosum
        _reporte.tecnico = tecnico
        _reporte.ruta = _lst_rutas
        _reporte.cantidad = cant_filtro
        _reporte.porcentaje = porc_filtro
        _reporte.cfg = cfg
        _reporte.url = url

        _resultado = _reporte.getReportData_rpt_auditoria_lect()

        context['result'] = _resultado

        if len(_resultado) > 0:

            return render_to_response('reportes/reporte_auditoria_lect/tabla_resultado.html', context)

        else:

            return HttpResponse(status=301)


    except Exception as e:
        log.error(str(e))
        return HttpResponse(status=500)


def get_tecnicos_from_oficina(request):
    context = RequestContext(request)
    of = request.POST['id_oficina']
    lista_tecnicos = []
    _tec_dicc = []
    try:
        lista_tecnicos = Tecnico.objects.select_related('terminal_portatil__oficina').values('codigo', 'nombre_1',
                                                                                             'apellido_1').filter(
            terminal_portatil__oficina=of)
        if len(lista_tecnicos) > 0:
            for l in lista_tecnicos:
                _tec_dicc.append({
                    'codigo': l['codigo'],
                    'nombre': l['nombre_1'] + " " + l['apellido_1']
                })
        _jsonres = json.dumps(_tec_dicc)  # dumps codifica la lista en archivo JSON
        return HttpResponse(_jsonres, content_type='application/json', status=200)
    except Exception as e:
        log.error(str(e))
        pass


def consulta_foto(request):
    context = RequestContext(request)
    nro_orden = request.POST['numos']
    try:
        _orden = Desc_Orden.objects.filter(orden_trabajo=nro_orden).values('orden_trabajo__desc_lectura__lectura')
        _foto = Desc_Foto.objects.filter(orden_trabajo=nro_orden)
        context['fotos'] = _foto
        context['lectura_registrada'] = _orden[0]['orden_trabajo__desc_lectura__lectura']
        return render_to_response('reportes/_consulta_foto.html', context)
    except Exception as e:
        log.error(str(e))
        pass


###### ------------------------- SOPORTE ------------------------------------ ######
@login_required(login_url=settings.LOGIN_PAGE)
def soporte_main(request):
    tareas = [{'valor': 'alert', 'tarea': 'Alerta'},
              {'valor': 'get_log', 'tarea': 'Pedir log'},
              {'valor': 'get_db3', 'tarea': 'Pedir db3'},
              {'valor': 'get_all', 'tarea': 'Pedir todo'},
              {'valor': 'commandSql', 'tarea': 'Comando sql'},
              {'valor': 'sql', 'tarea': 'Consulta sql'},
              {'valor': 'get_variable', 'tarea': 'Get variable'},
              {'valor': 'set_variable', 'tarea': 'Set variable'},
              {'valor': 'get_gps', 'tarea': 'Estado GPS'},
              {'valor': 'get_status', 'tarea': 'Estado general'}]

    context_dict = {'tareas': tareas}
    return render(request, 'soporte/soporte_push/_soporte.html', context_dict)

    '''  
    # Fetch the service account key JSON file contents
    try:
        cred = credentials.Certificate(settings.BASE_DIR+'/firebase-adminsdk.json')
        # Initialize the app with a service account, granting admin privileges
        firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://qorder-95b1a.firebaseio.com/'
        })
    except:
       pass
    # Get a database reference to our posts
    ref = db.reference('/devices')

    # Read the data at the posts reference (this is a blocking operation)
    result = ref.get()

    devices = []
    for k in result.keys():
        dev = {'device': k, 'token': result[k]['token']}
        devices.append(dev)

    context_dict = {'devices': devices}
    return render(request, 'soporte/_soporte.html', context_dict)
    '''


@login_required(login_url=settings.LOGIN_PAGE)
def soporte_get_terminales(request):
    try:

        id_oficina = request.POST['oficina']

        oficina = WorkUnit.objects.get(pk=id_oficina)

        terminales = TerminalPortatil.objects.filter(imei__isnull=False, oficina=oficina).values('alias',
                                                                                                 'cantidad_asignada',
                                                                                                 'cantidad_cargada',
                                                                                                 'pk', 'oficina_id',
                                                                                                 'estado',
                                                                                                 'fh_ultima_conexion',
                                                                                                 'androidID', 'token')

        for t in terminales:

            if t['fh_ultima_conexion'] is not None:
                t['fh_ultima_conexion'] = t['fh_ultima_conexion'].strftime("%d/%m/%y %H:%M:%S")

            t['estado'] = str(t['estado'])

        context_dict = {'devices': terminales}
        return render(request, 'soporte/soporte_push/_tabla_dispositivos.html', context_dict)

    except Exception as e:
        return HttpResponse(e, status=500)


@login_required(login_url=settings.LOGIN_PAGE)
def ejecutar_soporte(request):
    context = RequestContext(request)
    token = request.POST['token']
    method = request.POST['method']
    command = request.POST['command']
    titulo = request.POST['titulo']
    mensaje = request.POST['mensaje']
    vibrar = request.POST['vibrar']
    id = request.POST['id']
    id_terminal = request.POST['id_terminal']
    id = id + datetime.now().strftime("%Y%m%d%H%M%S")
    tipo = 0
    if method == 'alert':
        tipo = 3
        dataPayLoad = {'type': tipo, 'method': method, 'sql': command, 'id': id, 'titulo': titulo, 'cuerpo': mensaje,
                       'info': 'Información extra', 'vibrar': vibrar}
    else:
        dataPayLoad = {'type': tipo, 'method': method, 'sql': command, 'id': id}

    # clave Umbrella
    # serverToken = 'AAAATFplsRQ:APA91bEFfQ4IHafZ6GOH7gVlZre8HrHyiSSDOTmq_X-UP9nEZ_AdyCyWanirUdjB0LpeeeaTdjREENGwmC3BeHEhWrt83YC9S13pm_j4TIe2_d5W2FyUIovL3J2-NfKNECNKNJHMTCAH'
    # clave Qorden
    serverToken = 'AAAAXllscvE:APA91bE7hpnSUETsFCZhUvunOWuFs5CVDdW6GFP5a3twTjZgYGxP3lb91dXbyQCZGi2owHCXrWRilMAe8CEndPop2dUT-vqXZjsU-4iPFFobWs6f4obTjbCAXlXCDyuzJIat4ijEmzA9'
    # clave pushModule
    # serverToken = 'AAAA7bpDLpA:APA91bEDQOQ0rH_cDpG-B4IEtOllAVxmP5c-y-GKyTCroQSGlezvPRaHyS885asssznL6crYXQc7zEr7yhFVbTXtw5oH0zQsQmkif7jLgHvyeJQ2PBzoxc5wngWsDZc0JSFBTfyygbZv'
    # deviceToken = 'eHkYuMUmRrGjVZzTMuTASM:APA91bGbmiPvgJ-cMjS-epine3s302d5-qHgzxggnso7ni-l8M87qeetMegXolGqPsO6GEyMQ_2qdc0vExmXIezDTulhHfL4eGxhw9VtKlgZQltXx7UI8XBx4ky0q8aoXllsf8F8nswP'
    # deviceToken = 'fCw8grimLJY:APA91bGoH_TKzmWykP_hy5da_brOUNHZrV_q-r_VnVXIpXeKzK3qRNpX9gaiw_gv7sm7K3yG_HyvYQFSA5rqg5gk2u2xNpYVXNWKOrwvr2OvnCOMj8YLtXkW1lrnGhe-sTQ1kvOVYLs3'
    # token = 'fvpfkvV19VY:APA91bEcHJRsU5HmJ9pdpj8c4OD04qXoQg2JA36IJUrHcL6gFDhIQTMuqA4Pg_2jwOQcYcfgkbQj0-DeSYmGIHkwNWg3CgXFPOP7dxKUXf4j6vaWRh9sUcQAtxk2N-dt3_IR5F8DYuwa'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=' + serverToken,
    }

    body = {

        'to':
            token,
        'priority': 'high',
        'data': dataPayLoad
    }

    response = requests.post("https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(body))
    print(response.status_code)
    fecha_hora = datetime.now()
    msg = Mensajes_Dispositivos(id_mensaje=id, alias_dispositivo=id_terminal, fecha_hora_comando=fecha_hora,
                                tipo_mensaje=method, usuario_comando=request.user, comando_enviado=command)
    msg.save()
    print(response.json())
    # return HttpResponse(json.dumps(response.json()), content_type='application/json', status=response.status_code)
    if response.status_code == 200:
        return HttpResponse(json.dumps({'message_id': id, 'response': response.json()}),
                            content_type='application/json', status=response.status_code)
    return response.status_code


@login_required(login_url=settings.LOGIN_PAGE)
def get_soporte(request):
    id = request.POST['message_id']
    valores = []
    nuevo = ''
    tipo = ''
    try:
        msg = Mensajes_Dispositivos.objects.get(id_mensaje=id)
        if msg.respuesta == None:
            nuevo = json.loads('{ "Error" : "No se obtuvo respuesta a la solicitud" }')
        else:

            resultado = json.loads(msg.respuesta)
            tipo = resultado[0]['method']
            for k in resultado[0].keys():
                if k == 'mensaje':

                    if tipo == 'get_log' or tipo == 'get_db3' or tipo == 'get_all':
                        if resultado[0]['mensaje'].startswith('OK|'):
                            nuevo = resultado[0]['mensaje'][3:]
                        else:
                            nuevo = json.loads('{ "' + resultado[0]['method'] + '":"Error recibiendo archivo "}')

                    else:
                        try:
                            nuevo = json.loads('{ "' + resultado[0]['method'] + '":' + resultado[0]['mensaje'] + '}')
                        except:
                            nuevo = json.loads('{ "' + resultado[0]['method'] + '":" "}')
                else:
                    # dev = {k : resultado[0][k]}
                    dev = k + ":" + resultado[0][k]
                    valores.append(dev)

    except Exception as e:
        nuevo = json.loads('{ "Error"' + ':' + '"{}'.format(e) + '"}')
    '''
    for k in resultado.keys():

        if k=='mensaje':
            try:
                nuevo = json.loads('{ "'+resultado['method']+'":' + resultado[k]+ '}')
            except:
                nuevo = json.loads('{ "'+resultado['method']+'":" "}')
        else:
           dev = {k : resultado[k]}
           valores.append(dev)
    '''
    '''
    try:
      # Fetch the service account key JSON file contents
      cred = credentials.Certificate(settings.BASE_DIR+'/firebase-adminsdk.json')
      # Initialize the app with a service account, granting admin privileges
      firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://qorder-95b1a.firebaseio.com/'
      })
    except:
       pass
    ref = db.reference('/mensajes')
    result = ref.order_by_key().equal_to(message_id).get()
    print(result)
    valores=[]
    clave = result[message_id]
    for k in clave.keys():

        if k=='mensaje':
            try:
                nuevo = json.loads('{ "'+clave['method']+'":' + clave[k]+ '}')
            except:
                nuevo = json.loads('{ "'+clave['method']+'":" "}')
        else:
           dev = {k : clave[k]}
           valores.append(dev)
    '''
    context_dict = {'resultado': json.dumps(valores), 'res': nuevo, 'tipo': tipo}
    return render(request, 'soporte/soporte_push/_result_soporte.html', context_dict)


def download_file(request):
    try:
        # fill these variables with real values
        fl_path = request.POST['archivo']

        lst_archivo = fl_path.split("/")

        nombre_archivo = lst_archivo[-1]

        with open(fl_path, "rb") as f:
            bytes = f.read()
            encoded = base64.b64encode(bytes)

        data = {}

        # ASIGNAMOS LAS VARIABLES AL OBJETO DATA PARA DEVOLVERLO
        data["data"] = encoded.decode('ascii')

        # data["fecha_hora"] = fecha_hora_creacion
        data["nombre_archivo"] = nombre_archivo

        final_data = json.dumps(data)

        return HttpResponse(final_data, content_type='application/json', status=200)
        # response['Content-Disposition'] = "attachment; filename=%s" % filename

    except Exception as e:

        return HttpResponse(e, status=500)

