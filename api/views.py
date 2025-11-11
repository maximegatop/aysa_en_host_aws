from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework.decorators import parser_classes
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from qorder.models import  * 
import json
from datetime import timedelta, date, datetime
from api.log import *
from api.obj import *
from api.base import *
import os





@api_view(['GET','POST'])
def getflag(request):
    dictionary = {'test':'1'}
    return Response(dictionary)

@api_view(['GET','POST'])
def getfechahora(request):

    import datetime as dt

    _fechahora = dt.datetime.now()
    _result = []

    _result.append(_fechahora.strftime('%Y'))
    _result.append(_fechahora.strftime('%m'))
    _result.append(_fechahora.strftime('%d'))
    _result.append(_fechahora.strftime('%H'))
    _result.append(_fechahora.strftime('%M'))
    _result.append(_fechahora.strftime('%S'))
    _result.append(str(_fechahora.weekday()))

    #creo un diccionario con la respuesta
    _jsonres = {'jsondata': _result, 'status': 200, 'statusMessage': 'OK'}

    return Response(_jsonres,status=status.HTTP_200_OK)



@api_view(['GET','POST'])
def getcodigosiddesc(request):
    _log=Logger()
    _parametro=Parametro.objects.get(pk='P_TP_PATH_WS_LOG')
    path=_parametro.valor_1
    path1=path
    _log.logsetlevel('DEBUG')
    _log.setpath(path1)
        
    _log.Error( 'request 1 {}'.format(request))	
    _list = []
    codigo=''
    if request.method=='POST':
        codigo=request.data['cod']
        valor = Codigo.objects.get(pk=codigo)
        _jsonres ={'datacod':{'codigo':valor.codigo ,'descripcion':valor.descripcion},'status':200}
    else:
        valor=Codigo.objects.all()
        for cod in valor:

            _list.append({'codigo':cod.codigo ,'descripcion':cod.descripcion})

        _jsonres ={'datacod':_list,'status':200}
        _log=Logger()
        _parametro=Parametro.objects.get(pk='P_TP_PATH_WS_LOG')
        path=_parametro.valor_1
        path1=path
        _log.logsetlevel('DEBUG')
        _log.setpath(path1)
        _log.Debug( 'ERROR {}'.format(_jsonres))
        
    return Response(_jsonres)

  
@api_view(['GET','POST'])
def getdata(request):
    _log=Logger()
    _parametro=Parametro.objects.get(pk='P_TP_PATH_WS_LOG')
    path=_parametro.valor_1
    path1=path
    _log.logsetlevel('DEBUG')
    _log.setpath(path1)
    print(request)
    _list=[]
    func=''
    param=''
    if request.method=='POST':
        data = JSONParser().parse(request)
        _log=Logger()
        _parametro=Parametro.objects.get(pk='P_TP_PATH_WS_LOG')
        path=_parametro.valor_1
        path1=path
        _log.logsetlevel('DEBUG')
        _log.setpath(path1)
        
        func=data.get('Funcion','0')
        param=data.get('Parametro','')
    res={}
    if func=='1':
        res=getdate ()
    if func=='2':
        res=test_connection()
    if func=='3':
        res=getflagConversion(param)
    if func=='4':
        res=getflag(param)
    if func=='5':
        res=registrarDispositivoMovil(param)
    if func=='6':
        res=setUpdEstadoOrdenesCargadas(param)
    if func=='7':
        res=setUpdEstadoOrdenAnulada(param)
    if func=='8':
        res=getpasswordqorder()
    if func=='9':
        res=generarDatos_Online(param)
    if func=='10':
        res=enviarActividadUsuario(param)
    if func=='11':
        res=enviarPuntosGps(param)
    if func=='12':
        res=getNuevasAsignaciones(param)
    if func=='13':
        res=setUpdFlagSolicitudDescarga(param)
    if func=='14':
        res=logsetpath(param)
    if func=='15':
        res=setPasswordUsuario(param)
    
    
    
    
    return Response(res)

def getpasswordqorder():

    _param = Parametro.objects.get(pk='P_PASSWORD_QORDER')
    print(_param)
    _jsonres = {'status':200,'jsonData':_param.valor_1,'statusMenssage':'OK'}

    return _jsonres


def getdate():
    _list=[]
    _jsonres={'status':200,'jsonData':'Paso','statusMenssage':'OK'}
    return _jsonres

def getflagConversion(param):
    _list=[]
    print(param)                        
    deserializado = json.dumps(param)
    variable=json.loads(deserializado)
    print('variable {}'.format(variable))
 #   var=deserializado.replace("'","\"")
 #   print(var) 
    NumSerie=variable['numero_serie']
    Version=variable['version']

    _parametro=Parametro.objects.get(pk='P_TP_PATH_WS_LOG')
    path=_parametro.valor_1
    path1=path.replace("%NUM_SERIE%",NumSerie) 

    _log=Logger()    

    _jsonres={'status':200,'jsonData':variable['numero_serie'],'statusMenssage':'OK'}

    try:
        _tp=TerminalPortatil.objects.get(numero_serie=NumSerie)
        _tecnico=Tecnico.objects.get(terminal_portatil=_tp)

        print('tecnico {}'.format(_tecnico))
        print('_tp {}'.format(_tp))
    except Exception as e:
        print("Excepcion {}".format(e))


    _flag1_GetOrdenes_sinBorrarDB = True
    _flag2_BorrarDB = False
    _flag4_NuevasOrdenesAsignadas = False
    _flag8_ResetDeContraseña = False
    _flag16_UltimaPosicionGPS = True
    _flag32_ObtenerTodo = False
    _flag64_NuevaVersion = False
    #actualiza la fecha hora de la ultima conexion de la tp
    _tp.fh_ultima_conexion=datetime.now()
    _tp.save()
    print(_tp.fh_ultima_conexion.strftime('%Y%m%d %H%M%s'))
    #obtengo los flags del usuario de tp
    print(_tecnico.flag_reset_password)
    if _tecnico.flag_reset_password==1:

        _flag8_ResetDeContraseña=True
    print(_flag8_ResetDeContraseña)
    if _tecnico.flag_descarga_total==1:
        _flag32_ObtenerTodo=True
    if _tecnico.flag_liberar_datos==1:
        _flag2_BorrarDB=True

    cantidad=OrdenDeTrabajo.objects.filter(tecnico_id=_tecnico,estado=3,flag_asignacion_guardada=1).count()
    print(cantidad)
    if cantidad>0:
        _flag4_NuevasOrdenesAsignadas=True

    

    try:
        parametro=Parametro.objects.get(pk='P_ULT_VERSION_ANDR')
        print(parametro.valor_1)
        if parametro.valor_1==Version:
            _flag64_NuevaVersion=False
        else:
            _flag64_NuevaVersion=True


        if _tp.version_instalada is None:
           _tp.version_instalada=Version
           _tp.fecha_actualizacion=datetime.now()
           _tp.save()

        if _tp.version_instalada is not None and parametro.valor_1 != Version:
            _tp.version_instalada=Version
            _tp.fecha_actualizacion=datetime.now()
            _tp.save() 

        _nResult=''
        if TipoSync == '0' and _flag64_NuevaVersion==True:

            _nResult = '115'

            _jsonres={'status':200,'jsonData':_nResult,'statusMenssage':'OK'}

            _log.logsetlevel('DEBUG')
    
            _log.setpath(path1)

            _log.Debug( _tp + 'FLAG TP Valor:{}'.format(_nResult))

            return _jsonres

                    
        if TipoSync == '0' and _flag2_BorrarDB == True and _flag32_ObtenerTodo == False:
            _nResult = '2'
            _jsonres={'status':200,'jsonData':_nResult,'statusMenssage':'OK'}
            return _jsonres

            _log.logsetlevel('DEBUG')
    
            _log.setpath(path1)

            _log.Debug( _tp + 'FLAG TP Valor:{}'.format(_nResult))
        
        
        if TipoSync == '0' and _flag2_BorrarDB == True and _flag32_ObtenerTodo == True and _flag1_GetOrdenes_sinBorrarDB == True and _flag16_UltimaPosicionGPS == True:
            
            _nResult = '51'

            _jsonres={'status':200,'jsonData':_nResult,'statusMenssage':'OK'}

            _log.logsetlevel('DEBUG')
    
            _log.setpath(path1)

            _log.Debug( _tp + 'FLAG TP Valor:{}'.format(_nResult))

            return _jsonres


        if _flag1_GetOrdenes_sinBorrarDB == True and _flag2_BorrarDB == False and _flag32_ObtenerTodo == False and _flag4_NuevasOrdenesAsignadas == False and _flag8_ResetDeContraseña == False and _flag16_UltimaPosicionGPS == True :

            _nResult = '17'

        if _flag1_GetOrdenes_sinBorrarDB == True and _flag2_BorrarDB == False and _flag32_ObtenerTodo == False and _flag4_NuevasOrdenesAsignadas == True and _flag8_ResetDeContraseña == False and _flag16_UltimaPosicionGPS == True :

        
            _nResult = '21'

        if  _flag1_GetOrdenes_sinBorrarDB == True and _flag2_BorrarDB == False and _flag32_ObtenerTodo == False and _flag4_NuevasOrdenesAsignadas == True and _flag8_ResetDeContraseña == True and _flag16_UltimaPosicionGPS == True:
        
            _nResult = '29'

        if _flag1_GetOrdenes_sinBorrarDB == True and _flag2_BorrarDB == False and  _flag32_ObtenerTodo == False and _flag4_NuevasOrdenesAsignadas == False and _flag8_ResetDeContraseña == True and _flag16_UltimaPosicionGPS == True: 
        
            _nResult = '25'


        
        _jsonres={'status':200,'jsonData':_nResult,'statusMenssage':'OK'}

        _log.logsetlevel('DEBUG')
    
        _log.setpath(path1)

        _log.Debug( _tp + 'FLAG TP Valor:{}'.format(_nResult))     
    except Exception as e:
        print("Excepcion {}".format(e))
    return _jsonres


def setUpdFlagSolicitudDescarga(param):
    deserializado = json.dumps(param)
    variable=json.loads(deserializado)
    print('variable {}'.format(variable))
 #   var=deserializado.replace("'","\"")
 #   print(var) 
    NumSerie=variable['numero_serie']

    try:
        _tp=TerminalPortatil.objects.get(numero_serie=NumSerie)
        _tecnico=Tecnico.objects.get(terminal_portatil=_tp)

        _tecnico.flag_descarga_total='0'
        _tecnico.flag_liberar_datos='0'
        _tecnico.save()
        _jsonres={'status':200,'jsonData':'','statusMenssage':'OK'}

         
        print('tecnico {}'.format(_tecnico))
        print('_tp {}'.format(_tp))
    except Exception as e:
        _jsonres={'status':500,'jsonData':'','statusMenssage':'OK'}
        print("Excepcion {}".format(e))
    return _jsonres


def registrarDispositivoMovil(param):
    deserializado = json.dumps(param)
    variable=json.loads(deserializado)
    print('variable {}'.format(variable))
 #   var=deserializado.replace("'","\"")
 #   print(var)
    NumSerie=variable['numero_serie']
    Version=variable['version']
    Plataforma=variable['Plataforma']
    alias=variable['alias']
    estado=variable['estado']


    _parametro=Parametro.objects.get(pk='P_TP_PATH_WS_LOG')
    path=_parametro.valor_1
    path1=path.replace("%NUM_SERIE%",NumSerie)
    _log=Logger()
    _jsonres={}
    try:
        

        try:
            _tp=TerminalPortatil.objects.get(terminal_portatil=NumSerie)
            _jsonres={'status':500,'jsonData':'','statusMenssage':'El dispositivo m�vil ya se encuentra registrado'}

            _log.logsetlevel('ERROR')  
            _log.setpath(path1)
            _log.Error('El dispositivo m�vil ya se encuentra registrado')

            return _jsonres
        except Exception as e:

            _tp=TerminalPortatil()
            _tp.numero_serie=NumSerie
            _tp.version_instalada=Version
            _tp.plataforma=Plataforma
            _tp.alias=alias
            _tp.estado=estado
            _tp.fecha_actualizacion=datetime.now()
            _tp.save()



        _jsonres={'status':200,'jsonData':'','statusMenssage':'Dispositivo m�vil registrado con �xito'}
        _log.logsetlevel('INFO')  
        _log.setpath(path1)
        _log.Info('Dispositivo m�vil registrado con �xito')
    except Exception as e:
        _jsonres={'status':500,'jsonData':'','statusMenssage':'OK'}
        print("Excepcion {}".format(e))
    return _jsonres




def logsetpath(param):                          # Ruta del logger mas el mensaje a cargar
    deserializado = json.dumps(param)

    variable=json.loads(deserializado)

    NumSerie=variable['numero_serie']

    _tp=TerminalPortatil.objects.get(numero_serie=NumSerie)
    _parametro=Parametro.objects.get(pk='P_TP_PATH_WS_LOG')

    path=_parametro.valor_1

    path1=path.replace("%NUM_SERIE%",NumSerie) 

    print(path1)

    _log=Logger()

    _log.logsetlevel('DEBUG')
    
    _log.setpath(path1)

    _log.Debug('error')

    _jsonres={'status':200,'jsonData':NumSerie,'statusMenssage':'OK'}

    return _jsonres




def setPasswordUsuario(param):
    deserializado = json.dumps(param)
    print(deserializado)
    variable=json.loads(deserializado)

    NumSerie=variable['numero_serie']
    Idtecnico=variable['tecnico']
    NuevoPassword=variable['NuevoPassword']

    _parametro=Parametro.objects.get(pk='P_TP_PATH_WS_LOG')
    path=_parametro.valor_1
    path1=path.replace("%NUM_SERIE%",NumSerie) 

    _log=Logger()




    
    print(NumSerie)
    print(Idtecnico)
    print(NuevoPassword)
    try:
        _tp=TerminalPortatil.objects.get(numero_serie=NumSerie)
        _tecnico=Tecnico.objects.get(codigo=Idtecnico)
        print(_tp)
        print(_tecnico)



        _tecnico.flag_reset_password='0'
        _tecnico.password=NuevoPassword
        _tecnico.save()

        _jsonres={'status':200,'jsonData':[NumSerie,Idtecnico,NuevoPassword],'statusMenssage':'OK'}

        _log.logsetlevel('INFO')
    
        _log.setpath(path1)

        _log.Info('Se actualizo el password  del tecnico {} con el valor:{} '.format(Idtecnico ,NuevoPassword))        

         
    except Exception as e:

        _jsonres={'status':500,'jsonData':'','statusMenssage':'OK'}

        _log.logsetlevel('ERROR')
    
        _log.setpath(path1)

        _log.Error('Se actualizo el password  del tecnico {} con el valor:{} '.format(Idtecnico ,NuevoPassword)) 
       
        print("Excepcion {}".format(e))
    return _jsonres






def test_connection ():
    try:

        _jsonres={'status':200,'jsonData':'','statusMenssage':'OK'}


    except Exception as e:
        _jsonres={'status':500,'jsonData':'','statusMenssage':'OK'}

    return _jsonres


def getflag(param):
    deserializado = json.dumps(param)
    variable=json.loads(deserializado)
    print('variable {}'.format(variable))
    _parametro=Parametro.objects.get(pk='P_TP_PATH_WS_LOG')
    path=_parametro.valor_1
    path1=path.replace("%NUM_SERIE%",NumSerie) 

    _log=Logger()


    NumSerie=variable['numero_serie']
    #Plataforma=variable['Plataforma']
    TipoSync=variable['TipoSync'] 
    #print(TipoSync )   
    _jsonres={'status':200,'jsonData':variable['numero_serie'],'statusMenssage':'OK'}

    try:
        _tp=TerminalPortatil.objects.get(numero_serie=NumSerie)
        _tecnico=Tecnico.objects.get(terminal_portatil=_tp)

        #print('tecnico {}'.format(_tecnico))
        #print('_tp {}'.format(_tp))
    except Exception as e:
        print("Excepcion {}".format(e))


    _flag1_GetOrdenes_sinBorrarDB = True
    _flag2_BorrarDB = False
    _flag4_NuevasOrdenesAsignadas = False
    _flag8_ResetDeContraseña = False
    _flag16_UltimaPosicionGPS = True
    _flag32_ObtenerTodo = False
    #actualiza la fecha hora de la ultima conexion de la tp
    _tp.fh_ultima_conexion=datetime.now()
    _tp.save()
    #print(_tp.fh_ultima_conexion.strftime('%Y%m%d %H%M%s'))
    #obtengo los flags del usuario de tp
    print(_tecnico.flag_reset_password)
    if _tecnico.flag_reset_password==1:

        _flag8_ResetDeContraseña=True
    print(_flag8_ResetDeContraseña)
    if _tecnico.flag_descarga_total==1:
        _flag32_ObtenerTodo=True
    if _tecnico.flag_liberar_datos==1:
        _flag2_BorrarDB=True

    cantidad=OrdenDeTrabajo.objects.filter(tecnico_id=_tecnico,estado=3,flag_asignacion_guardada=1).count()
    print(cantidad)
    if cantidad>0:
        _flag4_NuevasOrdenesAsignadas=True

    

    try:

        _nResult=''
                    
        if TipoSync == '0' and _flag2_BorrarDB == True and _flag32_ObtenerTodo == False:
            _nResult = '2'
            _jsonres={'status':200,'jsonData':_nResult,'statusMenssage':'OK'}

            _log.logsetlevel('DEBUG')
    
            _log.setpath(path1)

            _log.Debug( _tp + 'FLAG TP Valor:{}'.format(_nResult))
            return _jsonres

        
        
        if TipoSync == '0' and _flag2_BorrarDB == True and _flag32_ObtenerTodo == True and _flag1_GetOrdenes_sinBorrarDB == True and _flag16_UltimaPosicionGPS == True:
            _nResult = '51'
            _jsonres={'status':200,'jsonData':_nResult,'statusMenssage':'OK'}

            _log.logsetlevel('DEBUG')

            _log.setpath(path1)

            _log.Debug(_tp + 'FLAG TP Valor:{}'.format(_nResult))

            return _jsonres


        if _flag1_GetOrdenes_sinBorrarDB == True and _flag2_BorrarDB == False and _flag32_ObtenerTodo == False and _flag4_NuevasOrdenesAsignadas == False and _flag8_ResetDeContraseña == False and _flag16_UltimaPosicionGPS == True :

            _nResult = '17'

        if _flag1_GetOrdenes_sinBorrarDB == True and _flag2_BorrarDB == False and _flag32_ObtenerTodo == False and _flag4_NuevasOrdenesAsignadas == True and _flag8_ResetDeContraseña == False and _flag16_UltimaPosicionGPS == True :

        
            _nResult = '21'

        if  _flag1_GetOrdenes_sinBorrarDB == True and _flag2_BorrarDB == False and _flag32_ObtenerTodo == False and _flag4_NuevasOrdenesAsignadas == True and _flag8_ResetDeContraseña == True and _flag16_UltimaPosicionGPS == True:
        
            _nResult = '29'

        if _flag1_GetOrdenes_sinBorrarDB == True and _flag2_BorrarDB == False and  _flag32_ObtenerTodo == False and _flag4_NuevasOrdenesAsignadas == False and _flag8_ResetDeContraseña == True and _flag16_UltimaPosicionGPS == True: 
        
            _nResult = '25'


        _jsonres={'status':200,'jsonData':_nResult,'statusMenssage':'OK'}
        _log.logsetlevel('DEBUG')

        _log.setpath(path1)

        _log.Debug(_tp + 'FLAG TP Valor:{}'.format(_nResult))

    except Exception as e:
        _jsonres={'status':500,'jsonData':'','statusMenssage':'OK'}
        _log.logsetlevel('ERROR')
        _log.setpath(path1)
        _log.Error('Error en GetFlag')
        print("Excepcion {}".format(e))
    return _jsonres



def setUpdEstadoOrdenesCargadas (param):
    deserializado = json.dumps(param)
    variable=json.loads(deserializado)
    print('variable {}'.format(variable))
 #   var=deserializado.replace("'","\"")
 #   print(var)
    _list=[]
    NumSerie=variable['numero_serie']
    Ordenes=variable['Ordenes']
    _list=Ordenes.split(',')

    _parametro=Parametro.objects.get(pk='P_TP_PATH_WS_LOG')
    path=_parametro.valor_1
    path1=path.replace("%NUM_SERIE%",NumSerie) 

    _log=Logger()

    try:
        print(_list)
        print(Ordenes)
        _tp=TerminalPortatil.objects.get(numero_serie=NumSerie)
        _ot=OrdenDeTrabajo.objects.filter(numero_orden__in=_list).update(estado=7)
        print(_ot)


        _jsonres={'status':200,'jsonData':[NumSerie,Ordenes],'statusMenssage':'OK'}

        _log.logsetlevel('INFO')

        _log.setpath(path1)

        _log.Info('Se actualizo el estado de las �rdenes')

    except Exception as e:
        _jsonres={'status':500,'jsonData':'','statusMenssage':'OK'}

        _log.logsetlevel('ERROR')

        _log.setpath(path1)

        _log.Error('Ocurri� un error al actualizar el estado de las �rdenes')
        
        print("Excepcion {}".format(e))
    return _jsonres




def setUpdEstadoOrdenAnulada (param):
    deserializado = json.dumps(param)
    variable=json.loads(deserializado)
    print('variable {}'.format(variable))
 #   var=deserializado.replace("'","\"")
 #   print(var)
    _list=[]
    NumSerie=variable['numero_serie']
    Ordenes=variable['Ordenes']

    _parametro=Parametro.objects.get(pk='P_TP_PATH_WS_LOG')
    path=_parametro.valor_1
    path1=path.replace("%NUM_SERIE%",NumSerie)

    _list=Ordenes.split(',')
    try:
        print(_list)
        print(Ordenes)
        _tp=TerminalPortatil.objects.get(numero_serie=NumSerie)
        _tecnico=Tecnico.objects.get(terminal_portatil=NumSerie)
        _ot=OrdenDeTrabajo.objects.filter(numero_orden__in=_list).update(estado=65)
        print(_ot)

        _ot=OrdenDeTrabajo.objects.filter(estado=3,tecnico=_tecnico).count()
        CantAsignada=_ot
        print(CantAsignada)
        if CantAsignada==0:
            _tp.estado_asignada=0
            _tp.cantidad_asignada=0
            _tp.save()

        else:
            _tp.estado_asignada=1
            _tp.cantidad_asignada=CantAsignada
            _tp.save()

        _ot=OrdenDeTrabajo.objects.filter(estado=7,tecnico=_tecnico).count()
        CantCargada=_ot
        print(CantCargada)
        if CantCargada==0:
            _tp.estado_cargada=0
            _tp.cantidad_cargada=0
            _tp.save()
        else:
            _tp.estado_cargada=0
            _tp.cantidad_cargada=CantCargada
            _tp.save()


        _jsonres={'status':200,'jsonData':[NumSerie,Ordenes],'statusMenssage':'OK'}

        _log.logsetlevel('INFO')

        _log.setpath(path1)

        _log.Info('Se actualizo el estado de las �rdenes')

    except Exception as e:
        _jsonres={'status':500,'jsonData':'','statusMenssage':'OK'}
        
        _log.logsetlevel('ERROR')

        _log.setpath(path1)

        _log.Error('Ocurri� un error al actualizar el estado de las �rdenes')
        print("Excepcion {}".format(e))
    return _jsonres



def enviarOrdenesNoTrabajadas(param):
    deserializado = json.dumps(param)
    variable=json.loads(deserializado)
    print('variable {}'.format(variable))

    _list=[]
    NumSerie=variable['numero_serie']
    Ordenes=variable['Ordenes']

    _parametro=Parametro.objects.get(pk='P_TP_PATH_WS_LOG')
    path=_parametro.valor_1
    path1=path.replace("%NUM_SERIE%",NumSerie)

    _list=Ordenes.split(',')
    try:

        _tp=TerminalPortatil.objects.get(numero_serie=NumSerie)
        _tecnico=Tecnico.objects.get(terminal_portatil=NumSerie)
        _ot=OrdenDeTrabajo.objects.filter(numero_orden__in=_list).update(estado=33)




        _jsonres={'status':200,'jsonData':[NumSerie,Ordenes],'statusMenssage':'OK'}

        _log.logsetlevel('INFO')

        _log.setpath(path1)

        _log.Info('Se enviaron ordenes no trabajadas')

    except Exception as e:
        _jsonres={'status':500,'jsonData':'','statusMenssage':'OK'}

        _log.logsetlevel('ERROR')

        _log.setpath(path1)

        _log.Error('Ocurri� un error al enviar �rdenes no trabajadas')
        
        print("Excepcion {}".format(e))
    return _jsonres



def enviarActividadUsuario (param):
    deserializado = json.dumps(param)
    variable=json.loads(deserializado)
    print('variable {}'.format(variable))

    _log=Logger()
    


    _list=[]
    print('Paso')
    NumSerie=variable['numero_serie']
    print('entro')
    GpsInfo=variable['GpsInfo']
    print(GpsInfo)
    _list=GpsInfo.split('|')
    print(_list)
    print(_list[0])
    print(_list[1])
    try:
        _sFechaHora = _list[0]
        _sLatitud = _list[1].replace( ',' , '.' )
        _sLongitud = _list[2].replace( ',' , '.' )
        _sId_Actividad = _list[3]
        _sRef_Actividad =_list[4]
        _fechahorasistema=datetime.now()

        _tp=TerminalPortatil.objects.get(numero_serie=NumSerie)
        _tecnico=Tecnico.objects.get(terminal_portatil=NumSerie)


        _gps=GpsActividadesUsuarios()
        _gps.actividad=_sId_Actividad
        _gps.ref_actividad=_sRef_Actividad
        _gps.fhregistro=_sFechaHora
        _gps.fh_sistema=_fechahorasistema
        _gps.latitud=_sLatitud
        _gps.longitud=_sLongitud
        _gps.oficina=_tp.oficina
        _gps.tecnico=_tecnico
        _gps.save()

        _jsonres={'status':200,'jsonData':'','statusMenssage':'OK'}

        _parametro=Parametro.objects.get(pk='P_TP_PATH_PUNTOS_GPS')
       
        path=_parametro.valor_1
        
        path1=path.replace("%NUM_SERIE%",NumSerie) 
        
        ruta=path1

        _sLogName= 'Actividad_GPS_'+ datetime.now().strftime('%Y%m%d_%H') + ".txt"
        
        escribir= GpsInfo
        if not os.path.exists(ruta): 
            os.makedirs(ruta)

        _file=open(path1 + '/'  + _sLogName ,'a')

        _file.write('\n' + escribir)

        _file.close()



    except Exception as e:
        _jsonres={'status':500,'jsonData':'','statusMenssage':'OK'}
        _log.logsetlevel('ERROR')  
        _log.setpath(path1)
        _log.Error('No se encuentra configurado el directorio de resguardo de las actividades GPS')


        print("Excepcion {}".format(e))
    return _jsonres


def enviarPuntosGps(param):
    deserializado = json.dumps(param)
    variable=json.loads(deserializado)
    #print('variable {}'.format(variable))

    _list=[]
    _list1=[]
    NumSerie=variable['numero_serie']
    GpsInfo=variable['GpsInfo']

    _list=GpsInfo.split('|')

    for pos in _list:
        _list1.append(pos.split(';'))

    _list3=[]
    for posi in _list1:

        try:
            FechaHora =posi[0]
            Latitud = posi[1]
            Longitud = posi[2]
            Velocidad = posi[3]

            i=0
            registro=len(_list1)
            _lista2=[]
            for posicion in _list1:
                #print('entro')
                #print(posicion)
                if i==0:
                    fecha_registro=FechaHora
                    sacarhora=datetime.strptime(fecha_registro,'%Y%m%d%H%M%S')
                    _result=[]
                    _result.append(sacarhora.strftime('%H'))
                    hora=_result[0]
                    print(_result)

                    Posiciones=fecha_registro+';'+Latitud+';'+Longitud+ ';'+ Velocidad + '|'
                else:
                    _fechaact=FechaHora
                    sacarhora1=datetime.strptime(_fechaact,'%Y%m%d%H%M%S')
                    _result1=[]
                    _result1.append(sacarhora1.strftime('%H'))
                    hora1=_result1[0]

                    if (fecha_registro!=_fechaact or hora!=hora1 or i == registro - 1):

                        _posiciongps=Posicionesgps()
                        _posiciongps.posgps(fecha_registro,hora,Posiciones)

                        _lista2.append(_posiciongps)

                        fecha_registro=FechaHora
                        hora=datetime.strptime(fecha_registro,'%Y%m%d%H%M%S')
                        _result=[]
                        _result.append(sacarhora.strftime('%H'))
                        hora=_result[0]
                        Posiciones=fecha_registro+';'+Latitud+';'+Longitud +';'+ Velocidad + '|'
                    else:

                        Posiciones=Posiciones+_fechaact +';'+Latitud+';'+Longitud+ ';'+ Velocidad + '|'
                i=i+1


            _tp=TerminalPortatil.objects.get(numero_serie=NumSerie)
            _tecnico=Tecnico.objects.get(terminal_portatil=NumSerie)

            for item in _lista2:
                _gps=GpsRegistroPosiciones()
                _gps.fecha_registro=item.Fecha
                _gps.hora_registro=item.Hora
                _gps.hora_actualizacion=datetime.now()
                _gps.posiciones=item.Posicion
                _gps.oficina=_tp.oficina
                _gps.tecnico=_tecnico
                _gps.save()


            _jsonres={'status':200,'jsonData':'','statusMenssage':'OK'}
            



        except Exception as e:
            _jsonres={'status':500,'jsonData':'','statusMenssage':'OK'}


            print("Excepcion {}".format(e))
        return _jsonres




def generarDatos_Online(param):
    deserializado=json.dumps(param)
    variable=json.loads(deserializado)
    print('variable {}'.format(variable))

    NumSerie=variable['numero_serie']

    try:
        _tp=TerminalPortatil.objects.get(numero_serie=NumSerie)


        #Generar path 
        
        _BaseDatos=BaseDeDatos()

        _parametro=Parametro.objects.get(pk='P_TP_PATH_GENERACION')
        path=_parametro.valor_1
        path1=path.replace("%NUM_SERIE%",NumSerie) 


        _BaseDatos.setpath(path1)

        _BaseDatos.NewFileOnlineData(NumSerie)

        _jsonres = {'status':200,'jsonData':_BaseDatos.code64OnlineData(),'statusMenssage':'OK'}

    except Exception as e:
        _jsonres={'status':500,'jsonData':'','statusMenssage':'OK'}

        print("Excepcion {}".format(e))
    return _jsonres



def getNuevasAsignaciones(param):
    deserializado=json.dumps(param)
    variable=json.loads(deserializado)
    print('variable {}'.format(variable))

    NumSerie=variable['numero_serie']

    try:
        _tp=TerminalPortatil.objects.get(numero_serie=NumSerie)


        #Generar path 
        
        _BaseDatos=BaseDeDatos()

        _parametro=Parametro.objects.get(pk='P_TP_PATH_GENERACION')
        path=_parametro.valor_1
        path1=path.replace("%NUM_SERIE%",NumSerie) 

        print(path1)

        _BaseDatos.setpath(path1)

        _BaseDatos.NewFileNewAssignment(NumSerie)



        _jsonres = {'status':200,'jsonData':_BaseDatos.code64NewAssignment(),'statusMenssage':'OK'}

    except Exception as e:
        _jsonres={'status':500,'jsonData':'','statusMenssage':'OK'}

        print("Excepcion {}".format(e))
    return _jsonres

