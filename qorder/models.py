from django.db import models
from django.db.models import Count
from core.models import EmserUser, WorkUnit, TipoPersonal, Contratista, TipoOrden, Prefijo
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import ugettext_lazy as _
from datetime import datetime,timedelta

STATUS_ENABLED = [1,33,1025]
OS_ASIGNADA = 2
OS_CARGADA = 3
OS_TRABAJADA = 4
OS_TRABAJADA_CON_ANOMALIA = 5
OS_PENDIENTE = 6
OS_ANULADA = 7
OS_FORZADA = 8
OS_LISTA_2_EXPORT = 9
OS_EXPORTADA = 10
OS_PR_ABIERTA = 11
OS_PR_CERRADA = 12
OS_RECHAZADA = 13
OS_ASIGNADA_A_HOJA_DE_RUTA = 14
OS_ANULADA_TRABAJADA = 15
OS_TO_STRING={2:'ASIGNADA',
              3:'CARGADA',
              4:'TRABAJADA',
              5:'TRABAJADA CON ANOMALIA',
              6:'PENDIENTE',
              7:'ANULADA',
              8:'FORZADA',
              9:'LISTA PARA EXPORTAR',
              10:'EXPORTADA',
              11:'ABIERTA CON PROBLEMAS',
              12:'CERRADA CON PROBLEMAS',
              13:'RECHAZADA',
              14:'ASIGNADA A HOJA DE RUTA',
              15:'ANULADA TRABAJADA'}


class Cliente(models.Model):

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
       return '{}'.format(self.nombre)
    
    codigo = models.CharField('Código',primary_key=True, max_length=50) 
    nombre = models.CharField('Nombre', max_length=60)    
    apellido_1 = models.CharField('Apellido 1', max_length=50,blank=True,null=True)
    apellido_2 = models.CharField('Apellido 2', max_length=50,blank=True,null=True)
    calle = models.CharField('Calle', max_length=50,blank=True,null=True)
    numero_puerta = models.IntegerField('Numero de Puerta',blank=True,null=True)
    piso = models.CharField('Piso',max_length=50,blank=True,null=True)
    duplicador = models.CharField('Duplicador', max_length=50,blank=True,null=True)
    localidad = models.CharField('Localidad', max_length=50,blank=True,null=True)
    municipio = models.CharField('Municipio', max_length=50,blank=True,null=True)
    barrio = models.CharField('Barrio', max_length=50,blank=True,null=True)
    departamento = models.CharField('Departamento', max_length=50,blank=True,null=True)
    codigo_postal = models.CharField('Código Postal', max_length=15,blank=True,null=True)
    estado_cliente = models.SmallIntegerField(default=1)
    fecha_alta = models.CharField('Fecha alta', max_length=25,blank=True,null=True) 
    #models.DateField(auto_now_add=True)
    observacion = models.CharField('Observación', max_length=600,blank=True,null=True)
    
class ContactoCliente(models.Model):

    class Meta:
        verbose_name = "ContactoCliente"
        verbose_name_plural = "ContactosCliente"

    def __str__(self):
        return self.nombre
    
    nombre = models.CharField('Nombre', max_length=50)    
    apellido_1 = models.CharField('Apellido 1', max_length=51)
    apellido_2 = models.CharField('Apellido 2', max_length=50,blank=True,null=True)
    direccion = models.CharField('Dirección', max_length=50,blank=True,null=True)
    telefono_fijo = PhoneNumberField('Teléfono fijo',blank=True,null=True)
    telefono_movil = PhoneNumberField('Teléfono móvil',blank=True,null=True)
    email_1 = models.EmailField('eMail 1',blank=True,null=True)
    email_2 = models.EmailField('eMail 2',blank=True,null=True)
    notas = models.TextField('Notas',blank=True,null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT,)

 
class Codigo(models.Model):

    class Meta:
        verbose_name = "Codigo"
        verbose_name_plural = "Codigos"
        unique_together = (("codigo", "prefijo"),)

    def __str__(self):
        return '{}-{}'.format(self.codigo,self.descripcion)
    
    codigo = models.CharField('Código', primary_key=True, max_length=50)
    prefijo = models.ForeignKey(Prefijo, on_delete=models.PROTECT)
    descripcion = models.CharField('Descripción', max_length=50)         
    activo =  models.SmallIntegerField('Activo',default=1)

    def enable(self,accion):
        self.activo=accion
        self.save()

class Encuesta(models.Model):

    class Meta:
        verbose_name = "Encuesta"
        verbose_name_plural = "Encuestas"
      

    def __str__(self):
        return '{} {}'.format(self.nombre,self.descripcion)
    
    nombre = models.CharField('Nombre', max_length=50)
    descripcion = models.CharField('Descripción', max_length=50)         
    activo =  models.SmallIntegerField('Activo',default=1)

    def enable(self,accion):
        self.activo=accion
        self.save()




class EncuestaDetalle(models.Model):

    class Meta:
        verbose_name = "EncuestaDetalle"
        verbose_name_plural = "EncuestasDetalle"
      

    def __str__(self):
        return '{}'.format(self.titulo)
    
    encuesta = models.ForeignKey(Encuesta, on_delete=models.PROTECT)
    titulo = models.CharField('Título', max_length=50)
    tipo = models.CharField('Tipo',max_length=5,choices=(('1', 'Si/No'),
                                              ('2', 'Selección Simple'), 
                                              ('3', 'Selección Múltiple'),
                                              ('4', 'Ingreso Numérico'),
                                              ('6', 'Ingreso Alfanumérico'),
                                              ))
    texto_pregunta = models.CharField('Pregunta', max_length=50)         
    opciones  = models.CharField('Opciones', max_length=1000,blank=True,null=True)
    orden = models.SmallIntegerField('Orden')


class Aparato(models.Model):

    class Meta:
        verbose_name = "Aparato"
        verbose_name_plural = "Aparatos"        
        unique_together = (("marca", "num_serie"),)

    def __str__(self):
        return '{}'.format(self.aparato)

    aparato = models.CharField('aparato_id',primary_key=True, max_length=80)
    marca = models.ForeignKey(Codigo, related_name='marca',on_delete=models.PROTECT,)
    num_serie = models.CharField('num. serie', max_length=50)   
    num_ruedas = models.SmallIntegerField('núm. ruedas')
    tipo_aparato = models.ForeignKey(Codigo,related_name='tipo_aparato', on_delete=models.PROTECT,blank=True,null=True)
    estado_aparato =  models.CharField('Activo',max_length=50,blank=True,null=True)
    tipo_intensidad = models.ForeignKey(Codigo, related_name='tipo_intensidad',on_delete=models.PROTECT,blank=True,null=True) 
    tipo_fase = models.ForeignKey(Codigo, related_name='tipo_fase',on_delete=models.PROTECT,blank=True,null=True)
    tipo_tension = models.ForeignKey(Codigo, related_name='tipo_tension',on_delete=models.PROTECT,blank=True,null=True)
    fecha_fabricacion = models.DateField('Fecha fabricación',blank=True,null=True)
    fecha_instalacion = models.DateField('Fecha instalación',blank=True,null=True)
    fecha_proxima_calibracion = models.DateField('Fecha prox. calibración',blank=True,null=True)
    diametro = models.CharField('diámetro', max_length=50,blank=True,null=True)
    presion = models.CharField('presión', max_length=50,blank=True,null=True)
    coef_perdida = models.CharField('coef. pérdida', max_length=50,blank=True,null=True) 


class Precinto(models.Model):

    class Meta:
        verbose_name = "Precinto"
        verbose_name_plural = "Precintos"

    def __str__(self):
        pass

    aparato = models.ForeignKey(Aparato)
    precinto = models.CharField('precinto', max_length=50)
    color = models.CharField('color', max_length=50,blank=True,null=True)


class Consumo(models.Model):

    class Meta:
        verbose_name = "Consumo"
        verbose_name_plural = "Consumos"

    def __str__(self):
        return '{}-{}-{}'.format(self.tipo_consumo.codigo,self.tope_lectura_maxima,self.tope_lectura_minima)
    
    consumo = models.CharField('consumo',primary_key=True, max_length=100)
    aparato = models.ForeignKey(Aparato, on_delete=models.PROTECT)
    tipo_consumo = models.ForeignKey(Codigo, on_delete=models.PROTECT,blank=True,null=True)
    constante = models.FloatField()
    lectura_anterior = models.IntegerField()
    consumo_anterior = models.IntegerField()
    fecha_lectura_anterior = models.DateField()
    tope_lectura_maxima = models.IntegerField()
    tope_lectura_minima = models.IntegerField()


class HistoricoConsumo(models.Model):

    class Meta:
        verbose_name = "HistoricoConsumo"
        verbose_name_plural = "HistoricoConsumos"

    def __str__(self):
        pass
    codigo=models.CharField('codigo',max_length=50,primary_key=True)    
    consumo = models.ForeignKey(Consumo, on_delete=models.PROTECT)
    fecha_lectura = models.DateField()
    lectura = models.IntegerField()
    valor_consumo = models.IntegerField()
    incidencia_1 = models.CharField('anomalía 1', max_length=50,blank=True,null=True)
    incidencia_2 = models.CharField('anomalia 2', max_length=50,blank=True,null=True)
    incidencia_3 = models.CharField('anomalia 3', max_length=50,blank=True,null=True)
    anio=models.CharField('anio',max_length=10,blank=True,null=True)
    tipo_consumo = models.ForeignKey(Codigo, on_delete=models.PROTECT,blank=True,null=True)
    cod_anomalia=models.CharField('cod_anomalia',max_length=10,blank=True,null=True)

class EstadoOrden(models.Model):

    class Meta:
        verbose_name = "EstadoOrden"
        verbose_name_plural = "EstadoOrdenes"

    def __str__(self):
        return self.descripcion
    
    descripcion = models.CharField('descripción', max_length=50)


class TerminalPortatil(models.Model):

    class Meta:
        verbose_name = "TerminalPortatil"
        verbose_name_plural = "TerminalesPortatiles"
   
    numero_serie = models.CharField(_('número_serie'), max_length=50,primary_key=True)
    alias = models.CharField(_('alias'), max_length=50,blank=True,null=True)
    oficina = models.ForeignKey(WorkUnit,on_delete=models.PROTECT,blank=True,null=True,related_name='contratistas')
    num_telefono = models.CharField('teléfono', max_length=50,blank=True,null=True)
    androidID = models.CharField('androidID', max_length=50,blank=True,null=True)
    imei = models.CharField('imei', max_length=50,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    fh_ultima_conexion = models.DateTimeField(blank=True,null=True)
    estado = models.SmallIntegerField('Activo')
    contratista = models.ForeignKey(Contratista,on_delete=models.PROTECT,blank=True,null=True)
    version_instalada = models.CharField('versión instalada', max_length=10,blank=True,null=True)
    plataforma = models.CharField('plataforma', max_length=50,blank=True,null=True)
    fecha_actualizacion = models.DateTimeField(blank=True,null=True)    
    token = models.CharField('token', max_length=500,blank=True,null=True)

    estado_asignada = models.SmallIntegerField(default=0,blank=True,null=True)
    cantidad_asignada = models.IntegerField(default=0,blank=True,null=True)
    estado_cargada = models.SmallIntegerField(default=0,blank=True,null=True)
    cantidad_cargada = models.IntegerField(default=0,blank=True,null=True)
    def __str__(self):
        return "{}".format(self.numero_serie)
    
    def get_fh_ultima_conexion(self):
        if self.fh_ultima_conexion:
            return self.fh_ultima_conexion.strftime("%d/%m/%Y %H:%M:%S")
        else:
            return ''

    def isInactivable(self):
        tecnico = Tecnico.objects.filter(terminal_portatil=self.numero_serie)
        
        if len(tecnico)>0: 
            return True
        else:
            return False
    
    def enable(self,accion):
        self.estado=accion
        self.save()

    def activar(self):
        self.estado=1 
        self.save()


    def desactivar(self):
        self.estado=0 
        self.save()






class Tecnico(models.Model):
    
        class Meta:
            verbose_name = "Tecnico"
            verbose_name_plural = "Tecnicos"
    
        def __str__(self):
            return "{} - {} {}".format(self.codigo,self.nombre_1,self.apellido_1)
        
        codigo = models.CharField('Código', max_length=10,primary_key=True)
        nombre_1 = models.CharField('Nombre ', max_length=50)
        apellido_1 = models.CharField('Apellido ', max_length=50)
        apellido_2 = models.CharField('Apellido 2', max_length=50,blank=True,null=True)
        legajo = models.CharField('Número empleado', max_length=50,blank=True,null=True)

        password = models.CharField('Contraseña', max_length=50,default='12345678')
        terminal_portatil = models.ForeignKey(TerminalPortatil, on_delete=models.PROTECT,blank=True,null=True)
        tipo_personal = models.ForeignKey(TipoPersonal, on_delete=models.PROTECT,blank=True,null=True)
        contratista = models.ForeignKey(Contratista,on_delete=models.PROTECT,blank=True,null=True)
        activo = models.SmallIntegerField('activo', default=1)
        flag_reset_password = models.SmallIntegerField(default=1,blank=True,null=True)
        flag_descarga_total = models.SmallIntegerField(default=0,blank=True,null=True)
        flag_descarga_parcial = models.SmallIntegerField(default=0,blank=True,null=True)
        flag_liberar_datos = models.SmallIntegerField(default=0,blank=True,null=True)

        def resetpassword(self,accion):
           print("resetpassword {}".format(accion))
           try:
              self.flag_reset_password=accion
              self.save() 
           except Exception as e:
              print("Error {}".format(e))
          

        def descarga(self,accion):
           self.flag_descarga_total=accion
           self.flag_liberar_datos=accion
           self.save()

        def liberar(self,accion):
           self.flag_liberar_datos=accion
           self.save()

        def enable(self,accion):
           self.activo=accion
           self.save()

        def nombre_completo(self):
            return "{} {} {}".format(self.nombre_1,self.apellido_1,self.apellido_2)

        #def myOrdersByEstado(self):
        #   return OrdenDeTrabajo.objects.filter(tecnico=self.id).values('estado').annotate(total=Count('estado'))
          

        #def get_asignadas(self):
            #return OrdenDeTrabajo.objects.filter(tecnico=self.id).extra(where=['estado = 3'])
          

        #def get_cargadas(self):
            #return OrdenDeTrabajo.objects.filter(tecnico=self.id).extra(where=['estado = 7'])
        

        #def get_trabajadas(self):
            ##return OrdenDeTrabajo.objects.filter(tecnico=self.id,estado__in=[9,17,265,273])
            #return OrdenDeTrabajo.objects.filter(tecnico=self.id).extra(where=['estado = 256 OR estado = 273'])

        #def get_revisar(self):
            ##return OrdenDeTrabajo.objects.filter(tecnico=self.id,estado__in=[9,17,265,273])
            #return OrdenDeTrabajo.objects.filter(tecnico=self.id).extra(where=['estado = 9  OR estado = 17'])

        #def get_exportadas(self):
            #hoy = datetime.now().strftime("%Y%m%d000000")
            ##return OrdenDeTrabajo.objects.filter(tecnico=self.id,estado__in=[777,785,913,905],fecha_hora_exportacion__gte=hoy)
            #return OrdenDeTrabajo.objects.filter(tecnico=self.id,fecha_hora_exportacion__gte=hoy).extra(where=['estado = 777 OR estado = 785 OR estado= 913 OR estado = 905'])
        def get_fh_ultima_conexion(self):
            try:

              tp = TerminalPortatil.objects.get(numero_serie=self.terminal_portatil)

              if tp.fh_ultima_conexion:
            
                 return tp.fh_ultima_conexion.strftime("%d/%m/%Y %H:%M:%S")
              else:
                return ' '
            except Exception as e:

              return ' '

        def get_posicion(self):
          try:
            return GpsUltimaPosicion.objects.get(tecnico_id=self.codigo)
          except Exception as e:
             pass
          return None;


class EstadoRuta(models.Model):

    class Meta:
        verbose_name = "EstadoRuta"
        verbose_name_plural = "EstadosRutas"    

    def __str__(self):
        pass
    
    estado = models.SmallIntegerField(default=0)
    descripcion = models.CharField('descripción', max_length=50)
  
          
class GpsUltimaPosicion(models.Model):

    class Meta:
        unique_together = (('oficina', 'tecnico', 'fecha_punto_gps'),)

    tecnico = models.ForeignKey(Tecnico, on_delete=models.PROTECT)
    oficina = models.ForeignKey(WorkUnit, on_delete=models.PROTECT)

    fecha_punto_gps = models.CharField(max_length=14)
    fecha_actualizacion = models.CharField(max_length=14, blank=True, null=True)
    latitud = models.CharField(max_length=20, blank=True, null=True)
    longitud = models.CharField(max_length=20, blank=True, null=True)
    velocidad = models.CharField(max_length=14, blank=True, null=True)
    curso = models.CharField(max_length=20, blank=True, null=True)



    def get_address(self):
        try:
            from geopy.geocoders import Nominatim
            from urllib.request import Request
        
            def get_geolocator():
                geolocator = Nominatim(scheme='http')
        
                requester = geolocator.urlopen
        
                def requester_hack(req, **kwargs):
                    req = Request(url=req, headers=geolocator.headers)
                    return requester(req, **kwargs)
        
                geolocator.urlopen = requester_hack
        
                return geolocator
        
            location = get_geolocator().reverse("{}, {}".format(self.latitud, self.longitud), timeout=20)
            return location.address
        except Exception as e:
            print('{}'.format(e))
            return 'S/D'

    def get_fecha_ultima_posicion(self):
        return datetime.strptime(self.fecha_punto_gps, "%Y%m%d%H%M%S")

    def get_status_string(self):
        ahora = datetime.now()
        hace_15 = (ahora-timedelta(minutes=15)).strftime("%Y%m%d%H%M%S")
        hace_60 = (ahora-timedelta(hours=1)).strftime("%Y%m%d%H%M%S")
        try:
            if int(self.fecha_punto_gps) > int(hace_15):
                return 'Reciente'
            if int(self.fecha_punto_gps) < int(hace_60):
                return 'Más de 60 minutos'
            if int(self.fecha_punto_gps) < int(hace_15):
                return 'Más de 15 minutos'
        except:
            pass
        return 'grey'

    def get_status_color(self):
        try:
            posicion = datetime.strptime(self.fecha_punto_gps, "%Y%m%d%H%M%S")
            ahora = datetime.now()
            status = ahora - posicion
            hace_15 = timedelta(minutes=15)
            hace_60 = timedelta(hours=1)
            print ("{}".format(status))
            if status > hace_60:
                return 'red'
            if status > hace_15:
                return 'yellow'
            if status <= hace_15 :
                return 'green'

        except Exception as e:
            print ("{}".format(e))
        return 'grey'
     
class Geofencing(models.Model):
    class Meta:
        verbose_name = "Geofencing"
        verbose_name_plural = "Geofencing" 

    oficina = models.ForeignKey(WorkUnit)
    descripcion = models.CharField(max_length=50)
    activo = models.SmallIntegerField('activo', default=1)

    def enable(self,accion):
        self.activo=accion
        self.save()


class GeofencingDetalle(models.Model):
    class Meta:
        verbose_name = "GeofencingDetalle"
        verbose_name_plural = "GeofencingDetalle"

    def __str__(self):
        return "{}".format(self.geofencing.id)

    geofencing = models.ForeignKey(Geofencing, on_delete=models.PROTECT)    
    radio_circulo = models.IntegerField(blank=True, null=True)
    composicion_area = models.CharField(max_length=2000,blank=True,null=True)
    geohash_centro_circulo = models.CharField(max_length=20,blank=True,null=True)
    geohash_centro_mapa = models.CharField(max_length=20,blank=True,null=True)
    zoom_mapa = models.SmallIntegerField(default=12) 
    notifica_email_ingreso = models.BooleanField('Notifica email ingreso', default=False) 
    notifica_email_egreso = models.BooleanField('Notifica email egreso', default=False) 
    notifica_pantalla_ingreso = models.BooleanField('Notifica pantalla ingreso', default=False) 
    notifica_pantalla_egreso = models.BooleanField('Notifica pantalla egreso', default=False) 
    notifica_sonido_ingreso = models.BooleanField('Notifica sonido ingreso', default=False) 
    notifica_sonido_egreso = models.BooleanField('Notifica sonido egreso', default=False) 
    notifica_ws_ingreso = models.BooleanField('Notifica ws ingreso', default=False) 
    notifica_ws_egreso = models.BooleanField('Notifica ws egreso', default=False) 
    emails_ingreso = models.CharField(max_length=2000,blank=True,null=True)
    emails_egreso = models.CharField(max_length=2000,blank=True,null=True)
    mensaje_email_ingreso = models.CharField(max_length=2000,blank=True,null=True)
    mensaje_email_egreso = models.CharField(max_length=2000,blank=True,null=True)
    mensaje_pantalla_ingreso = models.CharField(max_length=2000,blank=True,null=True)
    mensaje_pantalla_egreso = models.CharField(max_length=2000,blank=True,null=True)
    mensaje_ws_ingreso = models.CharField(max_length=2000,blank=True,null=True)
    mensaje_ws_egreso = models.CharField(max_length=2000,blank=True,null=True)

    id_actividad_ingreso = models.CharField(max_length=20,blank=True,null=True)
    id_actividad_egreso = models.CharField(max_length=20,blank=True,null=True)


class GeofencingXTecnico(models.Model):

    class Meta:
        verbose_name = "GeofencingXTecnico"
        verbose_name_plural = "GeofencingXTecnico"

    def __str__(self):
        return "{}".format(self.id)
    
    tecnico = models.ForeignKey(Tecnico, on_delete=models.PROTECT)
    geofencing = models.ForeignKey(Geofencing, on_delete=models.PROTECT)
    fecha_asignacion = models.DateField()
    

    
class GpsActividadesUsuarios(models.Model):
    oficina = models.ForeignKey(WorkUnit)
    tecnico = models.ForeignKey(Tecnico, on_delete=models.PROTECT)
    actividad = models.CharField(max_length=20)
    ref_actividad = models.CharField(max_length=50)
    fh_registro = models.CharField(max_length=14)
    fh_sistema = models.DateTimeField()
    latitud = models.CharField(max_length=20)
    longitud = models.CharField(max_length=20)
    geohash = models.CharField(max_length=50, blank=True, null=True)
    curso = models.CharField(max_length=20, blank=True, null=True)
    velocidad = models.CharField(max_length=20, blank=True, null=True)

    def get_fecha_str(self):
        return '{}/{}/{}'.format(self.fh_registro[6:8],self.fh_registro[4:6],self.fh_registro[0:4])

    def get_tecnico(self):
        return Tecnico.objects.get(id=self.tecnico_id)

    def get_orden(self):
        try:
            return OrdenDeTrabajo.objects.get(numero_orden=self.ref_actividad)
        except Exception as e:
            print (e)
            return None



    def get_address(self):
        try:
            from geopy.geocoders import Nominatim
            from urllib.request import Request
        
            def get_geolocator():
                geolocator = Nominatim(scheme='http')
        
                requester = geolocator.urlopen
        
                def requester_hack(req, **kwargs):
                    req = Request(url=req, headers=geolocator.headers)
                    return requester(req, **kwargs)
        
                geolocator.urlopen = requester_hack
        
                return geolocator
        
            location = get_geolocator().reverse("{}, {}".format(self.latitud, self.longitud), timeout=20)
            return location.address
        except Exception as e:
            print('{}'.format(e))
            return 'S/D'

    def position(self):
        return '{},{}'.format(self.latitud, self.longitud)


    def get_status_color(self):
        if 'PROBL' in self.actividad:
            return 'yellow';
        if 'ORDEN' in self.actividad:
            #resultado_lectura = DescLecturas.objects.get(num_os=self.ref_actividad)
            #if resultado_lectura.resultado_lectura==2:
            #    return 'purple'
            return 'green';
        return 'red';

    def is_actividad(self):
        if len(self.ref_actividad)>1:
            return True;
        return False;

    class Meta:
        unique_together = (('oficina', 'tecnico', 'actividad', 'ref_actividad', 'fh_registro', 'fh_sistema'),)



class GpsRegistroPosiciones(models.Model):
    oficina = models.ForeignKey(WorkUnit)
    tecnico = models.ForeignKey(Tecnico, on_delete=models.PROTECT)
    fecha_registro = models.CharField(max_length=8)
    hora_registro = models.CharField(max_length=2)
    hora_actualizacion = models.CharField(max_length=6, blank=True, null=True)
    posiciones = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = (('oficina', 'tecnico', 'fecha_registro', 'hora_registro'),)


class RutaSum(models.Model):
    class Meta:
        verbose_name = "RutaSum"
        verbose_name_plural = "RutasSum"

    def __str__(self):
        return '{}-{}'.format(str(self.rutasum),str(self.itinerario))
    idrutasum=models.CharField('idrutasum',max_length=20,primary_key=True)       
    oficina = models.ForeignKey(WorkUnit, on_delete=models.PROTECT,)
    rutasum = models.CharField('rutasum', max_length=5)
    itinerario = models.CharField('itinerario', max_length=5)
    Frecuencia=models.CharField('Frecuencia',max_length=10,null=True,blank=True)
    

class Ruta(models.Model):

    class Meta:
        verbose_name = "Ruta"
        verbose_name_plural = "Rutas"

    def __str__(self):
        return '{}-{}-{}-{}'.format(str(self.ciclo),str(self.ruta),str(self.itinerario),str(self.anio))
    
    idruta=models.CharField('idruta',max_length=30,primary_key=True)
    rutasum = models.ForeignKey(RutaSum, on_delete=models.PROTECT,)
    oficina = models.ForeignKey(WorkUnit, on_delete=models.PROTECT,)
    ciclo = models.CharField('ciclo', max_length=5)
    ruta = models.CharField('ruta', max_length=5)
    itinerario = models.CharField('itinerario', max_length=5)
    plan = models.CharField('plan', max_length=5,blank=True,null=True)
    anio = models.CharField('año', max_length=10)
    cantidad = models.SmallIntegerField(default=0)
    cantidad_leido  = models.SmallIntegerField(default=0)
    fecha_generacion = models.DateField(blank=True,null=True)
    fecha_estimada_resolucion = models.DateField(blank=True,null=True)
    estado =  models.IntegerField(default=0)
    tecnico = models.ForeignKey(Tecnico, on_delete=models.PROTECT,blank=True,null=True)
    flag_asignacion_guardada = models.SmallIntegerField(default=0)
    usuario_asignacion = models.ForeignKey(EmserUser ,blank=True, null=True)
    fecha_hora_asignacion = models.CharField(max_length=14, blank=True, null=True)
    fecha_hora_importacion = models.CharField(max_length=14, blank=True, null=True)
    fecha_hora_exportacion = models.CharField(max_length=14, blank=True, null=True)
    

    def getfilename(self):
        self._sLogName= str(self.idruta) + ".txt"
        return self._sLogName

    def getAvance(self):
         if self.cantidad_leido == 0:
            return 0
         if self.cantidad == 0:
            return 0
         return "{0:.2f}".format(self.cantidad_leido/self.cantidad * 100,2)
    
    def getAForzar(self):
        return OrdenDeTrabajo.objects.filter(ruta=self,estado=33).count()

class SemanaXUser(models.Model):
    class Meta:
        verbose_name = "SemanaXUser"
        verbose_name_plural = "SemanaXUser"

    def __str__(self):
        return "{}".format(self.semana)

    usuario = models.ForeignKey(EmserUser ,blank=True, null=True)
    semana = models.CharField('semana', max_length=14, blank=True, null=True)


class GeofencingXRuta(models.Model):

    class Meta:
        verbose_name = "GeofencingXRuta"
        verbose_name_plural = "GeofencingXRuta"

    def __str__(self):
        return "{}".format(self.id)
    
    ruta = models.ForeignKey(Ruta, on_delete=models.PROTECT)
    geofencing = models.ForeignKey(Geofencing, on_delete=models.PROTECT)
    fecha_asignacion = models.DateField()


class SegmentoSum(models.Model):
    class Meta:
        verbose_name = "SegmentoSum"
        verbose_name_plural = "SegmentosSum"
    
    def __str__(self):
        return '{}'.format(self.codigo_segmento)
    
    codigo_segmento = models.CharField('Codigo de Segmento', max_length=10,blank=True,null=True)
    descripcion_segmento = models.CharField('Descripcion de Segmento', max_length=50,blank=True,null=True)
    oficina = models.ForeignKey(WorkUnit, on_delete=models.PROTECT)

class Segmento_Areas(models.Model):
    class Meta:
        verbose_name = "Segmento_Area"
        verbose_name_plural = "Segmentos_Areas"
    
    def __str__(self):
        return '{}'.format(self.area)
    
    area = models.TextField(blank=True,null=True)
    segmentosum = models.ForeignKey(SegmentoSum, on_delete=models.PROTECT)

class PuntoDeSuministro(models.Model):

    class Meta:
        verbose_name = "PuntoDeSuministro"
        verbose_name_plural = "PuntoDeSuministros"

    def __str__(self):
        return 'Nis: {} - localidad: {}'.format(self.punto_suministro, self.localidad)
    
    num_contrato = models.CharField('Num.Contrato', max_length=50)
    punto_suministro = models.CharField('Punto Suministro', primary_key=True, max_length=50)
    tarifa = models.ForeignKey(Codigo,related_name='Tarifa', on_delete=models.PROTECT,blank=True,null=True)
    tipo_servicio = models.ForeignKey(Codigo,related_name='tipo_servicio', on_delete=models.PROTECT,)
    gps_latitud = models.CharField('latitud',max_length=14,blank=True,null=True)
    gps_longitud = models.CharField('longitud',max_length=14,blank=True,null=True)
    ref_finca = models.CharField('Ref. Acc. Finca', max_length=255,blank=True,null=True)
    ref_direccion = models.CharField('Ref. Direccion', max_length=255,blank=True,null=True)
    ref_suministro = models.CharField('Ref Suministro', max_length=255,blank=True,null=True)
    nif = models.CharField('NIF',max_length=10,blank=True,null=True)
    estado_suministro = models.SmallIntegerField('Activo')
    rutasum =  models.ForeignKey(RutaSum, on_delete=models.PROTECT,null=True,blank=True)
    calle = models.CharField('Calle', max_length=50)
    numero_puerta = models.IntegerField('Numero de Puerta')
    piso = models.CharField('Piso', max_length=100,blank=True,null=True)
    duplicador = models.CharField('Duplicador', max_length=50,blank=True,null=True)
    localidad = models.CharField('Localidad', max_length=50,blank=True,null=True)
    municipio = models.CharField('Municipio', max_length=50,blank=True,null=True)
    barrio = models.CharField('Barrio', max_length=50,blank=True,null=True)
    departamento = models.CharField('Departamento', max_length=50,blank=True,null=True)
    codigo_postal = models.CharField('Código Postal', max_length=15,blank=True,null=True)
    aparato = models.ForeignKey(Aparato, on_delete=models.PROTECT,blank=True,null=True)
    tipo_asociacion = models.ForeignKey(Codigo,related_name='tipo_asociacion', on_delete=models.PROTECT,blank=True,null=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT,blank=True,null=True)
    hashdata = models.CharField('hashdata', max_length=50,blank=True,null=True)
    secuencia_teorica = models.IntegerField(default=0,blank=True,null=True)
    secuencia_anterior=models.IntegerField(default=0,blank=True,null=True)
    fecha_actualizacion_secuencia=models.DateTimeField(blank=True,null=True)
    segmentosum = models.ForeignKey(SegmentoSum,on_delete=models.PROTECT,null=True, default=None)


    def ifExist():
        if PuntoDeSuministro.objects.filter(pk=self.punto_suministro).exists():
            return True
        else:
            return False

class Recibo(models.Model):

    class Meta:
        verbose_name = "Recibo"
        verbose_name_plural = "Recibos"

    def __str__(self):
        pass
    
    punto_suministro = models.ForeignKey(PuntoDeSuministro, on_delete=models.PROTECT)
    numero_recibo = models.CharField('número recibo', max_length=50)
    fecha_recibo = models.DateField()
    importe_recibo = models.FloatField()
    fecha_ultimo_pago = models.DateField()
    importe_ultimo_pago = models.FloatField()



class OrdenDeTrabajo(models.Model):

    class Meta:
        verbose_name = "OrdenDeTrabajo"
        verbose_name_plural = "OrdenDeTrabajos"

    def __str__(self):
        return '{}'.format(self.numero_orden)
    

    numero_orden = models.CharField('Número orden', primary_key=True, max_length=30)
    punto_suministro = models.ForeignKey(PuntoDeSuministro, on_delete=models.PROTECT)
    tipo_orden = models.ForeignKey(TipoOrden, on_delete=models.PROTECT)


    prioridad = models.SmallIntegerField(default=1)
    estado = models.IntegerField(default=1)
    secuencial_registro = models.SmallIntegerField(default=0)
    secuencia_teorica = models.IntegerField(default=0)
    ruta = models.ForeignKey(Ruta, on_delete=models.PROTECT)
    orden_terreno = models.SmallIntegerField(default=0)
    generada_desde_num_os  = models.CharField('generada desde', max_length=30,blank=True,null=True)
    tecnico = models.ForeignKey(Tecnico, on_delete=models.PROTECT,blank=True,null=True)
    flag_asignacion_guardada = models.SmallIntegerField(default=0)
    usuario_asignacion = models.ForeignKey(EmserUser ,blank=True,null=True)
    fecha_hora_asignacion = models.CharField(max_length=14, blank=True, null=True)
    fecha_hora_importacion = models.CharField(max_length=14, blank=True, null=True)
    fecha_hora_exportacion = models.CharField(max_length=14, blank=True, null=True)
    fecha_hora_anulacion = models.CharField(max_length=14, blank=True, null=True)
    fecha_hora_ult_modificacion = models.CharField(max_length=14, blank=True, null=True)
    fecha_hora_carga = models.CharField(max_length=14, blank=True, null=True)
    consumo = models.ForeignKey(Consumo, on_delete=models.PROTECT, blank=True, null=True)






class HistoricoEstadoRuta(models.Model):
   
    class Meta:
        verbose_name = "HistoricoEstadoRuta"
        verbose_name_plural = "HistoricoEstadoRutas"
   
    def __str__(self):
        pass

    ruta = models.ForeignKey(Ruta, on_delete=models.PROTECT)
    fecha = models.DateTimeField()
    usuario = models.CharField('usuario', max_length=50)
    estado = models.ForeignKey(EstadoRuta, on_delete=models.PROTECT)






class HistoricoEstadoOrden(models.Model):

    class Meta:
        verbose_name = "HistoricoEstadoOrden"
        verbose_name_plural = "HistoricoEstadoOrdens"

    def __str__(self):
        pass


    orden = models.ForeignKey(OrdenDeTrabajo, on_delete=models.PROTECT)
    estado = models.ForeignKey(EstadoOrden, on_delete=models.PROTECT)
    fecha = models.DateTimeField()
    usuairo = models.CharField('usuario', max_length=50)
    datos = models.CharField('datos', max_length=255)








class CodigoXTipoOrden(models.Model):

    class Meta:
        verbose_name = "CodigoXTipoOrden"
        verbose_name_plural = "CodigoXTipoOrdenes"

    def __str__(self):
        pass
    
    codigo = models.ForeignKey(Codigo, on_delete=models.PROTECT)
    tipo_orden = models.ForeignKey(TipoOrden, on_delete=models.PROTECT)
    prefijo = models.CharField('prefijo', max_length=5)
    propiedades = models.CharField('propiedades', max_length=100)



class OficinaXTecnico(models.Model):

    class Meta:
        verbose_name = "OficinaXTecnico"
        verbose_name_plural = "OficinasXTecnicos"

    def __str__(self):
        return "{}".format(self.id)
    
    tecnico = models.ForeignKey(Tecnico, on_delete=models.PROTECT)
    oficina = models.ForeignKey(WorkUnit, on_delete=models.PROTECT)
    fecha_asignacion = models.DateField()
    fecha_baja = models.DateField(blank=True,null=True)



class Problema(models.Model):
    class Meta:
         verbose_name = "Problema"

    def __str__(self):
        return '{}: {}'.format(self.id_problema,self.descripcion)

    id_problema = models.CharField(_('Código problema'),primary_key=True, max_length=5)
    descripcion = models.CharField(_('Descripción'),max_length=100, blank=True, null=True)   
    activo = models.SmallIntegerField('activo', default=1)

    def enable(self,accion):
        self.activo=accion
        self.save()

      

class Anomalia(models.Model):
    
    class Meta:
         verbose_name = "Anomalia"    

    def __str__(self):
        return '{}: {}'.format(self.id_anomalia,self.descripcion)

    id_anomalia = models.CharField(_('Código anomalía'),primary_key=True, max_length=5)
    descripcion = models.CharField(_('Descripción'),max_length=100, blank=True, null=True)
    tipo_resultado = models.ForeignKey(Codigo, on_delete=models.PROTECT, blank=True, null=True)
    prioridad = models.IntegerField(_('Prioridad'))    
    activo = models.SmallIntegerField('Activo', default=1)

        
    def enable(self,accion):
        self.activo=accion
        self.save()


 
class AnomaliaXTipo(models.Model):

    class Meta:
        verbose_name = "AnomaliaXTipo"
      

    def __str__(self):
        return "{} {}".format(self.id,self.foto_obligatoria)
    
    tipo_orden = models.ForeignKey(TipoOrden, on_delete=models.PROTECT)
    anomalia = models.ForeignKey(Anomalia, on_delete=models.PROTECT)
    foto_obligatoria = models.CharField(max_length=1, blank=True, null=True)
    observacion_obligatoria = models.CharField(max_length=1, blank=True, null=True)
    observacion_tabulada = models.CharField(max_length=1, blank=True, null=True)
    datos_medidor = models.CharField(max_length=1, blank=True, null=True)
    activo = models.SmallIntegerField('Activo', default=1)

    def getfoto_obligatoria(self):
        return "{}".format(self.foto_obligatoria)

    def enable(self,accion):
        self.activo=accion
        self.save()

    def foto(self,accion):
        self.foto_obligatoria=accion
        self.save()

    def obs(self,accion):
        self.observacion_obligatoria=accion
        self.save()

    def obst(self,accion):
        self.observacion_tabulada=accion
        self.save()

    def medidor(self,accion):
        self.datos_medidor=accion
        self.save()

class ProblemaXTipo(models.Model):

    class Meta:
        verbose_name = "ProblemaXTipo"
      

    def __str__(self):
        return "{}".format(self.id)
    
    tipo_orden = models.ForeignKey(TipoOrden, on_delete=models.PROTECT)
    problema = models.ForeignKey(Problema, on_delete=models.PROTECT)
    foto_obligatoria = models.CharField(max_length=1, blank=True, null=True)
    observacion_obligatoria = models.CharField(max_length=1, blank=True, null=True)
    datos_medidor = models.CharField(max_length=1, blank=True, null=True)
    activo = models.SmallIntegerField('Activo', default=1)


class ObservacionXAnomalia(models.Model):

    class Meta:
        verbose_name = "ObservacionXAnomalia"
        verbose_name_plural = "ObservacionXAnomalia"

    def __str__(self):
        return '{} {}'.format(self.codigo.codigo, self.anomalia)
    
    codigo = models.ForeignKey(Codigo, on_delete=models.PROTECT)
    anomalia = models.ForeignKey(Anomalia, on_delete=models.PROTECT)



class Parametro(models.Model):

    class Meta:
        verbose_name = "Parámetro"
        verbose_name_plural = "Parámetros"

    def __str__(self):
        return '{}-{}'.format(self.parametro, self.descripcion)
    

    parametro = models.CharField('Parámetro',primary_key=True, max_length=50)
    descripcion = models.CharField('Descripción', max_length=50,blank=True,null=True)
    valor_1 = models.CharField('Valor 1', max_length=100,blank=True,null=True)
    valor_2 = models.CharField('Valor 2', max_length=100,blank=True,null=True)
    parametro_movil = models.CharField('Parámetro para móvil',max_length=10,blank=True,null=True, default='0')

class Desc_Anomalia(models.Model):

    class Meta:
        verbose_name = "Desc_Anomalia"
        verbose_name_plural = "Desc_Anomalias"
        unique_together = (('orden_trabajo', 'id_anomalia'),)

    def __str__(self):
        return "{} {}".format(self.orden_trabajo,self.id_anomalia)
    
    id_descarga = models.CharField(max_length=50)
    orden_trabajo = models.ForeignKey(OrdenDeTrabajo, on_delete=models.PROTECT,db_index=True)
    id_anomalia = models.ForeignKey(Anomalia,on_delete=models.PROTECT)
    id_observacion = models.ForeignKey(Codigo,on_delete=models.PROTECT, blank=True, null=True)
    fecha_hora_registro = models.DateTimeField()
    paso_accion = models.CharField('paso acción', max_length=5, blank=True, null=True)
    oficina = models.ForeignKey(WorkUnit, on_delete=models.PROTECT,)
    tipo_resultado = models.ForeignKey(Codigo, on_delete=models.PROTECT,related_name='anom_tipo_resultado', blank=True, null=True)
    prioridad = models.IntegerField(default=0)
    comentario = models.CharField('Comentario', max_length=250, blank=True, null=True)


class Desc_AparatoAlta(models.Model):

    class Meta:
        verbose_name = "Desc_AparatoAlta"
        verbose_name_plural = "Desc_AparatosAlta"

    def __str__(self):
        pass
    
    id_descarga = models.CharField(max_length=50)
    orden_trabajo = models.ForeignKey(OrdenDeTrabajo, on_delete=models.PROTECT)
    secuencia_registro = models.IntegerField('secuencial registro')
    marca = models.ForeignKey(Codigo, related_name='marca_aparatoalta',on_delete=models.PROTECT,)
    num_serie = models.CharField('num. serie', max_length=50)   
    num_ruedas = models.SmallIntegerField('núm. ruedas')
    constante = models.FloatField('constante', default='1')
    tipo_servicio = models.ForeignKey(Codigo,related_name='tipo_servicio_aparatoalta', on_delete=models.PROTECT, blank=True, null=True)
    fecha_hora_registro = models.DateTimeField()
    paso_accion = models.CharField('paso acción', max_length=5, blank=True, null=True)
    oficina = models.ForeignKey(WorkUnit, on_delete=models.PROTECT,)
    lectura = models.IntegerField()
    fecha_hora_lectura = models.DateTimeField()
    num_serie_anterior = models.CharField('num. serie anterior', max_length=50, blank=True, null=True)
    nif_anterior = models.CharField('nif anterior', max_length=50, blank=True, null=True)
    num_serie_posterior = models.CharField('num. serie posterior', max_length=50, blank=True, null=True)
    nif_posterior = models.CharField('nif posterior', max_length=50, blank=True, null=True)
    observacion = models.CharField('observación', max_length=250, blank=True, null=True)


class Desc_AparatoModif(models.Model):

    class Meta:
        verbose_name = "Desc_AparatoModif"
        verbose_name_plural = "Desc_AparatosModif"

    def __str__(self):
        pass
    
    id_descarga = models.CharField( max_length=50)
    orden_trabajo = models.ForeignKey(OrdenDeTrabajo, on_delete=models.PROTECT)
    secuencia_registro = models.IntegerField('secuencial registro')
    marca = models.ForeignKey(Codigo, related_name='marca_aparato_modif',on_delete=models.PROTECT, blank=True, null=True)
    num_serie = models.CharField('num. serie', max_length=50)   
    paso_accion = models.CharField('paso acción', max_length=5, blank=True, null=True)
    oficina = models.ForeignKey(WorkUnit, on_delete=models.PROTECT,)
    observacion = models.CharField('observación', max_length=250, blank=True, null=True)
    lectura = models.IntegerField()


class Desc_Foto(models.Model):

    class Meta:
        verbose_name = "Desc_Foto"
        verbose_name_plural = "Desc_Fotos"
        #unique_together = (('orden_trabajo', 'fecha_hora_registro'),)        

    def __str__(self):
        return '{} {}'.format(self.orden_trabajo,self.fecha_hora_registro)
    
    id_descarga = models.CharField( max_length=50)
    orden_trabajo = models.ForeignKey(OrdenDeTrabajo, on_delete=models.PROTECT, db_index=True)
    fecha_hora_registro = models.DateTimeField()
    fecha = models.CharField('fecha', max_length=50)
    oficina = models.ForeignKey(WorkUnit, on_delete=models.PROTECT,)
    punto_suministro = models.CharField('Punto Suministro', max_length=50, db_index=True)
    descripcion_foto = models.CharField('descripcion', max_length=250)
    paso_accion = models.CharField('paso acción', max_length=5, blank=True, null=True)
    foto = models.BinaryField(blank=True, null=True,)


    def getFoto(self):
            import base64
            try:
                print('getFoto')
                r = base64.b64encode(self.foto)
                #r = '{}'.format(self.foto).encode('base64')
                return r
            except Exception as e:
                print(e)
                return 'Fallo'


class Desc_IndicadorPaso(models.Model):

    class Meta:
        verbose_name = "Desc_IndicadorPaso"
        verbose_name_plural = "Desc_IndicadorPasos"

    def __str__(self):
        pass
    
    id_descarga = models.CharField( max_length=50)
    orden_trabajo = models.ForeignKey(OrdenDeTrabajo, on_delete=models.PROTECT)
    fecha_hora_registro = models.DateTimeField()
    paso_accion = models.CharField('paso acción', max_length=5, blank=True, null=True)    
    indicador = models.CharField('indicador', max_length=50, blank=True, null=True)
    valor_indicador = models.CharField('valor indicador', max_length=50)
    oficina = models.ForeignKey(WorkUnit, on_delete=models.PROTECT,)


class Desc_Observacion(models.Model):

    class Meta:
        verbose_name = "Desc_Observacion"
        verbose_name_plural = "Desc_Observaciones"

    def __str__(self):
        pass
    
    id_descarga = models.CharField( max_length=50)
    orden_trabajo = models.ForeignKey(OrdenDeTrabajo, on_delete=models.PROTECT)
    fecha_hora_registro = models.DateTimeField()
    observacion = models.CharField('observacion', max_length=255)
    paso_accion = models.CharField('paso acción', max_length=5, blank=True, null=True)    
    oficina = models.ForeignKey(WorkUnit, on_delete=models.PROTECT,)


class Desc_Visita(models.Model):

    class Meta:
        verbose_name = "Desc_Visita"
        verbose_name_plural = "Desc_Visitas"

    def __str__(self):
        pass
    
    id_descarga = models.CharField( max_length=50)
    orden_trabajo = models.ForeignKey(OrdenDeTrabajo, on_delete=models.PROTECT)
    fecha_hora_visita = models.DateTimeField()
    accion_ejecutada = models.ForeignKey(Codigo, on_delete=models.PROTECT, default='AV001')
    observacion = models.CharField('observacion', max_length=255, blank=True, null=True)
    oficina = models.ForeignKey(WorkUnit, on_delete=models.PROTECT,)


class Desc_Lectura(models.Model):

    class Meta:
        verbose_name = "Desc_Lectura"
        verbose_name_plural = "Desc_Lecturas"

    def __str__(self):
        return "{} {}".format(self.num_serie,self.lectura)
    orden_trabajo = models.OneToOneField(OrdenDeTrabajo, on_delete=models.PROTECT)
    id_descarga = models.CharField( max_length=50)
    
    secuencia_registro = models.IntegerField()
    marca = models.ForeignKey(Codigo,on_delete=models.PROTECT)
    num_serie = models.CharField('num. serie', max_length=50)   
    tipo_consumo = models.ForeignKey(Codigo,related_name='tipo_consumo', on_delete=models.PROTECT)
    tipo_aparato = models.ForeignKey(Codigo,related_name='tipo_aparato_lectura', on_delete=models.PROTECT,blank=True,null=True)
    coef_perdida = models.CharField('coef. pérdida', max_length=50,blank=True,null=True)    
    constante = models.FloatField()
    lectura = models.IntegerField()
    consumo = models.IntegerField()
    paso_accion = models.CharField('paso acción', max_length=5, blank=True, null=True)   
    cantidad_intentos = models.SmallIntegerField()
    resultado_lectura = models.SmallIntegerField()
    consulto_historico = models.SmallIntegerField()
    oficina = models.ForeignKey(WorkUnit, on_delete=models.PROTECT,)
    lecturas_ingresadas = models.CharField('lecturas ingresadas', max_length=250, blank=True, null=True)

    
    def getDescripcion(self):
           
            try:

                if self.resultado_lectura == 2:
                   nombre = 'Alto consumo'
                elif self.resultado_lectura == 1:
                   nombre = 'Lectura normal'
                elif self.resultado_lectura == 3:
                   nombre = 'Bajo consumo'
                elif self.resultado_lectura == 4:
                   nombre = 'Sin Lectura'
                elif self.resultado_lectura == 5:
                   nombre = 'Lectura sin Controles'
                elif self.resultado_lectura == 6:
                  nombre = 'Consumo cero'
                elif self.resultado_lectura == 7:
                  nombre = 'Consumo negativo'  
                return nombre
            except Exception as e:
                print(e)
                return ' '


class Desc_Orden(models.Model):

    class Meta:
        verbose_name = "Desc_Orden"
        verbose_name_plural = "Desc_Ordenes"

    def __str__(self):
        return "{} {}".format(self.orden_trabajo,self.fh_fin)


    
    id_descarga = models.CharField( max_length=50)
    orden_trabajo = models.OneToOneField(OrdenDeTrabajo, on_delete=models.PROTECT)
    oficina = models.ForeignKey(WorkUnit, on_delete=models.PROTECT,)
    fecha_resolucion = models.DateField()
    fh_inicio = models.DateTimeField()
    fh_fin = models.DateTimeField()
    fh_descarga = models.DateTimeField()
    tecnico = models.ForeignKey(Tecnico, on_delete=models.PROTECT)
    gps_latitud = models.CharField(max_length=20, default="0.0")
    gps_longitud = models.CharField(max_length=20, default="0.0")
    secuencia_real  = models.IntegerField()
    trabajada_offline = models.SmallIntegerField(default=0)
    orden_modificada = models.SmallIntegerField(blank=True,null=True)
    fh_modificacion = models.DateTimeField(blank=True,null=True)
    usuario_modifico = models.CharField('usuario modificó', max_length=50,blank=True,null=True)
    orden_forzada = models.SmallIntegerField(blank=True,null=True)
    fh_forzado = models.DateTimeField(blank=True,null=True)
    usuario_forzo = models.CharField('usuario forzó', max_length=50,blank=True,null=True)


class Desc_Trabajo(models.Model):

    class Meta:
        verbose_name = "Desc_Trabajo"
        verbose_name_plural = "Desc_Trabajos"

    def __str__(self):
        pass
    
    id_descarga = models.CharField( max_length=50)
    orden_trabajo = models.ForeignKey(OrdenDeTrabajo, on_delete=models.PROTECT)
    oficina = models.ForeignKey(WorkUnit, on_delete=models.PROTECT,)
    trabajo_realizado = models.ForeignKey(Codigo, on_delete=models.PROTECT)
    fh_inicio = models.DateTimeField()
    fh_fin = models.DateTimeField()
    paso_accion = models.CharField('paso acción', max_length=5, blank=True, null=True)


class Desc_Problema(models.Model):

    class Meta:
        verbose_name = "Desc_Problema"
        verbose_name_plural = "Desc_Problemas"

    def __str__(self):
        pass
    
    id_descarga = models.CharField( max_length=50)
    orden_trabajo = models.ForeignKey(OrdenDeTrabajo, on_delete=models.PROTECT)
    oficina = models.ForeignKey(WorkUnit, on_delete=models.PROTECT,)
    problema = models.ForeignKey(Codigo, on_delete=models.PROTECT)
    observacion = models.CharField('observacion', max_length=150,blank=True,null=True)
    fh_inicio = models.DateTimeField()
    fh_fin = models.DateTimeField()
    paso_accion = models.CharField('paso acción', max_length=5, blank=True, null=True)


class Desc_Precinto(models.Model):

    class Meta:
        verbose_name = "Desc_Precinto"
        verbose_name_plural = "Desc_Precintos"

    def __str__(self):
        pass
    
    id_descarga = models.CharField( max_length=50)
    orden_trabajo = models.ForeignKey(OrdenDeTrabajo, on_delete=models.PROTECT)
    oficina = models.ForeignKey(WorkUnit, on_delete=models.PROTECT,)
    marca = models.ForeignKey(Codigo, related_name='marca_precinto',on_delete=models.PROTECT,)
    num_serie = models.CharField('num. serie', max_length=50) 
    num_precinto = models.CharField('num. precinto', max_length=50) 
    color = models.ForeignKey(Codigo, on_delete=models.PROTECT,blank=True,null=True)
    #accion 1 = instalado accion 0 = retirado
    accion = models.SmallIntegerField()

class Resguardo_OrdenTrabajo(models.Model):

   class Meta:
       verbose_name = "Resguardo_OrdenTrabajo"
       verbose_name_plural = "Resguardo_OrdenesTrabajo"

   def __str__(self):
       pass


   numero_orden = models.CharField('Número orden', primary_key=True, max_length=30)
   punto_suministro = models.ForeignKey(PuntoDeSuministro, on_delete=models.PROTECT)
   tipo_orden = models.ForeignKey(TipoOrden, on_delete=models.PROTECT)
   prioridad = models.SmallIntegerField(default=1)
   estado =  models.ForeignKey(EstadoOrden, on_delete=models.PROTECT)
   secuencial_registro = models.SmallIntegerField(default=0)
   secuencia_teorica = models.IntegerField(default=0)
   secuencia_real = models.IntegerField()

   oficina = models.ForeignKey(WorkUnit, on_delete=models.PROTECT,)
   ruta = models.ForeignKey(Ruta, on_delete=models.PROTECT)

   orden_terreno = models.SmallIntegerField(default=0)
   generada_desde_num_os  = models.CharField('generada desde', max_length=30,blank=True,null=True)

   tecnico = models.ForeignKey(Tecnico, on_delete=models.PROTECT,blank=True,null=True)
   usuario_asignacion = models.ForeignKey(EmserUser ,blank=True,null=True)

   fecha_hora_asignacion = models.CharField(max_length=14, blank=True, null=True)
   fecha_hora_importacion = models.CharField(max_length=14, blank=True, null=True)
   fecha_hora_exportacion = models.CharField(max_length=14, blank=True, null=True)
   fecha_hora_anulacion = models.CharField(max_length=14, blank=True, null=True)
   fecha_hora_ult_modificacion = models.CharField(max_length=14, blank=True, null=True)
   fecha_hora_carga = models.CharField(max_length=14, blank=True, null=True)

   id_descarga = models.CharField( max_length=50)

   fecha_resolucion = models.DateField()
   fh_inicio = models.DateTimeField()
   fh_fin = models.DateTimeField()
   fh_descarga = models.DateTimeField()

   gps_latitud = models.DecimalField(max_digits=9, decimal_places=7)
   gps_longitud = models.DecimalField(max_digits=9, decimal_places=7)

   trabajada_offline = models.SmallIntegerField(default=0)

   orden_modificada = models.SmallIntegerField(blank=True,null=True)
   fh_modificacion = models.DateTimeField(blank=True,null=True)
   usuario_modifico = models.CharField('usuario modificó', max_length=50,blank=True,null=True)
   orden_forzada = models.SmallIntegerField(blank=True,null=True)
   fh_forzado = models.DateTimeField(blank=True,null=True)
   usuario_forzo = models.CharField('usuario forzó', max_length=50,blank=True,null=True)


class Log_Auditoria(models.Model):

   class Meta:
       verbose_name = "Log_Auditoria"
       verbose_name_plural = "Log_Auditorias"

   def __str__(self):
       return '{} {} {} {} {}'.format(self.fh_registro,self.actividad,self.accion,self.usuario,self.datos)

   fh_registro = models.DateTimeField('fecha hora registro')
   actividad = models.CharField('actividad', max_length=50)
   accion = models.CharField('accion', max_length=50)
   usuario = models.CharField('usuario', max_length=50)
   datos = models.CharField('datos', max_length=1000)


class Resguardo_Anomalia(models.Model):

    class Meta:
        verbose_name = "Desc_Anomalia"
        verbose_name_plural = "Desc_Anomalias"

    def __str__(self):
        return "{} {}".format(self.orden_trabajo,self.id_anomalia)
    
    id_descarga = models.CharField(max_length=50)
    orden_trabajo = models.ForeignKey(OrdenDeTrabajo, on_delete=models.PROTECT)
    id_anomalia = models.ForeignKey(Anomalia,on_delete=models.PROTECT)
    id_observacion = models.ForeignKey(Codigo,on_delete=models.PROTECT, blank=True, null=True)
    fecha_hora_registro = models.DateTimeField()
    paso_accion = models.CharField('paso acción', max_length=5, blank=True, null=True)
    oficina = models.ForeignKey(WorkUnit, on_delete=models.PROTECT,)
    tipo_resultado = models.ForeignKey(Codigo, on_delete=models.PROTECT, related_name='resg_anom_tipo_resultado',blank=True, null=True)
    comentario = models.CharField('Comentario', max_length=250, blank=True, null=True)

class Resguardo_AparatoAlta(models.Model):

    class Meta:
        verbose_name = "Desc_AparatoAlta"
        verbose_name_plural = "Desc_AparatosAlta"

    def __str__(self):
        pass
    
    id_descarga = models.CharField(max_length=50)
    orden_trabajo = models.ForeignKey(OrdenDeTrabajo, on_delete=models.PROTECT)
    secuencia_registro = models.IntegerField('secuencial registro')
    marca = models.ForeignKey(Codigo, related_name='marca_raparatoalta',on_delete=models.PROTECT,)
    num_serie = models.CharField('num. serie', max_length=50)   
    num_ruedas = models.SmallIntegerField('núm. ruedas')
    constante = models.FloatField('constante', default='1')
    tipo_servicio = models.ForeignKey(Codigo,related_name='tipo_servicio_raparatoalta', on_delete=models.PROTECT, blank=True, null=True)
    fecha_hora_registro = models.DateTimeField()
    paso_accion = models.CharField('paso acción', max_length=5, blank=True, null=True)
    oficina = models.ForeignKey(WorkUnit, on_delete=models.PROTECT,)
    lectura = models.IntegerField()
    fecha_hora_lectura = models.DateTimeField()
    num_serie_anterior = models.CharField('num. serie anterior', max_length=50, blank=True, null=True)
    nif_anterior = models.CharField('nif anterior', max_length=50, blank=True, null=True)
    num_serie_posterior = models.CharField('num. serie posterior', max_length=50, blank=True, null=True)
    nif_posterior = models.CharField('nif posterior', max_length=50, blank=True, null=True)
    observacion = models.CharField('observación', max_length=250, blank=True, null=True)

class Resguardo_AparatoModif(models.Model):

    class Meta:
        verbose_name = "Desc_AparatoModif"
        verbose_name_plural = "Desc_AparatosModif"

    def __str__(self):
        pass
    
    id_descarga = models.CharField( max_length=50)
    orden_trabajo = models.ForeignKey(OrdenDeTrabajo, on_delete=models.PROTECT)
    secuencia_registro = models.IntegerField('secuencial registro')
    marca = models.ForeignKey(Codigo, related_name='marca_raparato_modif',on_delete=models.PROTECT, blank=True, null=True)
    num_serie = models.CharField('num. serie', max_length=50)   
    paso_accion = models.CharField('paso acción', max_length=5, blank=True, null=True)
    oficina = models.ForeignKey(WorkUnit, on_delete=models.PROTECT,)
    observacion = models.CharField('observación', max_length=250, blank=True, null=True)
    lectura = models.IntegerField()


class Resguardo_Foto(models.Model):

    class Meta:
        verbose_name = "Desc_Foto"
        verbose_name_plural = "Desc_Fotos"
        unique_together = (('orden_trabajo', 'fecha_hora_registro'),)        

    def __str__(self):
        pass
    
    id_descarga = models.CharField( max_length=50)
    orden_trabajo = models.ForeignKey(OrdenDeTrabajo, on_delete=models.PROTECT)
    fecha_hora_registro = models.DateTimeField()
    fecha = models.CharField('fecha', max_length=50)
    oficina = models.ForeignKey(WorkUnit, on_delete=models.PROTECT,)
    punto_suministro = models.CharField('Punto Suministro', primary_key=True, max_length=50)
    descripcion_foto = models.CharField('descripcion', max_length=250)
    paso_accion = models.CharField('paso acción', max_length=5, blank=True, null=True)
    foto = models.BinaryField(blank=True, null=True,)


    def getFoto(self):
            import base64
            try:
                print('getFoto')
                r = base64.b64encode(self.foto)
                #r = '{}'.format(self.foto).encode('base64')
                return r
            except Exception as e:
                print(e)
                return 'Fallo'


class Resguardo_IndicadorPaso(models.Model):

    class Meta:
        verbose_name = "Desc_IndicadorPaso"
        verbose_name_plural = "Desc_IndicadorPasos"

    def __str__(self):
        pass
    
    id_descarga = models.CharField( max_length=50)
    orden_trabajo = models.ForeignKey(OrdenDeTrabajo, on_delete=models.PROTECT)
    fecha_hora_registro = models.DateTimeField()
    paso_accion = models.CharField('paso acción', max_length=5, blank=True, null=True)    
    indicador = models.CharField('indicador', max_length=50)
    valor_indicador = models.CharField('valor indicador', max_length=50)
    oficina = models.ForeignKey(WorkUnit, on_delete=models.PROTECT,)


class Resguardo_Observacion(models.Model):

    class Meta:
        verbose_name = "Desc_Observacion"
        verbose_name_plural = "Desc_Observaciones"

    def __str__(self):
        pass
    
    id_descarga = models.CharField( max_length=50)
    orden_trabajo = models.ForeignKey(OrdenDeTrabajo, on_delete=models.PROTECT)
    fecha_hora_registro = models.DateTimeField()
    observacion = models.CharField('observacion', max_length=255)
    paso_accion = models.CharField('paso acción', max_length=5, blank=True, null=True)    
    oficina = models.ForeignKey(WorkUnit, on_delete=models.PROTECT,)


class Resguardo_Visita(models.Model):

    class Meta:
        verbose_name = "Desc_Visita"
        verbose_name_plural = "Desc_Visitas"

    def __str__(self):
        pass
    
    id_descarga = models.CharField( max_length=50)
    orden_trabajo = models.ForeignKey(OrdenDeTrabajo, on_delete=models.PROTECT)
    fecha_hora_visita = models.DateTimeField()
    accion_ejecutada = models.ForeignKey(Codigo, on_delete=models.PROTECT, default='AV001')
    observacion = models.CharField('observacion', max_length=255, blank=True, null=True)
    oficina = models.ForeignKey(WorkUnit, on_delete=models.PROTECT,)


class Resguardo_Lectura(models.Model):

    class Meta:
        verbose_name = "Desc_Lectura"
        verbose_name_plural = "Desc_Lecturas"

    def __str__(self):
        return "{} {}".format(self.num_serie,self.lectura)
    
    id_descarga = models.CharField( max_length=50)
    orden_trabajo = models.ForeignKey(OrdenDeTrabajo, on_delete=models.PROTECT)
    secuencia_registro = models.IntegerField()
    marca = models.ForeignKey(Codigo, related_name='rmarca_lectura',on_delete=models.PROTECT,)
    num_serie = models.CharField('num. serie', max_length=50)   
    tipo_consumo = models.ForeignKey(Codigo,related_name='rtipo_consumo', on_delete=models.PROTECT)
    tipo_aparato = models.ForeignKey(Codigo,related_name='rtipo_aparato_lectura', on_delete=models.PROTECT,blank=True,null=True)
    coef_perdida = models.CharField('coef. pérdida', max_length=50,blank=True,null=True)    
    constante = models.FloatField()
    lectura = models.IntegerField()
    consumo = models.IntegerField()
    paso_accion = models.CharField('paso acción', max_length=5, blank=True, null=True)   
    cantidad_intentos = models.SmallIntegerField()
    resultado_lectura = models.SmallIntegerField()
    consulto_historico = models.SmallIntegerField()
    oficina = models.ForeignKey(WorkUnit, on_delete=models.PROTECT,)
    tope_lectura_minima = models.IntegerField(default=0)
    tope_lectura_maxima = models.IntegerField(default=0)

    def getDescripcion(self):
           
            try:
                print('getDescricion')
                if self.resultado_lectura == 2:
                   nombre = 'Alto consumo'
                elif self.resultado_lectura == 1:
                   nombre = 'Lectura normal'
                elif self.resultado_lectura == 3:
                   nombre = 'Lectura menor'
                elif self.resultado_lectura == 4:
                   nombre = 'Sin Lectura'
                elif self.resultado_lectura == 5:
                   nombre = 'Lectura sin Controles'
               
                return nombre
            except Exception as e:
                print(e)
                return ' '

class Resguardo_Trabajo(models.Model):

    class Meta:
        verbose_name = "Desc_Trabajo"
        verbose_name_plural = "Desc_Trabajos"

    def __str__(self):
        pass
    
    id_descarga = models.CharField( max_length=50)
    orden_trabajo = models.ForeignKey(OrdenDeTrabajo, on_delete=models.PROTECT)
    oficina = models.ForeignKey(WorkUnit, on_delete=models.PROTECT,)
    trabajo_realizado = models.ForeignKey(Codigo, on_delete=models.PROTECT)
    fh_inicio = models.DateTimeField()
    fh_fin = models.DateTimeField()
    paso_accion = models.CharField('paso acción', max_length=5, blank=True, null=True)


class Resguardo_Problema(models.Model):

    class Meta:
        verbose_name = "Desc_Problema"
        verbose_name_plural = "Desc_Problemas"

    def __str__(self):
        pass
    
    id_descarga = models.CharField( max_length=50)
    orden_trabajo = models.ForeignKey(OrdenDeTrabajo, on_delete=models.PROTECT)
    oficina = models.ForeignKey(WorkUnit, on_delete=models.PROTECT,)
    problema = models.ForeignKey(Codigo, on_delete=models.PROTECT)
    observacion = models.CharField('observacion', max_length=150,blank=True,null=True)
    fh_inicio = models.DateTimeField()
    fh_fin = models.DateTimeField()
    paso_accion = models.CharField('paso acción', max_length=5, blank=True, null=True)


class Resguardo_Precinto(models.Model):

    class Meta:
        verbose_name = "Desc_Precinto"
        verbose_name_plural = "Desc_Precintos"

    def __str__(self):
        pass
    
    id_descarga = models.CharField( max_length=50)
    orden_trabajo = models.ForeignKey(OrdenDeTrabajo, on_delete=models.PROTECT)
    oficina = models.ForeignKey(WorkUnit, on_delete=models.PROTECT,)
    marca = models.ForeignKey(Codigo, related_name='rmarca_precinto',on_delete=models.PROTECT,)
    num_serie = models.CharField('num. serie', max_length=50) 
    num_precinto = models.CharField('num. precinto', max_length=50) 
    color = models.ForeignKey(Codigo, on_delete=models.PROTECT,blank=True,null=True)
    #accion 1 = instalado accion 0 = retirado
    accion = models.SmallIntegerField()  


class ProcesoImpExp(models.Model):

    class Meta:
        verbose_name = "ProcesoImpExp"
        verbose_name_plural = "ProcesosImpExp"

    def __str__(self):
        '{}:{} - estado: {} - {} - fh_inicio: {} - fh_fin: {}'.format(str(self.proceso),self.nombre_proceso,str(self.estado_proceso),str(self.tipo_proceso), str(self.fh_inicio_proceso), str(self.fh_fin_proceso))

    oficina = models.ForeignKey(WorkUnit, on_delete=models.PROTECT,)
    proceso = models.SmallIntegerField('proceso')
    nombre_proceso = models.CharField('nombre proceso', max_length=100,blank=True,null=True)
    descripcion_proceso = models.CharField('descripción del proceso', max_length=100,blank=True,null=True)
    tipo_proceso = models.CharField('tipo proceso', max_length=1,blank=True,null=True)
    estado_proceso = models.IntegerField('estado del proceso',default =0 )
    fh_inicio_proceso = models.CharField('fecha y hora de inicio', max_length=20,blank=True,null=True)
    fh_fin_proceso = models.CharField('fecha y hora de fin', max_length=20,blank=True,null=True)
    ejecutado_por = models.CharField('ejecutado por', max_length=100,blank=True,null=True)
    parametros_proceso = models.CharField('parámetros del proceso', max_length=250,blank=True,null=True)
    total=models.IntegerField('total',default=0)
    estado=models.CharField('estado',max_length=20,blank=True,null=True)

class Reorganizar(models.Model):
    class Meta:
        verbose_name="Reorganizar"
        verbose_name_plural="Reorganizar"

    ruta=models.ForeignKey(Ruta,on_delete=models.PROTECT,)
    fecha_solicitud=models.DateTimeField(blank=True,null=True)
    tecnico_solicito=models.ForeignKey(Tecnico,on_delete=models.PROTECT,)
    fecha_autorizado=models.DateTimeField(blank=True,null=True)
    fecha_denegado=models.DateTimeField(blank=True,null=True)
    usuario=models.ForeignKey(EmserUser,on_delete=models.PROTECT,blank=True,null=True)
    oficina=models.ForeignKey(WorkUnit,on_delete=models.PROTECT,blank=True,null=True)

class ConfigAccion_Cabe(models.Model):
    class Meta:
        verbose_name = "Configuración acción cabecera"
        verbose_name_plural = "Configuración acciones cabecera"

    def __str__(self):
        return "{}-{}".format(self.codigo,self.descripcion)

    codigo = models.CharField( 'Código', max_length=50,primary_key=True)
    descripcion = models.CharField('Descripcion', max_length=100,blank=False,null=False)
    activo = models.SmallIntegerField(default=1)
    fecha_vigencia= models.DateField('Fecha vigencia',blank=True,null=True)
    ultima_modif = models.DateTimeField('Fecha última modificación',blank=True,null=True)
    usuario_modif = models.CharField('ejecutado por', max_length=100,blank=True,null=True)
    filtros_clientes = models.CharField(max_length=512,blank=True,null=True)
    
class ConfigAccion_Deta(models.Model):
    class Meta:
        verbose_name = "Configuración acciones detalle"
        verbose_name_plural = "Configuración acciones detalle"

    def __str__(self):
        return "{}-{}-}{}-{}".format(self.codigo_config_accion,self.codigo_accion,self.tipo_accion,self.orden_ejecucion)

    codigo_accion = models.ForeignKey(Codigo, on_delete=models.CASCADE,)
    codigo_config_accion = models.ForeignKey(ConfigAccion_Cabe, on_delete=models.CASCADE,)
    tipo_accion = models.CharField('Tipo acción', max_length=50,blank=False,null=False)
    orden_ejecucion =models.SmallIntegerField(default=0)
    parametro_adicional = models.CharField('Parametro adicional', max_length=100,blank=True,null=True)
    obligatorio = models.SmallIntegerField('Obligatorio',default=1)

class ConfigAccion_Cliente(models.Model):
    class Meta:
        verbose_name = "Configuración acciones cliente"
        verbose_name_plural = "Configuración acciones cliente"

        unique_together = (('codigo_config_accion_cabe', 'codigo_cliente','codigo_punto_suministro'),)

    def __str__(self):
        return "{}-{}-}".format(self.codigo_config_accion_cabe,self.codigo_cliente,self.codigo_punto_suministro)

    codigo_config_accion_cabe = models.ForeignKey(ConfigAccion_Cabe, on_delete=models.CASCADE,)
    codigo_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE,)
    codigo_punto_suministro = models.ForeignKey(PuntoDeSuministro, on_delete=models.CASCADE,null=True,blank=True)

class Desc_Accion(models.Model):
    
    class Meta:
        verbose_name = "Descarga acción"
        verbose_name_plural = "Descarga acciones"

    id_descarga = models.CharField( max_length=50)
    orden_trabajo = models.ForeignKey(OrdenDeTrabajo, on_delete=models.PROTECT)
    fecha_hora_registro = models.DateTimeField()
    punto_suministro = models.CharField('Punto Suministro', max_length=50,blank=True, null=True)
    num_contrato = models.CharField('Num.Contrato', max_length=50,blank=True, null=True)
    codigo_accion = models.ForeignKey(Codigo, on_delete=models.PROTECT,)
    codigo_config_accion = models.ForeignKey(ConfigAccion_Cabe, on_delete=models.PROTECT,)
    tipo_accion = models.CharField('Tipo acción', max_length=50,blank=False,null=False)
    parametro_adicional = models.CharField('Parametro adicional', max_length=100,blank=True,null=True)
    oficina = models.ForeignKey(WorkUnit, on_delete=models.PROTECT,)
    paso_accion = models.CharField('paso acción', max_length=5, blank=True, null=True)
    valor_binario_relevado = models.FileField('Multimedia relevado',blank=True, null=True,)
    valor_texto_relevado= models.CharField('texto relevado', max_length=500, blank=True, null=True)

class HistoricoConfigAccion_Cliente(models.Model):
    class Meta:
        verbose_name = "Historico Configuración acciones cliente"
        verbose_name_plural = "Historico Configuración acciones cliente"

        unique_together = (('codigo_config_accion_cabe', 'codigo_cliente','codigo_punto_suministro','fecha'),)

    def __str__(self):
        return "{}-{}-}".format(self.codigo_config_accion_cabe,self.codigo_cliente,self.codigo_punto_suministro)

    codigo_config_accion_cabe = models.ForeignKey(ConfigAccion_Cabe, on_delete=models.CASCADE,)
    codigo_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE,)
    codigo_punto_suministro = models.ForeignKey(PuntoDeSuministro, on_delete=models.CASCADE,null=True,blank=True)
    fecha = models.DateTimeField(blank=True,null=True)
    usuario_asignacion = models.ForeignKey(EmserUser ,blank=True, null=True)


class porcionessemana(models.Model):
    class Meta:
        verbose_name="porcionessemana"
        verbose_name_plural="porcionessemanas"

    PORCION= models.CharField('PORCION', max_length=100,blank=True,null=True)
    SEMANA=models.CharField('SEMANA',max_length=100,blank=True,null=True)
    REGION=models.CharField('REGION',max_length=100,blank=True,null=True)
    DISTRITO=models.CharField('DISTRITO',max_length=100,blank=True,null=True)
    DESCDISTRITO=models.CharField('DESCDISTRITO',max_length=100,blank=True,null=True)



     
class semanasgu(models.Model):
    class Meta:
        verbose_name="semanasgu"
        verbose_name_plural="semanasgu"

    NROEQUIP=models.FloatField('NROEQUIP',blank=True,null=True)
    PORCION=models.CharField('PORCION',max_length=100,blank=True,null=True)
    DIST=models.SmallIntegerField('DIST',blank=True,null=True)
    UNIDAD=models.CharField('UNIDAD',max_length=100,blank=True,null=True)
    NROPUERT=models.FloatField('NROPUERT',blank=True,null=True)
    SEC=models.SmallIntegerField('SEC',blank=True,null=True)
    INTERLOC=models.FloatField('INTERLOC',blank=True,null=True)
    CLIENTE=models.CharField('CLIENTE',max_length=100,blank=True,null=True)
    CALLE=models.CharField('CALLE',max_length=100,blank=True,null=True)
    DIREXION=models.FloatField('DIREXION',blank=True,null=True)
    CORTE=models.CharField('CORTE',max_length=100,blank=True,null=True)
    NROSERIE=models.CharField('NROSERIE',max_length=100,blank=True,null=True)
    CLASE_AP=models.CharField('CLASE_AP',max_length=100,blank=True,null=True)
    MARCA=models.CharField('MARCA',max_length=100,blank=True,null=True)
    TEX_DIV=models.CharField('TEX_DIV',max_length=100,blank=True,null=True)
    DIAMED=models.CharField('DIAMED',max_length=100,blank=True,null=True)
    CONS_EST=models.FloatField('CONS_EST',blank=True,null=True)
    CONS_MIN=models.FloatField('CONS_MIN',blank=True,null=True)
    CONS_MAX=models.FloatField('CONS_MAX',blank=True,null=True)
    INC_1=models.SmallIntegerField('INC_1',blank=True,null=True)
    LECT_1=models.FloatField('LECT_1',blank=True,null=True)
    CONS_1=models.FloatField('CONS_1',blank=True,null=True)
    PLANIF_1=models.FloatField('PLANIF_1',blank=True,null=True)
    INC_2=models.SmallIntegerField('INC_2',blank=True,null=True)
    LECT_2=models.FloatField('LECT_2',blank=True,null=True)
    CONS_2=models.FloatField('CONS_2',blank=True,null=True)
    PLANIF_2=models.FloatField('PLANIF_2',blank=True,null=True)
    INC_3=models.SmallIntegerField('INC_3',blank=True,null=True)
    LECT_3=models.FloatField('LECT_3',blank=True,null=True)
    CONS_3=models.FloatField('CONS_3',blank=True,null=True)
    PLANIF_3=models.FloatField('PLANIF_3',blank=True,null=True)
    INC_4=models.SmallIntegerField('INC_4',blank=True,null=True)
    LECT_4=models.FloatField('LECT_4',blank=True,null=True)
    CONS_4=models.FloatField('CONS_4',blank=True,null=True)
    PLANIF_4=models.FloatField('PLANIF_4',blank=True,null=True)
    INC_5=models.SmallIntegerField('INC_5',blank=True,null=True)
    LECT_5=models.FloatField('LECT_5',blank=True,null=True)
    CONS_5=models.FloatField('CONS_5',blank=True,null=True)
    PLANIF_5=models.FloatField('PLANIF_5',blank=True,null=True)
    INC_6=models.SmallIntegerField('INC_6',blank=True,null=True)
    LECT_6=models.FloatField('LECT_6',blank=True,null=True)
    CONS_6=models.FloatField('CONS_6',blank=True,null=True)
    PLANIF_6=models.FloatField('PLANIF_6',blank=True,null=True)
    INC_REC=models.SmallIntegerField('INC_REC',blank=True,null=True)
    LEC_RET=models.FloatField('LEC_RET',blank=True,null=True)
    CONS_RET=models.FloatField('CONS_RET',blank=True,null=True)
    FEC_REC=models.FloatField('FEC_REC',blank=True,null=True)
    CON_ACUM=models.FloatField('CON_ACUM',blank=True,null=True)
    ULT_LECT=models.FloatField('ULT_LECT',blank=True,null=True)
    ANIO_INS=models.CharField('ANIO_INS',max_length=100,blank=True,null=True)
    TIPO_CON=models.CharField('TIPO_CON',max_length=100,blank=True,null=True)
    DIGITOS=models.SmallIntegerField('DIGITOS',blank=True,null=True)
    CODPOST=models.CharField('CODPOST',max_length=100,blank=True,null=True)
    DCSM=models.CharField('DCSM',max_length=100,blank=True,null=True)
    PORCION_ORIGINAL=models.CharField('PORCION_ORIGINAL',max_length=100,blank=True,null=True)
    SEC_ORIGINAL=models.SmallIntegerField('SEC_ORIGINAL',blank=True,null=True)
    DISTRITO=models.CharField('DISTRITO',max_length=100,blank=True,null=True)
    CIRC=models.CharField('CIRC',max_length=100,blank=True,null=True)
    SECCION=models.CharField('SECCION',max_length=100,blank=True,null=True)
    MANZANA=models.CharField('MANZANA',max_length=100,blank=True,null=True)
    UNIDAD_ORIGINAL=models.CharField('UNIDAD_ORIGINAL',max_length=100,blank=True,null=True)
    ORDENADO_POR=models.CharField('ORDENADO_POR',max_length=100,blank=True,null=True)
    SEC_RELACIONADA=models.IntegerField('SEC_RELACIONADA',blank=True,null=True)
    LAT=models.FloatField('LAT',blank=True,null=True)
    LON=models.FloatField('LON',blank=True,null=True)
    SEMANA=models.SmallIntegerField('SEMANA',blank=True,null=True)
    EXP=models.CharField('EXP',max_length=100,blank=True,null=True)
    EXPSAP=models.CharField('EXPSAP',max_length=100,blank=True,null=True)


class semanasre(models.Model):
    class Meta:
        verbose_name="semanasre"
        verbose_name_plural="semanasre"

    NROEQUIP=models.FloatField('NROEQUIP',blank=True,null=True)
    PORCION=models.CharField('PORCION',max_length=100,blank=True,null=True)
    DIST=models.SmallIntegerField('DIST',blank=True,null=True)
    UNIDAD=models.CharField('UNIDAD',max_length=100,blank=True,null=True)
    NROPUERT=models.FloatField('NROPUERT',blank=True,null=True)
    SEC=models.SmallIntegerField('SEC',blank=True,null=True)
    INTERLOC=models.FloatField('INTERLOC',blank=True,null=True)
    CLIENTE=models.CharField('CLIENTE',max_length=100,blank=True,null=True)
    CALLE=models.CharField('CALLE',max_length=100,blank=True,null=True)
    DIREXION=models.FloatField('DIREXION',blank=True,null=True)
    CORTE=models.CharField('CORTE',max_length=100,blank=True,null=True)
    NROSERIE=models.CharField('NROSERIE',max_length=100,blank=True,null=True)
    CLASE_AP=models.CharField('CLASE_AP',max_length=100,blank=True,null=True)
    MARCA=models.CharField('MARCA',max_length=100,blank=True,null=True)
    TEX_DIV=models.CharField('TEX_DIV',max_length=100,blank=True,null=True)
    DIAMED=models.CharField('DIAMED',max_length=100,blank=True,null=True)
    CONS_EST=models.FloatField('CONS_EST',blank=True,null=True)
    CONS_MIN=models.FloatField('CONS_MIN',blank=True,null=True)
    CONS_MAX=models.FloatField('CONS_MAX',blank=True,null=True)
    INC_1=models.SmallIntegerField('INC_1',blank=True,null=True)
    LECT_1=models.FloatField('LECT_1',blank=True,null=True)
    CONS_1=models.FloatField('CONS_1',blank=True,null=True)
    PLANIF_1=models.FloatField('PLANIF_1',blank=True,null=True)
    INC_2=models.SmallIntegerField('INC_2',blank=True,null=True)
    LECT_2=models.FloatField('LECT_2',blank=True,null=True)
    CONS_2=models.FloatField('CONS_2',blank=True,null=True)
    PLANIF_2=models.FloatField('PLANIF_2',blank=True,null=True)
    INC_3=models.SmallIntegerField('INC_3',blank=True,null=True)
    LECT_3=models.FloatField('LECT_3',blank=True,null=True)
    CONS_3=models.FloatField('CONS_3',blank=True,null=True)
    PLANIF_3=models.FloatField('PLANIF_3',blank=True,null=True)
    INC_4=models.SmallIntegerField('INC_4',blank=True,null=True)
    LECT_4=models.FloatField('LECT_4',blank=True,null=True)
    CONS_4=models.FloatField('CONS_4',blank=True,null=True)
    PLANIF_4=models.FloatField('PLANIF_4',blank=True,null=True)
    INC_5=models.SmallIntegerField('INC_5',blank=True,null=True)
    LECT_5=models.FloatField('LECT_5',blank=True,null=True)
    CONS_5=models.FloatField('CONS_5',blank=True,null=True)
    PLANIF_5=models.FloatField('PLANIF_5',blank=True,null=True)
    INC_6=models.SmallIntegerField('INC_6',blank=True,null=True)
    LECT_6=models.FloatField('LECT_6',blank=True,null=True)
    CONS_6=models.FloatField('CONS_6',blank=True,null=True)
    PLANIF_6=models.FloatField('PLANIF_6',blank=True,null=True)
    INC_REC=models.SmallIntegerField('INC_REC',blank=True,null=True)
    LEC_RET=models.FloatField('LEC_RET',blank=True,null=True)
    CONS_RET=models.FloatField('CONS_RET',blank=True,null=True)
    FEC_REC=models.FloatField('FEC_REC',blank=True,null=True)
    CON_ACUM=models.FloatField('CON_ACUM',blank=True,null=True)
    ULT_LECT=models.FloatField('ULT_LECT',blank=True,null=True)
    ANIO_INS=models.CharField('ANIO_INS',max_length=100,blank=True,null=True)
    TIPO_CON=models.CharField('TIPO_CON',max_length=100,blank=True,null=True)
    DIGITOS=models.SmallIntegerField('DIGITOS',blank=True,null=True)
    CODPOST=models.CharField('CODPOST',max_length=100,blank=True,null=True)
    DCSM=models.CharField('DCSM',max_length=100,blank=True,null=True)
    PORCION_ORIGINAL=models.CharField('PORCION_ORIGINAL',max_length=100,blank=True,null=True)
    SEC_ORIGINAL=models.SmallIntegerField('SEC_ORIGINAL',blank=True,null=True)
    DISTRITO=models.CharField('DISTRITO',max_length=100,blank=True,null=True)
    CIRC=models.CharField('CIRC',max_length=100,blank=True,null=True)
    SECCION=models.CharField('SECCION',max_length=100,blank=True,null=True)
    MANZANA=models.CharField('MANZANA',max_length=100,blank=True,null=True)
    UNIDAD_ORIGINAL=models.CharField('UNIDAD_ORIGINAL',max_length=100,blank=True,null=True)
    ORDENADO_POR=models.CharField('ORDENADO_POR',max_length=100,blank=True,null=True)
    SEC_RELACIONADA=models.IntegerField('SEC_RELACIONADA',blank=True,null=True)
    LAT=models.FloatField('LAT',blank=True,null=True)
    LON=models.FloatField('LON',blank=True,null=True)
    SEMANA=models.SmallIntegerField('SEMANA',blank=True,null=True)
    EXP=models.CharField('EXP',max_length=100,blank=True,null=True)
    EXPSAP=models.CharField('EXPSAP',max_length=100,blank=True,null=True)



class suministros(models.Model):
    class Meta:
        verbose_name="suministros"
        verbose_name_plural="suministros"
    def __str__(self):
        return '{}'.format(self.SEG_REG)

    COD_UNICOM=models.CharField('COD_UNICOM',max_length=100,blank=True,null=True)
    RUTA=models.CharField('RUTA',max_length=100,blank=True,null=True)
    ITINERARIO=models.CharField('ITINERARIO',max_length=100,blank=True,null=True)
    CICLO=models.CharField('CICLO',max_length=100,blank=True,null=True)
    ANIO=models.CharField('ANIO',max_length=100,blank=True,null=True)
    SEG_REG=models.CharField('SEG_REG',max_length=100,blank=True,null=True)
    DIVISION=models.CharField('DIVISION',max_length=100,blank=True,null=True)
    SECUENCIA=models.IntegerField('SECUENCIA',blank=True,null=True)
    LOCALIDAD=models.CharField('LOCALIDAD',max_length=100,blank=True,null=True)
    NOMBRE_CLIENTE=models.CharField('NOMBRE_CLIENTE',max_length=100,blank=True,null=True)
    DIRECCION=models.CharField('DIRECCION',max_length=100,blank=True,null=True)
    NRO_PUERTA=models.DecimalField(max_digits=8, decimal_places=7)
    PISO=models.CharField('PISO',max_length=100,blank=True,null=True)
    DUPLICADOR=models.CharField('DUPLICADOR',max_length=100,blank=True,null=True)
    NRO_APARTO=models.CharField('NRO_APARTO',max_length=100,blank=True,null=True)
    COD_MARCA=models.CharField('COD_MARCA',max_length=100,blank=True,null=True)
    RUEDAS=models.SmallIntegerField('RUEDAS',blank=True,null=True)
    MULTIPLICADOR=models.SmallIntegerField('MULTIPLICADOR',blank=True,null=True)
    LECTURA_ANTERIOR=models.DecimalField(max_digits=8,decimal_places=7)
    LECTURA_MINIMA=models.DecimalField(max_digits=8,decimal_places=7)
    LECTURA_MAXIMA=models.DecimalField(max_digits=8,decimal_places=7)
    DESC_CONSUMO=models.CharField('DESC_CONSUMO',max_length=100,blank=True,null=True)
    ACCESO_FINCA=models.CharField('ACCESO_FINCA',max_length=100,blank=True,null=True)
    ACCESO_PM=models.CharField('ACCESO_PM',max_length=100,blank=True,null=True)
    ESTADO_LECT=models.CharField('ESTADO_LECT',max_length=100,blank=True,null=True)
    ESTADO_SUM=models.CharField('ESTADO_SUM',max_length=100,blank=True,null=True)
    ESTADO_ACT=models.CharField('ESTADO_ACT',max_length=100,blank=True,null=True)
    COD_TARIFA=models.CharField('COD_TARIFA',max_length=100,blank=True,null=True)
    LECTURA_ACTUAL=models.DecimalField(max_digits=8,decimal_places=7)
    TIP_CONSUMO=models.CharField('TIP_CONSUMO',max_length=100,blank=True,null=True)
    FH_LECTURA=models.CharField('FH_LECTURA',max_length=100,blank=True,null=True)
    CONSUMO=models.DecimalField(max_digits=8,decimal_places=7)
    CANT_LECT_FORZADA=models.IntegerField('CANT_LECT_FORZADA',blank=True,null=True)
    NRO_LECTURISTA=models.IntegerField('NRO_LECTURISTA',blank=True,null=True)
    COD_COLECTOR=models.CharField('COD_COLECTOR',max_length=100,blank=True,null=True)
    COD_ANOMALIA_HH_1=models.CharField('COD_ANOMALIA_HH_1',max_length=100,blank=True,null=True)
    NOTAS1=models.CharField('NOTAS1',max_length=100,blank=True,null=True)
    COD_ANOMALIA_HH_2=models.CharField('COD_ANOMALIA_HH_2',max_length=100,blank=True,null=True)
    NOTAS2=models.CharField('NOTAS2',max_length=100,blank=True,null=True)
    COD_ANOMALIA_HH_3=models.CharField('COD_ANOMALIA_HH_3',max_length=100,blank=True,null=True)
    NOTAS3=models.CharField('NOTAS3',max_length=100,blank=True,null=True)
    SECUENCIA_REAL=models.IntegerField('SECUENCIA_REAL',blank=True,null=True)
    NRO_CLIENTE=models.CharField('NRO_CLIENTE',max_length=100,blank=True,null=True)
    COMPLEMENTO=models.CharField('COMPLEMENTO',max_length=100,blank=True,null=True)
    CONSUMO_ESTIMADO=models.DecimalField(max_digits=8,decimal_places=7)
    COD_ANOMALIA1=models.CharField('COD_ANOMALIA1',max_length=100,blank=True,null=True)
    LECTURA1=models.IntegerField()
    CONSUMO1=models.IntegerField()
    FECHA_LECTURA1=models.CharField('FECHA_LECTURA1',max_length=100,blank=True,null=True)
    COD_ANOMALIA2=models.CharField('COD_ANOMALIA2',max_length=100,blank=True,null=True)
    LECTURA2=models.IntegerField()
    CONSUMO2=models.IntegerField()
    FECHA_LECTURA2=models.CharField('FECHA_LECTURA2',max_length=100,blank=True,null=True)
    COD_ANOMALIA3=models.CharField('COD_ANOMALIA3',max_length=100,blank=True,null=True)
    LECTURA3=models.IntegerField()
    CONSUMO3=models.IntegerField()
    FECHA_LECTURA3=models.CharField('FECHA_LECTURA3',max_length=100,blank=True,null=True)
    COD_ANOMALIA4=models.CharField('COD_ANOMALIA4',max_length=100,blank=True,null=True)
    LECTURA4=models.IntegerField()
    CONSUMO4=models.IntegerField()
    FECHA_LECTURA4=models.CharField('FECHA_LECTURA4',max_length=100,blank=True,null=True)
    COD_ANOMALIA5=models.CharField('COD_ANOMALIA5',max_length=100,blank=True,null=True)
    LECTURA5=models.IntegerField()
    CONSUMO5=models.IntegerField()
    FECHA_LECTURA5=models.CharField('FECHA_LECTURA5',max_length=100,blank=True,null=True)
    COD_ANOMALIA6=models.CharField('COD_ANOMALIA6',max_length=100,blank=True,null=True)
    LECTURA6=models.IntegerField()
    CONSUMO6=models.IntegerField()
    FECHA_LECTURA6=models.CharField('FECHA_LECTURA6',max_length=100,blank=True,null=True)
    COD_RECAMBIO=models.CharField('COD_RECAMBIO',max_length=100,blank=True,null=True)
    LEC_MEDIDOR_RETIRADO=models.DecimalField(max_digits=8,decimal_places=7)
    CONSUMO_ULTIMO_RECAMBIO=models.DecimalField(max_digits=8,decimal_places=7)
    FECHA_RECAMBIO=models.CharField('FECHA_RECAMBIO',max_length=100,blank=True,null=True)
    ACUM_CONS_VARIOS_RECAMBIOS=models.DecimalField(max_digits=8,decimal_places=7)
    ANIO_INSTALACION=models.DecimalField(max_digits=10,decimal_places=7)
    COD_TIPO_CONEXION=models.CharField('COD_TIPO_CONEXION',max_length=100,blank=True,null=True)
    TIPO_MEDIDOR=models.CharField('TIPO_MEDIDOR',max_length=100,blank=True,null=True)
    COD_DIAMETRO=models.CharField('COD_DIAMETRO',max_length=100,blank=True,null=True)
    CONSULTO_HISTORICOS=models.CharField('CONSULTO_HISTORICOS',max_length=100,blank=True,null=True)
    COD_ESTADO_CONEXION=models.CharField('COD_ESTADO_CONEXION',max_length=100,blank=True,null=True)
    NRO_LECTURISTA_AUDITORIA=models.IntegerField('NRO_LECTURISTA_AUDITORIA',blank=True,null=True)
    COD_UNICOM_LECT_AUDIT=models.CharField('COD_UNICOM_LECT_AUDIT',max_length=100,blank=True,null=True)
    COD_COLECTOR_AUDITORIA=models.IntegerField('COD_COLECTOR_AUDITORIA',blank=True,null=True)
    COD_UNICOM_COLEC_AUDIT=models.CharField('COD_UNICOM_COLEC_AUDIT',max_length=100,blank=True,null=True)
    FH_LECTURA_AUDIT=models.CharField('FH_LECTURA_AUDIT',max_length=100,blank=True,null=True)
    LECTURA_ACTUAL_AUDIT=models.DecimalField(max_digits=8,decimal_places=7)
    COD_ANOMALIA_HH_1_AUDIT=models.CharField('COD_ANOMALIA_HH_1_AUDIT',max_length=100,blank=True,null=True)
    NOTAS1_AUDIT=models.CharField('NOTAS1_AUDIT',max_length=100,blank=True,null=True)
    GPS_LATITUD=models.CharField('GPS_LATITUD',max_length=100,blank=True,null=True)
    GPS_LONGITUD=models.CharField('GPS_LONGITUD',max_length=100,blank=True,null=True)
    PORCION_ORIGINAL=models.CharField('PORCION_ORIGINAL',max_length=100,blank=True,null=True)
    SEC_ORIGINAL=models.IntegerField('SEC_ORIGINAL',blank=True,null=True)
    UNIDAD_ORIGINAL=models.CharField('UNIDAD_ORIGINAL',max_length=100,blank=True,null=True)
    CODPOST=models.CharField('CODPOST',max_length=100,blank=True,null=True)
    DCSM=models.CharField('DCSM',max_length=100,blank=True,null=True)
    DISTRITO=models.CharField('DISTRITO',max_length=100,blank=True,null=True)
    CIRC=models.CharField('CIRC',max_length=100,blank=True,null=True)
    SECCION=models.CharField('SECCION',max_length=100,blank=True,null=True)
    MANZANA=models.CharField('MANZANA',max_length=100,blank=True,null=True)
    ORDENADO_POR=models.CharField('ORDENADO_POR',max_length=100,blank=True,null=True)
    SEC_RELACIONADA=models.IntegerField('SEC_RELACIONADA',blank=True,null=True)
    LAT=models.FloatField('LAT',blank=True,null=True)
    LON=models.FloatField('LON',blank=True,null=True)


class suministros_gu(models.Model):
    class Meta:
        verbose_name="suministros_gu"
        verbose_name_plural="suministros_gu"


    COD_UNICOM=models.CharField('COD_UNICOM',max_length=100,blank=True,null=True)
    RUTA=models.CharField('RUTA',max_length=100,blank=True,null=True)
    ITINERARIO=models.CharField('ITINERARIO',max_length=100,blank=True,null=True)
    CICLO=models.CharField('CICLO',max_length=100,blank=True,null=True)
    ANIO=models.CharField('ANIO',max_length=100,blank=True,null=True)
    SEG_REG=models.CharField('SEG_REG',max_length=100,blank=True,null=True)
    DIVISION=models.CharField('DIVISION',max_length=100,blank=True,null=True)
    SECUENCIA=models.IntegerField('SECUENCIA',blank=True,null=True)
    LOCALIDAD=models.CharField('LOCALIDAD',max_length=100,blank=True,null=True)
    NOMBRE_CLIENTE=models.CharField('NOMBRE_CLIENTE',max_length=100,blank=True,null=True)
    DIRECCION=models.CharField('DIRECCION',max_length=100,blank=True,null=True)
    NRO_PUERTA=models.DecimalField(max_digits=8, decimal_places=7)
    PISO=models.CharField('PISO',max_length=100,blank=True,null=True)
    DUPLICADOR=models.CharField('DUPLICADOR',max_length=100,blank=True,null=True)
    NRO_APARTO=models.CharField('NRO_APARTO',max_length=100,blank=True,null=True)
    COD_MARCA=models.CharField('COD_MARCA',max_length=100,blank=True,null=True)
    RUEDAS=models.SmallIntegerField('RUEDAS',blank=True,null=True)
    MULTIPLICADOR=models.SmallIntegerField('MULTIPLICADOR',blank=True,null=True)
    LECTURA_ANTERIOR=models.DecimalField(max_digits=8,decimal_places=7)
    LECTURA_MINIMA=models.DecimalField(max_digits=8,decimal_places=7)
    LECTURA_MAXIMA=models.DecimalField(max_digits=8,decimal_places=7)
    DESC_CONSUMO=models.CharField('DESC_CONSUMO',max_length=100,blank=True,null=True)
    ACCESO_FINCA=models.CharField('ACCESO_FINCA',max_length=100,blank=True,null=True)
    ACCESO_PM=models.CharField('ACCESO_PM',max_length=100,blank=True,null=True)
    ESTADO_LECT=models.CharField('ESTADO_LECT',max_length=100,blank=True,null=True)
    ESTADO_SUM=models.CharField('ESTADO_SUM',max_length=100,blank=True,null=True)
    ESTADO_ACT=models.CharField('ESTADO_ACT',max_length=100,blank=True,null=True)
    COD_TARIFA=models.CharField('COD_TARIFA',max_length=100,blank=True,null=True)
    LECTURA_ACTUAL=models.DecimalField(max_digits=8,decimal_places=7)
    TIP_CONSUMO=models.CharField('TIP_CONSUMO',max_length=100,blank=True,null=True)
    FH_LECTURA=models.CharField('FH_LECTURA',max_length=100,blank=True,null=True)
    CONSUMO=models.DecimalField(max_digits=8,decimal_places=7)
    CANT_LECT_FORZADA=models.IntegerField('CANT_LECT_FORZADA',blank=True,null=True)
    NRO_LECTURISTA=models.IntegerField('NRO_LECTURISTA',blank=True,null=True)
    COD_COLECTOR=models.CharField('COD_COLECTOR',max_length=100,blank=True,null=True)
    COD_ANOMALIA_HH_1=models.CharField('COD_ANOMALIA_HH_1',max_length=100,blank=True,null=True)
    NOTAS1=models.CharField('NOTAS1',max_length=100,blank=True,null=True)
    COD_ANOMALIA_HH_2=models.CharField('COD_ANOMALIA_HH_2',max_length=100,blank=True,null=True)
    NOTAS2=models.CharField('NOTAS2',max_length=100,blank=True,null=True)
    COD_ANOMALIA_HH_3=models.CharField('COD_ANOMALIA_HH_3',max_length=100,blank=True,null=True)
    NOTAS3=models.CharField('NOTAS3',max_length=100,blank=True,null=True)
    SECUENCIA_REAL=models.IntegerField('SECUENCIA_REAL',blank=True,null=True)
    NRO_CLIENTE=models.CharField('NRO_CLIENTE',max_length=100,blank=True,null=True)
    COMPLEMENTO=models.CharField('COMPLEMENTO',max_length=100,blank=True,null=True)
    CONSUMO_ESTIMADO=models.DecimalField(max_digits=8,decimal_places=7)
    COD_ANOMALIA1=models.CharField('COD_ANOMALIA1',max_length=100,blank=True,null=True)
    LECTURA1=models.IntegerField()
    CONSUMO1=models.IntegerField()
    FECHA_LECTURA1=models.CharField('FECHA_LECTURA1',max_length=100,blank=True,null=True)
    COD_ANOMALIA2=models.CharField('COD_ANOMALIA2',max_length=100,blank=True,null=True)
    LECTURA2=models.IntegerField()
    CONSUMO2=models.IntegerField()
    FECHA_LECTURA2=models.CharField('FECHA_LECTURA2',max_length=100,blank=True,null=True)
    COD_ANOMALIA3=models.CharField('COD_ANOMALIA3',max_length=100,blank=True,null=True)
    LECTURA3=models.IntegerField()
    CONSUMO3=models.IntegerField()
    FECHA_LECTURA3=models.CharField('FECHA_LECTURA3',max_length=100,blank=True,null=True)
    COD_ANOMALIA4=models.CharField('COD_ANOMALIA4',max_length=100,blank=True,null=True)
    LECTURA4=models.IntegerField()
    CONSUMO4=models.IntegerField()
    FECHA_LECTURA4=models.CharField('FECHA_LECTURA4',max_length=100,blank=True,null=True)
    COD_ANOMALIA5=models.CharField('COD_ANOMALIA5',max_length=100,blank=True,null=True)
    LECTURA5=models.IntegerField()
    CONSUMO5=models.IntegerField()
    FECHA_LECTURA5=models.CharField('FECHA_LECTURA5',max_length=100,blank=True,null=True)
    COD_ANOMALIA6=models.CharField('COD_ANOMALIA6',max_length=100,blank=True,null=True)
    LECTURA6=models.IntegerField()
    CONSUMO6=models.IntegerField()
    FECHA_LECTURA6=models.CharField('FECHA_LECTURA6',max_length=100,blank=True,null=True)
    COD_RECAMBIO=models.CharField('COD_RECAMBIO',max_length=100,blank=True,null=True)
    LEC_MEDIDOR_RETIRADO=models.DecimalField(max_digits=8,decimal_places=7)
    CONSUMO_ULTIMO_RECAMBIO=models.DecimalField(max_digits=8,decimal_places=7)
    FECHA_RECAMBIO=models.CharField('FECHA_RECAMBIO',max_length=100,blank=True,null=True)
    ACUM_CONS_VARIOS_RECAMBIOS=models.DecimalField(max_digits=8,decimal_places=7)
    ANIO_INSTALACION=models.DecimalField(max_digits=10,decimal_places=7)
    COD_TIPO_CONEXION=models.CharField('COD_TIPO_CONEXION',max_length=100,blank=True,null=True)
    TIPO_MEDIDOR=models.CharField('TIPO_MEDIDOR',max_length=100,blank=True,null=True)
    COD_DIAMETRO=models.CharField('COD_DIAMETRO',max_length=100,blank=True,null=True)
    CONSULTO_HISTORICOS=models.CharField('CONSULTO_HISTORICOS',max_length=100,blank=True,null=True)
    COD_ESTADO_CONEXION=models.CharField('COD_ESTADO_CONEXION',max_length=100,blank=True,null=True)
    NRO_LECTURISTA_AUDITORIA=models.IntegerField('NRO_LECTURISTA_AUDITORIA',blank=True,null=True)
    COD_UNICOM_LECT_AUDIT=models.CharField('COD_UNICOM_LECT_AUDIT',max_length=100,blank=True,null=True)
    COD_COLECTOR_AUDITORIA=models.IntegerField('COD_COLECTOR_AUDITORIA',blank=True,null=True)
    COD_UNICOM_COLEC_AUDIT=models.CharField('COD_UNICOM_COLEC_AUDIT',max_length=100,blank=True,null=True)
    FH_LECTURA_AUDIT=models.CharField('FH_LECTURA_AUDIT',max_length=100,blank=True,null=True)
    LECTURA_ACTUAL_AUDIT=models.DecimalField(max_digits=8,decimal_places=7)
    COD_ANOMALIA_HH_1_AUDIT=models.CharField('COD_ANOMALIA_HH_1_AUDIT',max_length=100,blank=True,null=True)
    NOTAS1_AUDIT=models.CharField('NOTAS1_AUDIT',max_length=100,blank=True,null=True)
    GPS_LATITUD=models.CharField('GPS_LATITUD',max_length=100,blank=True,null=True)
    GPS_LONGITUD=models.CharField('GPS_LONGITUD',max_length=100,blank=True,null=True)
    PORCION_ORIGINAL=models.CharField('PORCION_ORIGINAL',max_length=100,blank=True,null=True)
    SEC_ORIGINAL=models.IntegerField('SEC_ORIGINAL',blank=True,null=True)
    UNIDAD_ORIGINAL=models.CharField('UNIDAD_ORIGINAL',max_length=100,blank=True,null=True)
    CODPOST=models.CharField('CODPOST',max_length=100,blank=True,null=True)
    DCSM=models.CharField('DCSM',max_length=100,blank=True,null=True)
    DISTRITO=models.CharField('DISTRITO',max_length=100,blank=True,null=True)
    CIRC=models.CharField('CIRC',max_length=100,blank=True,null=True)
    SECCION=models.CharField('SECCION',max_length=100,blank=True,null=True)
    MANZANA=models.CharField('MANZANA',max_length=100,blank=True,null=True)
    ORDENADO_POR=models.CharField('ORDENADO_POR',max_length=100,blank=True,null=True)
    SEC_RELACIONADA=models.IntegerField('SEC_RELACIONADA',blank=True,null=True)
    LAT=models.FloatField('LAT',blank=True,null=True)
    LON=models.FloatField('LON',blank=True,null=True)

class suministros_res(models.Model):
    class Meta:
        verbose_name="suministros_res"
        verbose_name_plural="suministros_res"


    COD_UNICOM=models.CharField('COD_UNICOM',max_length=100,blank=True,null=True)
    RUTA=models.CharField('RUTA',max_length=100,blank=True,null=True)
    ITINERARIO=models.CharField('ITINERARIO',max_length=100,blank=True,null=True)
    CICLO=models.CharField('CICLO',max_length=100,blank=True,null=True)
    ANIO=models.CharField('ANIO',max_length=100,blank=True,null=True)
    SEG_REG=models.CharField('SEG_REG',max_length=100,blank=True,null=True)
    DIVISION=models.CharField('DIVISION',max_length=100,blank=True,null=True)
    SECUENCIA=models.IntegerField('SECUENCIA',blank=True,null=True)
    LOCALIDAD=models.CharField('LOCALIDAD',max_length=100,blank=True,null=True)
    NOMBRE_CLIENTE=models.CharField('NOMBRE_CLIENTE',max_length=100,blank=True,null=True)
    DIRECCION=models.CharField('DIRECCION',max_length=100,blank=True,null=True)
    NRO_PUERTA=models.DecimalField(max_digits=8, decimal_places=7)
    PISO=models.CharField('PISO',max_length=100,blank=True,null=True)
    DUPLICADOR=models.CharField('DUPLICADOR',max_length=100,blank=True,null=True)
    NRO_APARTO=models.CharField('NRO_APARTO',max_length=100,blank=True,null=True)
    COD_MARCA=models.CharField('COD_MARCA',max_length=100,blank=True,null=True)
    RUEDAS=models.SmallIntegerField('RUEDAS',blank=True,null=True)
    MULTIPLICADOR=models.SmallIntegerField('MULTIPLICADOR',blank=True,null=True)
    LECTURA_ANTERIOR=models.DecimalField(max_digits=8,decimal_places=7)
    LECTURA_MINIMA=models.DecimalField(max_digits=8,decimal_places=7)
    LECTURA_MAXIMA=models.DecimalField(max_digits=8,decimal_places=7)
    DESC_CONSUMO=models.CharField('DESC_CONSUMO',max_length=100,blank=True,null=True)
    ACCESO_FINCA=models.CharField('ACCESO_FINCA',max_length=100,blank=True,null=True)
    ACCESO_PM=models.CharField('ACCESO_PM',max_length=100,blank=True,null=True)
    ESTADO_LECT=models.CharField('ESTADO_LECT',max_length=100,blank=True,null=True)
    ESTADO_SUM=models.CharField('ESTADO_SUM',max_length=100,blank=True,null=True)
    ESTADO_ACT=models.CharField('ESTADO_ACT',max_length=100,blank=True,null=True)
    COD_TARIFA=models.CharField('COD_TARIFA',max_length=100,blank=True,null=True)
    LECTURA_ACTUAL=models.DecimalField(max_digits=8,decimal_places=7)
    TIP_CONSUMO=models.CharField('TIP_CONSUMO',max_length=100,blank=True,null=True)
    FH_LECTURA=models.CharField('FH_LECTURA',max_length=100,blank=True,null=True)
    CONSUMO=models.DecimalField(max_digits=8,decimal_places=7)
    CANT_LECT_FORZADA=models.IntegerField('CANT_LECT_FORZADA',blank=True,null=True)
    NRO_LECTURISTA=models.IntegerField('NRO_LECTURISTA',blank=True,null=True)
    COD_COLECTOR=models.CharField('COD_COLECTOR',max_length=100,blank=True,null=True)
    COD_ANOMALIA_HH_1=models.CharField('COD_ANOMALIA_HH_1',max_length=100,blank=True,null=True)
    NOTAS1=models.CharField('NOTAS1',max_length=100,blank=True,null=True)
    COD_ANOMALIA_HH_2=models.CharField('COD_ANOMALIA_HH_2',max_length=100,blank=True,null=True)
    NOTAS2=models.CharField('NOTAS2',max_length=100,blank=True,null=True)
    COD_ANOMALIA_HH_3=models.CharField('COD_ANOMALIA_HH_3',max_length=100,blank=True,null=True)
    NOTAS3=models.CharField('NOTAS3',max_length=100,blank=True,null=True)
    SECUENCIA_REAL=models.IntegerField('SECUENCIA_REAL',blank=True,null=True)
    NRO_CLIENTE=models.CharField('NRO_CLIENTE',max_length=100,blank=True,null=True)
    COMPLEMENTO=models.CharField('COMPLEMENTO',max_length=100,blank=True,null=True)
    CONSUMO_ESTIMADO=models.DecimalField(max_digits=8,decimal_places=7)
    COD_ANOMALIA1=models.CharField('COD_ANOMALIA1',max_length=100,blank=True,null=True)
    LECTURA1=models.IntegerField()
    CONSUMO1=models.IntegerField()
    FECHA_LECTURA1=models.CharField('FECHA_LECTURA1',max_length=100,blank=True,null=True)
    COD_ANOMALIA2=models.CharField('COD_ANOMALIA2',max_length=100,blank=True,null=True)
    LECTURA2=models.IntegerField()
    CONSUMO2=models.IntegerField()
    FECHA_LECTURA2=models.CharField('FECHA_LECTURA2',max_length=100,blank=True,null=True)
    COD_ANOMALIA3=models.CharField('COD_ANOMALIA3',max_length=100,blank=True,null=True)
    LECTURA3=models.IntegerField()
    CONSUMO3=models.IntegerField()
    FECHA_LECTURA3=models.CharField('FECHA_LECTURA3',max_length=100,blank=True,null=True)
    COD_ANOMALIA4=models.CharField('COD_ANOMALIA4',max_length=100,blank=True,null=True)
    LECTURA4=models.IntegerField()
    CONSUMO4=models.IntegerField()
    FECHA_LECTURA4=models.CharField('FECHA_LECTURA4',max_length=100,blank=True,null=True)
    COD_ANOMALIA5=models.CharField('COD_ANOMALIA5',max_length=100,blank=True,null=True)
    LECTURA5=models.IntegerField()
    CONSUMO5=models.IntegerField()
    FECHA_LECTURA5=models.CharField('FECHA_LECTURA5',max_length=100,blank=True,null=True)
    COD_ANOMALIA6=models.CharField('COD_ANOMALIA6',max_length=100,blank=True,null=True)
    LECTURA6=models.IntegerField()
    CONSUMO6=models.IntegerField()
    FECHA_LECTURA6=models.CharField('FECHA_LECTURA6',max_length=100,blank=True,null=True)
    COD_RECAMBIO=models.CharField('COD_RECAMBIO',max_length=100,blank=True,null=True)
    LEC_MEDIDOR_RETIRADO=models.DecimalField(max_digits=8,decimal_places=7)
    CONSUMO_ULTIMO_RECAMBIO=models.DecimalField(max_digits=8,decimal_places=7)
    FECHA_RECAMBIO=models.CharField('FECHA_RECAMBIO',max_length=100,blank=True,null=True)
    ACUM_CONS_VARIOS_RECAMBIOS=models.DecimalField(max_digits=8,decimal_places=7)
    ANIO_INSTALACION=models.DecimalField(max_digits=10,decimal_places=7)
    COD_TIPO_CONEXION=models.CharField('COD_TIPO_CONEXION',max_length=100,blank=True,null=True)
    TIPO_MEDIDOR=models.CharField('TIPO_MEDIDOR',max_length=100,blank=True,null=True)
    COD_DIAMETRO=models.CharField('COD_DIAMETRO',max_length=100,blank=True,null=True)
    CONSULTO_HISTORICOS=models.CharField('CONSULTO_HISTORICOS',max_length=100,blank=True,null=True)
    COD_ESTADO_CONEXION=models.CharField('COD_ESTADO_CONEXION',max_length=100,blank=True,null=True)
    NRO_LECTURISTA_AUDITORIA=models.IntegerField('NRO_LECTURISTA_AUDITORIA',blank=True,null=True)
    COD_UNICOM_LECT_AUDIT=models.CharField('COD_UNICOM_LECT_AUDIT',max_length=100,blank=True,null=True)
    COD_COLECTOR_AUDITORIA=models.IntegerField('COD_COLECTOR_AUDITORIA',blank=True,null=True)
    COD_UNICOM_COLEC_AUDIT=models.CharField('COD_UNICOM_COLEC_AUDIT',max_length=100,blank=True,null=True)
    FH_LECTURA_AUDIT=models.CharField('FH_LECTURA_AUDIT',max_length=100,blank=True,null=True)
    LECTURA_ACTUAL_AUDIT=models.DecimalField(max_digits=8,decimal_places=7)
    COD_ANOMALIA_HH_1_AUDIT=models.CharField('COD_ANOMALIA_HH_1_AUDIT',max_length=100,blank=True,null=True)
    NOTAS1_AUDIT=models.CharField('NOTAS1_AUDIT',max_length=100,blank=True,null=True)
    GPS_LATITUD=models.CharField('GPS_LATITUD',max_length=100,blank=True,null=True)
    GPS_LONGITUD=models.CharField('GPS_LONGITUD',max_length=100,blank=True,null=True)
    PORCION_ORIGINAL=models.CharField('PORCION_ORIGINAL',max_length=100,blank=True,null=True)
    SEC_ORIGINAL=models.IntegerField('SEC_ORIGINAL',blank=True,null=True)
    UNIDAD_ORIGINAL=models.CharField('UNIDAD_ORIGINAL',max_length=100,blank=True,null=True)
    CODPOST=models.CharField('CODPOST',max_length=100,blank=True,null=True)
    DCSM=models.CharField('DCSM',max_length=100,blank=True,null=True)
    DISTRITO=models.CharField('DISTRITO',max_length=100,blank=True,null=True)
    CIRC=models.CharField('CIRC',max_length=100,blank=True,null=True)
    SECCION=models.CharField('SECCION',max_length=100,blank=True,null=True)
    MANZANA=models.CharField('MANZANA',max_length=100,blank=True,null=True)
    ORDENADO_POR=models.CharField('ORDENADO_POR',max_length=100,blank=True,null=True)
    SEC_RELACIONADA=models.IntegerField('SEC_RELACIONADA',blank=True,null=True)
    LAT=models.FloatField('LAT',blank=True,null=True)
    LON=models.FloatField('LON',blank=True,null=True)

class log_rutas(models.Model):
    class Meta:
        verbose_name="logruta"
        verbose_name_plural="logrutas"

    ruta=models.ForeignKey(Ruta,on_delete=models.PROTECT)
    estado=models.CharField('Estado',max_length=100,blank=True,null=True)
    fecha_log=models.DateTimeField(blank=True,null=True)
    usuario=models.ForeignKey(EmserUser ,blank=True, null=True)
    observacion=models.CharField('Observacion',max_length=100,blank=True,null=True)


class Resguardo_Terreno(models.Model):

    class Meta:
        verbose_name = "resguardo_terreno"
        verbose_name_plural = "resguardos_terreno"

    fecha_generacion = models.DateTimeField(blank=True,null=True)
    orden_trabajo = models.ForeignKey(OrdenDeTrabajo,on_delete=models.PROTECT)
    punto_suministro = models.ForeignKey(PuntoDeSuministro,on_delete=models.PROTECT)
    cliente = models.ForeignKey(Cliente,on_delete=models.PROTECT)
    cuenta_contrato = models.CharField(max_length=30, blank=True, null=True)
    tecnico = models.ForeignKey(Tecnico,on_delete=models.PROTECT)
    nombre_apellido = models.CharField(max_length=250, blank=True, null=True)
    cod_ruta = models.ForeignKey(Ruta,on_delete=models.PROTECT)
    numero_ruta = models.CharField(max_length=30, blank=True, null=True)
    itinerario = models.CharField(max_length=15, blank=True, null=True)
    ciclo = models.CharField(max_length=10, blank=True, null=True)
    tipo_orden = models.CharField(max_length=30, blank=True, null=True)
    clase_actividad = models.CharField(max_length=20, blank=True, null=True)
    fh_inicio = models.DateTimeField(blank=True, null=True)
    fh_fin = models.DateTimeField(blank=True, null=True)
    lectura = models.IntegerField(blank=True, null=True)
    lectura_anterior = models.IntegerField(blank=True, null=True)
    consumo = models.IntegerField(blank=True, null=True)
    cargado = models.NullBooleanField()
    descargado = models.NullBooleanField()
    fecha_descarga = models.DateTimeField(blank=True, null=True)
    fecha_asignacion = models.DateTimeField(blank=True, null=True)
    fecha_carga = models.CharField(max_length=20, blank=True, null=True)
    oficina = models.ForeignKey(WorkUnit,on_delete=models.PROTECT)
    usuario_asignacion = models.ForeignKey(EmserUser,on_delete=models.PROTECT)
    estado = models.SmallIntegerField(default=1)
    alias_dispositivo = models.CharField(max_length=20, blank=True, null=True)
    tiene_auditoria = models.NullBooleanField()


class ExtensionDatos(models.Model):
    class Meta:
        verbose_name = "extension_dato"
        verbose_name_plural = "extension_datos"
        index_together = ['tabla_extension', 'campo_extension', 'clave_registro']

    def _str_(self):
        pass

    tabla_extension = models.CharField('Tabla extensión', max_length=50, blank=False, null=False)
    campo_extension = models.CharField('Campo extensión', max_length=50, blank=False, null=False)
    clave_registro = models.CharField('Clave registro', max_length=50, blank=False, null=False, db_index=True)
    valor = models.CharField('Valor', max_length=500, blank=True, null=True)
    etiqueta_campo_extension = models.CharField('Etiqueta campo extensión', max_length=50, blank=True, null=True)


class reubicacion_suministro(models.Model):
    class Meta:
        verbose_name="reubicacion_suministro"
        verbose_name_plural="reubicacion_suministros"

    oficina=models.ForeignKey(WorkUnit,on_delete=models.PROTECT,blank=True,null=True)
    ruta=models.CharField('ruta',max_length=100,blank=True,null=True)
    itinerario=models.CharField('itinerario',max_length=100,blank=True,null=True)
    punto_suministro=models.CharField('punto_suministro',max_length=100,blank=True,null=True)
    secuencia_teorica=models.IntegerField('secuencia_teorica',blank=True,null=True)
    direccion=models.CharField('direccion',max_length=100,blank=True,null=True)
    numero_puerta=models.IntegerField('numero_puerta',blank=True,null=True)
    porcion_original=models.CharField('porcion_original',max_length=100,blank=True,null=True)
    sec_original=models.IntegerField('sec_original',blank=True,null=True)
    unidad_original=models.CharField('unidad_original',max_length=100,blank=True,null=True)


class importacion_historico(models.Model):
    class Meta:
        verbose_name="importacion_historico"
        verbose_name_plural="importacion historicos"

    orden_trabajo=models.ForeignKey(OrdenDeTrabajo, on_delete=models.PROTECT,db_index=True)
    cod_anomalia1=models.CharField('COD_ANOMALIA1',max_length=100,blank=True,null=True)
    lectura1=models.IntegerField()
    consumo1=models.IntegerField()
    fecha_lectura1=models.CharField('fecha_lectura1',max_length=100,blank=True,null=True)
    cod_anomalia2=models.CharField('COD_ANOMALIA2',max_length=100,blank=True,null=True)
    lectura2=models.IntegerField()
    consumo2=models.IntegerField()
    fecha_lectura2=models.CharField('fecha_lectura2',max_length=100,blank=True,null=True)
    cod_anomalia3=models.CharField('COD_ANOMALIA3',max_length=100,blank=True,null=True)
    lectura3=models.IntegerField()
    consumo3=models.IntegerField()
    fecha_lectura3=models.CharField('fecha_lectura3',max_length=100,blank=True,null=True)
    cod_anomalia4=models.CharField('COD_ANOMALIA4',max_length=100,blank=True,null=True)
    lectura4=models.IntegerField()
    consumo4=models.IntegerField()
    fecha_lectura4=models.CharField('fecha_lectura4',max_length=100,blank=True,null=True)
    cod_anomalia5=models.CharField('COD_ANOMALIA5',max_length=100,blank=True,null=True)
    lectura5=models.IntegerField()
    consumo5=models.IntegerField()
    fecha_lectura5=models.CharField('fecha_lectura5',max_length=100,blank=True,null=True)
    cod_anomalia6=models.CharField('COD_ANOMALIA6',max_length=100,blank=True,null=True)
    lectura6=models.IntegerField()
    consumo6=models.IntegerField()
    fecha_lectura6=models.CharField('fecha_lectura6',max_length=100,blank=True,null=True)


class Mensajes_Dispositivos(models.Model):
    
    class Meta:
        verbose_name = "Mensaje Dispositivo"
        verbose_name_plural = "Mensajes Dispositivos"


    id_mensaje = models.CharField(max_length=150)
    alias_dispositivo = models.CharField(max_length=100, blank=True, null=True)
    fecha_hora_comando = models.DateTimeField('fecha_hora_comando',db_column='fecha_hora_comando',  blank=True, null=True)  
    fecha_hora_respuesta = models.DateTimeField('fecha_hora_respuesta',db_column='fecha_hora_respuesta',   blank=True, null=True)  
    tipo_mensaje = models.CharField(max_length=100, blank=True, null=True)
    usuario_comando = models.CharField(max_length=100, blank=True, null=True)
    comando_enviado = models.CharField(max_length=250, blank=True, null=True)
    respuesta = models.TextField( blank=True, null=True)


    

