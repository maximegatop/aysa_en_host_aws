import sqlite3
import os
from zipfile import ZipFile
import base64
import codecs
from api.TablasBD import *
from qorder.models import * 
from contextlib import closing
from core.models import *





class BaseDeDatos(object):

	"""docstring for ClassName"""
	def __init__(self):
		self._ruta=''
		self._ruta1=''		
		self.rutadef=''
		self._sLogName=''
		self.cursor=''
		self.archivo=''
		self.Conexion=''
		self.sql=''
		self.vector=[]
		
		

	def setpath(self,path1):	
		os.chdir(path1)					
		self._ruta=path1		
		print('_ruta {}'.format(self._ruta))

	
	def NewFileOnlineData(self,NumSerie):			#Creacion db3 y directorio de la ruta
		self.rutadef=self._ruta
		print(self.rutadef)

		if not os.path.exists(self.rutadef): 
			os.makedirs(self.rutadef)
		self.archivo=self.rutadef + '/'+ self.FileNameOnlineData()
		print(self.archivo)
		if os.path.exists(self.archivo):
			os.remove(self.archivo)
		self.Conexion=sqlite3.connect( self.rutadef + '/'+ self.FileNameOnlineData())
		print('llego')
		


		self.cursor=self.Conexion.cursor()
		self.cursor.executescript(CargaBD())		
		self.SaveBD(self.CargaUsuario(NumSerie))
		self.SaveBD(self.CargaOrdenes(NumSerie))
		self.SaveBD(self.CargarCodigo())
		self.SaveBD(self.CargarAnomailia())
		self.SaveBD(self.CargaObservacionesXanomalia())
		self.SaveBD(self.CargaRutas())
		self.SaveBD(self.CargaAparatosConsumo(NumSerie))
		self.SaveBD(self.Cargadatossum(NumSerie))
		self.SaveBD(self.CargaAparatosSuministro(NumSerie))
		self.SaveBD(self.CargaConfiguraciones())



		self.Conexion.close()
		self.ComprimirOnlineData()
		self.code64OnlineData()




	def NewFileNewAssignment(self,NumSerie):			#Creacion db3 y directorio de la ruta
		self.rutadef=self._ruta
		print(self.rutadef)
		if not os.path.exists(self.rutadef): 
			os.makedirs(self.rutadef)

		self.archivo=self.rutadef + '/'+ self.FileNameNewAssignment()
		print(self.archivo)
		if os.path.exists(self.archivo):
			os.remove(self.archivo)
		self.Conexion=sqlite3.connect( self.rutadef + '/'+ self.FileNameNewAssignment())
		print('llego1')



		self.cursor=self.Conexion.cursor()
		self.cursor.executescript(CargaBD())		
		self.SaveBD(self.CargaOrdenes(NumSerie))
		self.SaveBD(self.CargaAparatosConsumo(NumSerie))
		self.SaveBD(self.Cargadatossum(NumSerie))
		self.SaveBD(self.CargaAparatosSuministro(NumSerie))



		self.Conexion.close()
		self.ComprimirNewAssignment()
		self.code64NewAssignment()





	def SaveBD(self,vector):
		try:	

			for o in self.vector:

				self.cursor=self.Conexion.cursor()
				self.cursor.executescript(o)
				self.vector=[]
		except Exception as e:
			print(e)
	


	def FileNameOnlineData(self):
		_sLogName= 'db' + ".db3"
		print(_sLogName)
		print('entroname')
		return _sLogName



	def FileNameNewAssignment(self):
		_sLogName= 'QorderDB' + ".db3"
		print(_sLogName)
		print('entroname')
		return _sLogName



	def ComprimirNewAssignment(self):

		myzip = ZipFile('Ordendb.zip', 'w')
		print(myzip)
		print('llegacomp')
		myzip.write('QorderDB.db3')
		print('Comprimir')
		myzip.close()



	def ComprimirOnlineData(self):

		myzip = ZipFile('db3.zip', 'w')
		print(myzip)
		print('llegacomp1')
		myzip.write('db.db3')
		print('Comprimir1')
		myzip.close()



	def code64OnlineData(self):										#Archivo BD con codificacion 	Base 64

		encoded=''
		pathcode='db3.zip'
		print(pathcode)
		with open (pathcode, 'rb') as f:
			print('aca')
			encoded=base64.b64encode(f.read())


		return encoded

	def code64NewAssignment(self):										#Archivo BD con codificacion 	Base 64

		encoded=''
		pathcode='Ordendb.zip'
		print(pathcode)
		with open (pathcode, 'rb') as f:
			print('aca')
			encoded=base64.b64encode(f.read())


		return encoded

	
	def CargaUsuario(self,NumSerie):

		_tp=TerminalPortatil.objects.get(numero_serie=NumSerie)
		_tecnico=Tecnico.objects.get(terminal_portatil=_tp)
		print('paso')

		self.sql="""INSERT INTO USUARIO(NOMBRE_USUARIO,PASSWORD,ACTUALIZAR_PASSWORD,ENVIAR_NUEVO_PASSWORD) VALUES ('{}','{}','{}','{}')""".format(_tecnico.nombre_1,_tecnico.password,_tecnico.flag_reset_password,0)
		self.vector.append(self.sql)
		print(self.vector)
		return self.vector

	
	def CargaOrdenes(self,NumSerie):

		_tp=TerminalPortatil.objects.get(numero_serie=NumSerie)

		_tecnico=Tecnico.objects.get(terminal_portatil=_tp)

		_ruta=Ruta.objects.filter(tecnico=_tecnico)
		for ruta in _ruta:
			print(ruta)
			_orden=OrdenDeTrabajo.objects.filter(tecnico=_tecnico,estado=3,flag_asignacion_guardada=1)
			print(_orden)
			for o in _orden:

				_ptosum=PuntoDeSuministro.objects.get(punto_suministro=o.punto_suministro_id)

				_cto=TipoOrden(tipo_orden=o.tipo_orden_id)
				print('paso1')


				self.sql="""INSERT INTO ORDENES(num_os,tip_os,f_gen, f_estm_rest,co_prior_ord,nis_rad, nic, sec_nis, cod_emp_asig,coment_os,direccion, rutaitin, estado,enviado,ord_disponible,secuencia,ciclo,ruta,itinerario,acceso_suministro, DESC_TIPO_ORDEN)VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')""".format(o.numero_orden,_cto.tipo_orden,ruta.fecha_generacion,ruta.fecha_estimada_resolucion,o.prioridad,_ptosum.punto_suministro,_ptosum.num_contrato,o.secuencial_registro,o.tecnico,'','','','0','0','99',o.secuencial_registro,'',ruta.idruta,'',_ptosum.ref_suministro,_cto.descripcion)
				self.vector.append(self.sql)					

				print(self.vector)

		return self.vector
	
	def CargarCodigo(self):
		print('aca')

		_codigo=Codigo.objects.all()
		for cod in _codigo:


			self.sql="""INSERT INTO CODIGOS(cod, desc_cod)VALUES('{}','{}')""".format(cod.codigo,cod.descripcion)
			self.vector.append(self.sql)
			print(self.sql)

		return self.vector

	def CargarAnomailia(self):

		_anomalia=Anomalia.objects.all()

		for anomalia in _anomalia:


			self.sql="""INSERT INTO anomalias (codigo,codigo_corto, descripcion, prioridad,tipo_anom_lect)VALUES('{}','{}','{}','{}','{}')""".format(anomalia.id_anomalia,anomalia.id_anomalia,anomalia.descripcion,anomalia.prioridad,anomalia.tipo_resultado)
			print(self.sql)
			self.vector.append(self.sql)

		return self.vector


	def CargaObservacionesXanomalia(self):

		_observacionxanomailia=ObservacionXAnomalia.objects.all()

		for oxanomalia in _observacionxanomailia:


			self.sql="""INSERT INTO ObservacionesXanomalia (anomalia,observacion)VALUES('{}','{}')""".format(oxanomalia.anomalia,oxanomalia.codigo)
			self.vector.append(self.sql)
			print(self.sql)
		return self.vector

	def CargaRutas(self):
		_rutas=Ruta.objects.all()

		for rutas in _rutas:

			self.sql="""INSERT INTO RUTAS (ID,CICLO,RUTA,ITINERARIO,PLAN,ANIO,CANT_total,FECHA_GENERACION,FECHA_ESTIMADA_RESOLUCION,OFICINA)VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')""".format(rutas.idruta,rutas.ciclo,rutas.ruta,rutas.itinerario,rutas.plan,rutas.anio,rutas.cantidad,rutas.fecha_generacion,rutas.fecha_estimada_resolucion,rutas.oficina)
			self.vector.append(self.sql)
			print(self.vector)

		return self.vector


	def Cargadatossum(self,NumSerie):
		_tp=TerminalPortatil.objects.get(numero_serie=NumSerie)

		_tecnico=Tecnico.objects.get(terminal_portatil=_tp)

		_orden=OrdenDeTrabajo.objects.filter(tecnico=_tecnico,estado=3,flag_asignacion_guardada=1)

		for o in _orden:

			_ptosum=PuntoDeSuministro.objects.get(punto_suministro=o.punto_suministro_id)
			print('valor psum {}'.format(_ptosum))

			self.sql="""INSERT INTO DATOSUM(num_os,nis_rad,sec_nis,nic,nif,ruta,num_itin,rutaitin, municipio, localidad, departamento,calle,num_puerta,duplicador,cgv_sum,ref_direccion,acceso_direccion,acceso_suministro,nom_cli,TFNO_CLI,estado_serv,tip_serv)VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')""".format(_ptosum.num_contrato,_ptosum.punto_suministro,o.secuencial_registro,_ptosum.cliente.nombre,'',o.ruta_id,'','',_ptosum.municipio,_ptosum.localidad,_ptosum.departamento,_ptosum.calle,_ptosum.numero_puerta,_ptosum.duplicador,_ptosum.piso,_ptosum.ref_finca,_ptosum.ref_direccion,_ptosum.ref_suministro,'','','',_ptosum.tipo_servicio_id)
			self.vector.append(self.sql)
			print(self.sql)

		return self.vector

	def CargaAparatosConsumo(self,NumSerie):
		_tp=TerminalPortatil.objects.get(numero_serie=NumSerie)
		
		_tecnico=Tecnico.objects.get(terminal_portatil=_tp)

		_orden=OrdenDeTrabajo.objects.filter(tecnico=_tecnico,estado=3,flag_asignacion_guardada=1)

		for o in _orden:

			_ptosum=PuntoDeSuministro.objects.get(punto_suministro=o.punto_suministro_id)
			
			_apa=Aparato.objects.get(aparato=_ptosum.aparato_id)
			
			_consumo=Consumo.objects.get(aparato=_apa.aparato)

			self.sql="""INSERT INTO APACONEN(num_os,nis_rad,co_marca, marca_medidor,num_apa,num_rue,tip_csmo, csmo_anterior,lect_anterior, fecha_lect_anterior, lect_min, lect_max, constante, DESCRIPCION_CSMO)VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')""".format(o.numero_orden,_ptosum.punto_suministro,_apa.marca_id,_apa.marca.descripcion,_apa.num_serie,_apa.num_ruedas,_consumo.consumo,_consumo.consumo_anterior,_consumo.lectura_anterior,_consumo.fecha_lectura_anterior,_consumo.tope_lectura_minima,_consumo.tope_lectura_maxima,_consumo.constante,_consumo.tipo_consumo.descripcion)
			print(self.sql)
			self.vector.append(self.sql)
		return self.vector

	def CargaAparatosSuministro(self,NumSerie):
		_tp=TerminalPortatil.objects.get(numero_serie=NumSerie)

		_tecnico=Tecnico.objects.get(terminal_portatil=_tp)

		_orden=OrdenDeTrabajo.objects.filter(tecnico=_tecnico,estado=3,flag_asignacion_guardada=1)

		for o in _orden:

			_ptosum=PuntoDeSuministro.objects.get(punto_suministro=o.punto_suministro_id)

			_apa=Aparato.objects.get(aparato=_ptosum.aparato_id)

			self.sql="""INSERT INTO APARATOS(num_os,nis_rad,co_marca,num_apa,tip_apa,est_apa,aol_apa)VALUES('{}','{}','{}','{}','{}','{}','{}')""".format(o.numero_orden,_ptosum.punto_suministro,_apa.marca_id,_apa.num_serie,_apa.tipo_aparato_id,_apa.estado_aparato,'')
			self.vector.append(self.sql)
			print(self.sql)
		return self.vector


	def CargaConfiguraciones(self):
		_parametro=Parametro.objects.filter(parametro_movil=1)

		for param in _parametro:

			self.sql="""INSERT INTO CONFIGURACION(Parametro, valor)VALUES('{}','{}')""".format(param.parametro,param.descripcion)
			self.vector.append(self.sql)
			print(self.sql)

		return self.vector