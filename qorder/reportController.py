from cgitb import text
import json
from optparse import Values
import random
from django.db import connection
from django.db.models.query_utils import Q
from django.db.models import Max
from qorder.models import *
from datetime import datetime, time


class reporte_controller(object):
    def __init__(self):
        self.oficina = ""
        self.fecha_desde = ""
        self.fecha_hasta = ""
        self.tecnico = ""
        self.ptosum = ""
        self.ruta = ""
        self.cantidad = ""
        self.porcentaje = ""
        self.cfg = ""
        self.url = ""

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)

    def getReportData_rpt_auditoria_lect(self):
        # Variables
        id_centro = self.oficina
        ods_no_trabjadas = self.ods_no_trabajadas
        fecha_d = self.fecha_desde
        fecha_h = self.fecha_hasta
        tec = self.tecnico
        ptosum = self.ptosum
        _ruta = self.ruta
        _ordenes = []
        codigos_registros = []
        #filtros
        cantidad = self.cantidad
        porcentaje = self.porcentaje
        cfg = self.cfg
        try:
            di = datetime.strptime(fecha_d, '%Y-%m-%d')
            df = datetime.strptime(fecha_h, '%Y-%m-%d')
            d_f = datetime.combine(df, time.max)  # 23:59
            q = Q()
            q &= Q(orden_trabajo__ruta__oficina=id_centro)
            q &= Q(fecha_asignacion__gte=di)
            q &= Q(fecha_asignacion__lte=d_f)

            q.add(Q(tiene_auditoria=True), Q.AND)


            if ods_no_trabjadas != 'true':

                q.add(Q(descargado=True), Q.AND)


            if tec != '0':

                q.add(Q(orden_trabajo__tecnico=tec), Q.AND)

            if ptosum != '':

                q.add(Q(orden_trabajo__punto_suministro=ptosum), Q.AND)

            if _ruta != '':

                if _ruta[0] != 'all':

                    q.add(Q(orden_trabajo__ruta__itinerario__in=_ruta), Q.AND)


            if cfg:

                # codigos_ordenes = ExtensionDatos.objects.filter(tabla_extension="resguardo_terreno",campo_extension="codigo_accion",valor=cfg).values_list("clave_registro",flat=True)

                cod_registros = ExtensionDatos.objects.filter(tabla_extension="resguardo_terreno",campo_extension="codigo_accion",valor=cfg).values("clave_registro")

                
                for cod in cod_registros:

                    codigos_registros.append(int(cod['clave_registro']))


                if len(codigos_registros) > 0:

                    codigos_registros = list(dict.fromkeys(codigos_registros))


                q.add(Q(pk__in = codigos_registros), Q.AND)


            _num_ods_sin_filtrar = Resguardo_Terreno.objects.filter(q).values_list("orden_trabajo",flat=True)

            _num_ods_sin_filtrar = list(dict.fromkeys(_num_ods_sin_filtrar))

            _parametro_sp = []

            if len(_num_ods_sin_filtrar) > 0:

                _texto_parametro = ''

                for _num_od in _num_ods_sin_filtrar:

                    _texto_parametro += ',' + _num_od

                _texto_parametro = _texto_parametro[1:]

                _parametro_sp.append(_texto_parametro)


                with connection.cursor() as cursor:

                    cursor.callproc('sp_rpt_auditoria_lecturas', params=[_parametro_sp])

                    _ods = cursor.fetchall()

            else:

                _ods = []


            # _ods = Resguardo_Terreno.objects.select_related("orden_trabajo","punto_suministro")\
            #             .values("pk","nombre_apellido","orden_trabajo","numero_ruta","ciclo","itinerario","fecha_descarga",\
            #             "punto_suministro__aparato","orden_trabajo__desc_lectura__cantidad_intentos",\
            #             "orden_trabajo__desc_lectura__lectura","orden_trabajo__desc_lectura__consumo",\
            #             "estado")\
            #             .filter(q)

            # Se filtra por cantidad o porcentaje si se seleccionó

            ods_filtradas = []

            if cantidad:

                _l_new = []

                _l_new = sorted(_ods,key=lambda i:i[2])

                sort_l = list(_l_new)

                random.shuffle(sort_l)

                if len(sort_l) == 0:

                    return ods_filtradas

                else:

                    cant = int(cantidad)

                    ods_filtradas = []

                    for l in sort_l:

                        if len(ods_filtradas) < cant:

                            ods_filtradas.append(l)


            elif porcentaje:

                _l_new = []

                _l_new = sorted(_ods,key = lambda i: i[2])

                sort_l = list(_l_new)

                random.shuffle(sort_l)

                if len(sort_l) == 0:

                    return ods_filtradas

                else:

                    cantidadreturn = len(sort_l)

                    porc = int(porcentaje)

                    ce = porc*cantidadreturn

                    ce2 = ce*0.01

                    ce2_converted = int(ce2)

                    lista_retorno = []

                    for l in sort_l:

                        if len(ods_filtradas) < ce2_converted:

                            ods_filtradas.append(l)
            else:

                ods_filtradas = _ods


            for o in ods_filtradas:

                _estado = ''

                if o[11] == 1:

                    _estado = 'Importada'

                elif o[11] == 3:
    
                    _estado = 'Asignada'

                elif o[11] == 7:
    
                    _estado = 'Cargada'

                elif o[11] == 265:
    
                    _estado = 'Trabajada'

                elif o[11] == 777:
    
                    _estado = 'Exportada'

                else:

                    _estado = 'No definido'

                tiene_foto = '0'

                fotos = Desc_Foto.objects.filter(orden_trabajo=o[2]).values('foto')

                if len(fotos) > 0:

                    tiene_foto = '1'

                anomalia = Desc_Anomalia.objects.filter(orden_trabajo = o[2]).first()

                _fecha_lectura = ''

                _hora_lectura = ''
                
                if o[6] is not None:

                    _fecha_lectura = str(o[6].strftime("%d/%m/%Y"))[:10].ljust(10)

                    _hora_lectura = o[6].strftime("%H:%M")



                if cfg:

                    codigo_accion = ExtensionDatos.objects.filter(tabla_extension="resguardo_terreno",clave_registro=o[0],campo_extension="codigo_accion").values('id','valor')

                    codigo_accion_filtrado = ExtensionDatos.objects.filter(tabla_extension="resguardo_terreno",clave_registro=o[0],campo_extension="codigo_accion",valor=cfg).values('id','valor')

                    posiciones_codigos = []

                    for caf in codigo_accion_filtrado:

                        for index, ca in enumerate(codigo_accion):

                            if caf['id'] == ca['id']:

                                posiciones_codigos.append(index)

                    descripcion_accion = ExtensionDatos.objects.filter(tabla_extension="resguardo_terreno",clave_registro=o[0],campo_extension="descripcion_accion").values('valor')

                    for i in posiciones_codigos:
    
                        _ordenes.append({
                            'num_os': o[2],
                            'ruta': o[3],
                            'ciclo': o[4],
                            'itinerario': o[5],
                            'estado': _estado,
                            'codigo_accion': codigo_accion[i]['valor'],
                            'descripcion_accion': descripcion_accion[i]['valor'],
                            'fh_lectura': _fecha_lectura,
                            'hora_lectura': _hora_lectura,
                            'punto_suministro': o[12],
                            'aparato': o[7],
                            'cantidad_intentos': o[8],
                            'lectura': o[9],
                            'consumo': o[10],
                            'foto': tiene_foto,
                            'anomalia': anomalia.id_anomalia.id_anomalia+'-'+anomalia.id_anomalia.descripcion if anomalia is not None  else None,
                            'url':self.url+'foto?numOrden='+o[2]
                        })

                else:

                    codigo_accion = ExtensionDatos.objects.filter(tabla_extension="resguardo_terreno",clave_registro=o[0],campo_extension="codigo_accion").values("valor")

                    descripcion_accion = ExtensionDatos.objects.filter(tabla_extension="resguardo_terreno",clave_registro=o[0],campo_extension="descripcion_accion").values("valor")

                    for i in range(len(codigo_accion)):
        
                        _ordenes.append({
                            'num_os': o[2],
                            'ruta': o[3],
                            'ciclo': o[4],
                            'itinerario': o[5],
                            'estado': _estado,
                            'codigo_accion': codigo_accion[i]['valor'],
                            'descripcion_accion': descripcion_accion[i]['valor'],
                            'fh_lectura': _fecha_lectura,
                            'hora_lectura': _hora_lectura,
                            'punto_suministro': o[12],
                            'aparato': o[7],
                            'cantidad_intentos': o[8],
                            'lectura': o[9],
                            'consumo': o[10],
                            'foto': tiene_foto,
                            'anomalia': anomalia.id_anomalia.id_anomalia+'-'+anomalia.id_anomalia.descripcion if anomalia is not None  else None,
                            'url':self.url+'foto?numOrden='+o[2]
                        })                


            return _ordenes


        except Exception as e:
            print(e)
            return

    # def getReportData_rpt_auditoria_lect(self):
    #     # Variables
    #     id_centro = self.oficina
    #     fecha_d = self.fecha_desde
    #     fecha_h = self.fecha_hasta
    #     tec = self.tecnico
    #     ptosum = self.ptosum
    #     _ruta = self.ruta
    #     _ordenes = []
    #     _desc_orden = []
    #     #filtros
    #     cantidad = self.cantidad
    #     porcentaje = self.porcentaje
    #     cfg = self.cfg
    #     try:
    #         di = datetime.strptime(fecha_d, '%Y-%m-%d')
    #         df = datetime.strptime(fecha_h, '%Y-%m-%d')
    #         d_f = datetime.combine(df, time.max)  # 23:59
    #         q = Q()
    #         q &= Q(orden_trabajo__ruta__oficina=id_centro)
    #         q &= Q(fh_descarga__gte=di)
    #         q &= Q(fh_descarga__lte=d_f)
    #         if tec == '0' and ptosum == '' and _ruta == '':
    #             # orden_trabajo__ruta__oficina = id_centro,fh_descarga__gte = di,fh_descarga__lte = d_f
    #             None
    #         elif tec != '0' and ptosum == '' and _ruta == '':
    #             q &= Q(orden_trabajo__tecnico=tec)
    #         elif tec == '0' and ptosum != '' and _ruta == '':
    #             q &= Q(orden_trabajo__punto_suministro=ptosum)
    #         elif tec == '0' and ptosum == '' and _ruta != '':
    #             if _ruta[0] != 'all':
    #                 q &= Q(orden_trabajo__ruta__itinerario__in=_ruta)
    #         elif tec != '0' and ptosum != '' and _ruta == '':
    #             q &= Q(orden_trabajo__tecnico=tec,
    #                    orden_trabajo__punto_suministro=ptosum)
    #         elif tec != '0' and ptosum == '' and _ruta != '':
    #             if _ruta[0] != 'all':
    #                 q &= Q(orden_trabajo__tecnico=tec,
    #                     orden_trabajo__ruta__itinerario__in=_ruta)
    #             else:
    #                 q &= Q(orden_trabajo__tecnico=tec)
    #         elif tec == '0' and ptosum != '' and _ruta != '':
    #             if _ruta[0] != 'all':
    #                 q &= Q(orden_trabajo__punto_suministro=ptosum,
    #                     orden_trabajo__ruta__itinerario__in=_ruta)
    #             else:
    #                 q &= Q(orden_trabajo__punto_suministro=ptosum)
    #         else:
    #             if _ruta[0] != 'all':
    #                 q &= Q(orden_trabajo__tecnico=tec, orden_trabajo__punto_suministro=ptosum,
    #                     orden_trabajo__ruta__itinerario=_ruta)
    #             else:
    #                 q &= Q(orden_trabajo__tecnico=tec, orden_trabajo__punto_suministro=ptosum)
            
    #         q2 = Q()

    #         if cfg:

    #             num_contrats = ConfigAccion_Cliente.objects.filter(codigo_config_accion_cabe = cfg).values('codigo_cliente')

    #             res = []

    #             for nc in num_contrats:

    #                 res.append(nc['codigo_cliente'])

    #             q2 &= Q(orden_trabajo__punto_suministro__num_contrato__in = res)



    #         _desc_orden = Desc_Orden.objects.select_related('orden_trabajo__ruta',
    #             'orden_trabajo__punto_suministro__aparato', 'orden_trabajo__desc_lectura__cantidad_intentos', 'orden_trabajo__desc_lectura__consumo','orden_trabajo__desc_foto').values('orden_trabajo', 'orden_trabajo__ruta__ruta',
    #             'orden_trabajo__ruta__ciclo', 'orden_trabajo__ruta__itinerario', 'fh_descarga', 'secuencia_real',
    #             'orden_trabajo__punto_suministro__aparato', 'orden_trabajo__desc_lectura__cantidad_intentos', 'orden_trabajo__desc_lectura__lectura', 'orden_trabajo__desc_lectura__consumo', 'orden_trabajo').filter(q,
    #             q2,orden_trabajo__desc_foto__descripcion_foto = 'Foto AUD')
    #         for d in _desc_orden:
    #             tiene_ = '0'
    #             val = Desc_Foto.objects.filter(
    #                 orden_trabajo=d['orden_trabajo']).values('foto')
    #             if len(val) > 0:
    #                 tiene_ = '1'
    #             anomalia = Desc_Anomalia.objects.filter(orden_trabajo = d['orden_trabajo']).first()
    #             _ordenes.append({
    #                     'num_os': d['orden_trabajo'],
    #                     'ruta': d['orden_trabajo__ruta__ruta'],
    #                     'ciclo': d['orden_trabajo__ruta__ciclo'],
    #                     'itinerario': d['orden_trabajo__ruta__itinerario'],
    #                     'fh_lectura': str(d['fh_descarga'].strftime("%Y/%m/%d"))[:10].ljust(10),
    #                     'hora_lectura': d['fh_descarga'].strftime("%H:%M"),
    #                     'secuencia': d['secuencia_real'],
    #                     'aparato': d['orden_trabajo__punto_suministro__aparato'],
    #                     'cantidad_intentos': d['orden_trabajo__desc_lectura__cantidad_intentos'],
    #                     'lectura': d['orden_trabajo__desc_lectura__lectura'],
    #                     'consumo': d['orden_trabajo__desc_lectura__consumo'],
    #                     'foto': tiene_,
    #                     'anomalia': anomalia.id_anomalia.id_anomalia+'-'+anomalia.id_anomalia.descripcion if anomalia is not None  else None,
    #                     'url':self.url+'foto?numOrden='+d['orden_trabajo']
    #                 })
    #         lista_nueva = []
    #         if cantidad:
    #             _l_new = []
    #             _l_new = sorted(_ordenes,key=lambda i:i['num_os'])
    #             sort_l = list(_l_new)
    #             random.shuffle(sort_l)
    #             if len(sort_l) == 0:
    #                 return lista_nueva
    #             else:
    #                 cant = int(cantidad)
    #                 lista_nueva = []
    #                 for l in sort_l:
    #                     if len(lista_nueva) < cant:
    #                         lista_nueva.append(l)
    #         elif porcentaje:
    #             _l_new = []
    #             _l_new = sorted(_ordenes,key = lambda i: i['num_os'])
    #             sort_l = list(_l_new)
    #             random.shuffle(sort_l)
    #             if len(sort_l) == 0:
    #                 return lista_nueva
    #             else:
    #                 cantidadreturn = len(sort_l)
    #                 porc = int(porcentaje)
    #                 ce = porc*cantidadreturn
    #                 ce2 = ce*0.01
    #                 ce2_converted = int(ce2)
    #                 lista_nueva = []
    #                 for l in sort_l:
    #                     if len(lista_nueva) < ce2_converted:
    #                         lista_nueva.append(l)
    #         else:
    #             lista_nueva = _ordenes
    #         return lista_nueva
    #     except Exception as e:
    #         print(e)
    #         return

