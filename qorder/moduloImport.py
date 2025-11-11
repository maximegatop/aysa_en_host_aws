from qorder.models import *
from core.models import *
from hashlib import md5
from ftplib import FTP
from qorder.utils import *

import petl as etl
import datetime
import time
import logging
import os
import errno



def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def compararIntegridadArchivo(md5FtpFile,pathlocal,  filename):
	md5file = getMD5FromFile(pathlocal + filename)
	
	print ('md5Ftp: ' + md5FtpFile)
	print ('md5file: ' + md5file)

	if md5file == md5FtpFile:
		return True
	else:
		return False

def getMD5FromFile(filename):
	hasher = md5()
	with open(filename, 'rb') as afile:
		#se lee todo el archivo como bytes
		buf = afile.read()
		hasher.update(buf)
	return hasher.hexdigest()


def getMD5(ftp,filename):
	m = md5()
	ftp.retrbinary('RETR %s' % filename, m.update)
	return m.hexdigest()


	
def getFile(ftp, pathlocal, filename):	

	filenameCopy = pathlocal+filename
	filelocal = open(filenameCopy,'wb')
	ftp.retrbinary('RETR ' + filename, filelocal.write, 1024 )
	filelocal.close()


def placeFile(ftp, filename):	
	ftp.storbinary('STOR ' + filename, open(filename, 'rb'))


def getLoggerFileName(oficina,proceso,usuario):
	logfileName = '{}_{}_{}_{}.txt'.format(oficina,proceso,usuario,datetime.datetime.today().strftime('%Y%m%d_%H%M%S'))
	return logfileName


def generarCabeceraLog(_log):
	_log.info('******************************************')
	_log.info('       Qorder importación - V1.0          ')
	_log.info('Proceso iniciado: {}'.format(datetime.datetime.today().strftime('%d/%m/%Y %H:%M') ) )
	_log.info('******************************************')
	

def getLoggingFileData(filename):
	_file = open( filename, 'r')
	str1 =  _file.read()
	#lines = _file.readlines(
	_file.close()
	
	return str1

def generarPieLog(_log):
	_log.info('******************************************')	
	_log.info('Proceso finalizado: {}'.format(datetime.datetime.today().strftime('%d/%m/%Y %H:%M') ) )
	_log.info('******************************************')

def cerrarLog(_log):
	_handlers = _log.handlers[:]

	for h in _handlers:
		h.close()
		_log.removeHandler(h)


def notificarFinProceso(_slogfinal,_bnotifica_error,_bfin_proceso_error,_smails_notifica_error,_bnotifica_ok,_bfin_proceso_ok,_smails_notifica_ok):


	_ssubject_ok = "OK - Proceso de importación finalizado correctamente"
	_ssubject_error = "ERROR - El proceso de importación finalizó con error"

	#notificar por mail el OK y el error

	if _bnotifica_error == True:
		print('_bnotifica_error: ' + str(_bnotifica_error))
		if _bfin_proceso_error == True:
			print('_bfin_proceso_error: ' + str(_bfin_proceso_error))

			if not _smails_notifica_error == True:
				print('_smails_notifica_error: ' + str(_smails_notifica_error))
		
				_notif = Notificacion()
				_notif._message = _slogfinal
				_notif._subject = _ssubject_error
				_notif._from = 'daniel.gonzalez@emser.net'
				_notif._to = _smails_notifica_ok
				_notif._smtp_server = "mail.emser.net"
				_notif._smtp_port = 2525
				_notif._user = 'daniel.gonzalez@emser.net'
				_notif._user_password = 'arcangel2012'				

				_notif.SendMail()

	if _bnotifica_ok == True:
		print('_bnotifica_ok: ' + str(_bnotifica_ok))
		if _bfin_proceso_ok == True:
			print('_bfin_proceso_ok: ' + str(_bfin_proceso_ok))

			if not _smails_notifica_ok == True:
				print('_smails_notifica_ok: ' + str(_smails_notifica_ok))
	
				_notif = Notificacion()
				_notif._message = _slogfinal
				_notif._subject = _ssubject_ok
				_notif._from = 'daniel.gonzalez@emser.net'
				_notif._to = _smails_notifica_ok
				_notif._smtp_server = "mail.emser.net"
				_notif._smtp_port = 2525
				_notif._user = 'daniel.gonzalez@emser.net'
				_notif._user_password = 'arcangel2012'				

				_notif.SendMail()



def getHashFromString(item):
	_shash = item['NIS_RAD'].strip(' ') + item['NIC'].strip(' ') + item['TIP_SERV'].strip(' ') + item['REF_DIR'].strip(' ') + item['ACC_PM'].strip(' ') + item['CO_MARCA'].strip(' ') + item['NUM_APA'].strip(' ') +  item['DIRECCION'].strip(' ') + item['NUM_PUERTA'].strip(' ') + item['CGV_PM'].strip(' ') + item['DUPLICADOR'].strip(' ') + item['LOCALIDAD'].strip(' ') + item['MUNICIPIO'].strip(' ') + item['DEPTO'].strip(' ')
	_hash = md5()
	_hash.update(_shash.encode('utf-8'))

	_val = _hash.hexdigest()
	return _val

	




#////////////////////////////////////////////////////////
#inicio del proceso de importacion
#////////////////////////////////////////////////////////


def importar(id_centro, user):

	#variables
	_ftp = None
	_ĺistarutas=[]
	_codigos = []
	_fileName = ""
	_logfileName = ""

	#ruta de suministros
	_rutasum = None

	#proceso de impexp
	_proceso_imp = None


	_btxtimport = False
	_bwsimport  = False
	_bftpimport = False



	_urlftp = ""
	_userftp = ""
	_passftp = ""
	_dirftp = ""
	_dirlocal = ""
	_dirBkpImp = ""

	#fecha de generacion para usar en el nro de orden
	_sfecha_generacion = ""
	
	#string del log a retornar
	_slogfinal = ""

	#parametro de num ruedas (default 8)
	_nnumero_ruedas = 8

	#parametro notificacion via mail
	_bnotifica_ok = False
	_bnotifica_error = False
	_bfin_proceso_ok = False
	_bfin_proceso_error = False

	_smails_notifica_ok = ""
	_smails_notifica_error = ""

	_smail_from = ""
	_smail_from_password = ""
	_smail_server = ""
	_nmail_server_port = 0


	_spath_log = ""

	try:
		print('Obteniendo parametros de directorio log')
		
		_param = Parametro.objects.get(pk='P_PATH_LOG_IMP_EXP')
		_spath_log = _param.valor_1
		
		print('P_PATH_LOG_IMP_EXP: ' + _spath_log )

	except Exception as errOf:
		print('Ocurrió un error al obtener parametros de configuración de path log: {}'.format(errOf))
		
		_spath_log = ".//defLog//"
		



	#CREACION DEL LOGGER
	_log = logging.getLogger('ImportExport')
	_fileName = getLoggerFileName(id_centro,'IMP',user.first_name + '_' + user.last_name)
	_logfileName = _spath_log + _fileName

	_log.setLevel(logging.INFO)
	
	handler = logging.FileHandler( _logfileName )

	handler.setLevel(logging.INFO)	
	formatter = logging.Formatter(
                    fmt='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                    )

	handler.setFormatter(formatter)
	_log.addHandler(handler)
	
	#FIN CREACION LOGGER



	#try general del proceso
	try:		
		
		#genero la cabecera del log
		generarCabeceraLog(_log)

		try:
			print('Obteniendo parametros de configuracion')
			_log.info('Obteniendo parametros de configuracion...')

			_param = Parametro.objects.get(pk='P_MAIL_SMTP_SERVER')
			_smail_server = _param.valor_1
			_nmail_server_port = _param.valor_2

			print('P_MAIL_SMTP_SERVER: ' + _smail_server + ' - ' + _nmail_server_port)

			_param = Parametro.objects.get(pk='P_MAIL_USER')
			_smail_from = _param.valor_1
			_smail_from_password = _param.valor_2

			print('P_MAIL_USER: ' + _smail_from + ' - ' + _smail_from_password)

			_param = Parametro.objects.get(pk='P_MAX_NUM_RUEDAS')
			_nnumero_ruedas = _param.valor_1

			print('P_MAX_NUM_RUEDAS: ' + _nnumero_ruedas )

		except Exception as errOf:
			print('Ocurrió un error al obtener parametros de configuración: {}'.format(errOf))
			_log.error('Ocurrió un error al obtener parametros de configuración: {}'.format(errOf))

			_bfin_proceso_error = True

			generarPieLog(_log)			
			_slogfinal = str(getLoggingFileData(_logfileName))
			cerrarLog(_log)
					
			return _slogfinal



		#verifico que no haya otro proceso corriendo para la misma oficina
		try:

			_proceso_imp =  ProcesoImpExp.objects.get(oficina=id_centro,proceso=1,tipo_proceso='I')
			
			if _proceso_imp.estado_proceso == 0:

				print('Proceso disponible para ejecución')
				_log.info('Iniciando proceso de importación...')

				_proceso_imp.estado_proceso = 1
				_proceso_imp.fh_inicio_proceso = datetime.datetime.today().strftime('%d/%m/%Y %H:%M')

				_proceso_imp.ejecutado_por = user.username

				_proceso_imp.save()

			else:

				print('Proceso disponible para ejecución')
				_log.info('El proceso de importación ya se encuentra iniciado por el usuario: {} - {}'.format(str(_proceso_imp.ejecutado_por),_proceso_imp.fh_inicio_proceso) )

				_bfin_proceso_error = False
				_bfin_proceso_ok = True

				generarPieLog(_log)			
				_slogfinal = str(getLoggingFileData(_logfileName))
				cerrarLog(_log)
					
				return _slogfinal

		except Exception as err:
			print('Registro de proceso inexistente. Creando registro de proceso')
			_proceso_imp = ProcesoImpExp()
			_proceso_imp.oficina = WorkUnit.objects.get(pk=id_centro)
			_proceso_imp.proceso = 1
			_proceso_imp.nombre_proceso = 'Importación'
			_proceso_imp.descripcion_proceso = 'Importación por archivo de texto'
			_proceso_imp.tipo_proceso = 'I'
			_proceso_imp.estado_proceso = 1
			_proceso_imp.fh_inicio_proceso = datetime.datetime.today().strftime('%d/%m/%Y %H:%M')
			_proceso_imp.ejecutado_por = user.username

			_proceso_imp.save()


			
		



		#obtengo el obj parametro de config de oficina para la importacion
		try:
			print("Importando oficina {}".format(id_centro))

			configoficina = ConfigParamsImpExp.objects.get(oficina=id_centro)			
			print(configoficina)

			#obtengo los datos del parametro de notificacion del proceso de importacion

			if configoficina.notificar_ok == 1:				
				_bnotifica_ok = True

			if configoficina.notificar_error == 1:				
				_bnotifica_error = True

			_smails_notifica_ok = configoficina.mails_ok
			_smails_notifica_error = configoficina.mails_error

		except Exception as errOf:
			print('La oficina {} no se encuentra configurada {}'.format(id_centro,errOf))
			_log.error('La oficina {} no se encuentra configurada'.format(id_centro))

			_bfin_proceso_error = True

			generarPieLog(_log)			
			_slogfinal = str(getLoggingFileData(_logfileName))
			cerrarLog(_log)
					
			return _slogfinal



		#verifico el medio de importacion que se debe realizar

		if configoficina.txt_import == 1:
			_btxtimport = True
			_log.info('Importación por archivo de texto')
		elif configoficina.ws_import == 1:
			_bwsimport = True
			_log.info('Importación por web service')
		elif configoficina.ftp_import == 1:
			_bftpimport = True
			_log.info('Importación por archivo de texto vía FTP')

		if _bftpimport == True:

			filenamecabecera = 'lese0350.dat'		
			filenamedetalle = 'lese0355.dat'

			#obtengo los datos de configuracion
			_urlftp = configoficina.url_ftp_import
			_userftp = configoficina.ftp_user
			_passftp = configoficina.ftp_user_password
			_dirftp = configoficina.dir_ftp_import
			_dirlocal = configoficina.path_txt_import
			_dirBkpImp = configoficina.dir_ftp_bkp_import

			print(_urlftp)
			print(_userftp)
			print(_passftp)
			print(_dirftp)
			print(_dirlocal)
			make_sure_path_exists(_dirlocal)
			#proceso de copiado de archivo desde FTP
			

			#_ftp = FTP('02fbb77.netsolhost.com','djgonzalez','Sarmiento1150!')
			print('Conectando a FTP...')
			_log.info('Conectando a FTP...')
			_ftp = FTP(_urlftp,_userftp,_passftp)
			_log.info('Conexión correcta a FTP')
			print('Conexión correcta a FTP')
			_log.info('Cambiando directorio a: '+_dirftp)
			print('Cambiando directorio a: '+_dirftp)
			_ftp.cwd(_dirftp)

            
			#obtengo el md5 de la cabecera
			md5archivoenftp = getMD5(_ftp,filenamecabecera)			
			print(md5archivoenftp)
			getFile(_ftp,_dirlocal,filenamecabecera)

			#verifico integridad de la cabecera
			if compararIntegridadArchivo(md5archivoenftp,_dirlocal, filenamecabecera):
				_log.info('Archivo cabcera copiado correctamente')
			else:
				_log.info('Archivo cabcera no se copió correctamente')
				generarPieLog(_log)
				
				_bfin_proceso_error = True

				_slogfinal = str(getLoggingFileData(_logfileName))
				cerrarLog(_log)
				
				return _slogfinal

			#verifico integridad detalle
			md5archivodetalleenftp = getMD5(_ftp,filenamedetalle)
			print(md5archivodetalleenftp)
			getFile(_ftp,_dirlocal,filenamedetalle)


			#verifico integridad del detalle
			if compararIntegridadArchivo(md5archivodetalleenftp,_dirlocal, filenamedetalle):
				_log.info('Archivo detalle copiado correctamente')
			else:
				_log.info('Archivo detalle no se copió correctamente')
				generarPieLog(_log)

				_bfin_proceso_error = True

				_slogfinal = str(getLoggingFileData(_logfileName))
				cerrarLog(_log)
				
				return _slogfinal

			

	except Exception as ftperr:
		print(ftperr)		
		_log.error('Ocurrió un error al procesar los archivo del FTP: ' + str(ftperr))
		generarPieLog(_log)
				
		_bfin_proceso_error = True


		_slogfinal = str(getLoggingFileData(_logfileName))
		cerrarLog(_log)
				
		return _slogfinal
		
	finally:		
		if _ftp is not None:
			_ftp.quit()
		


	try:

		_log.info('abriendo archivo de rutas')
		print('abriendo archivo de rutas')
		#abro archivo cabecera de rutas
		arc_cabeRutas = etl.fromtsv(_dirlocal+filenamecabecera,encoding='ISO-8859-1')
		#incluyo la cabecera de cada campo
		print('#incluyo la cabecera de cada campo')
		reg_cabecera = etl.transform.pushheader(arc_cabeRutas, ['COD_UNICOM','RUTA','NUM_ITIN','CICLO','EST_ITIN','NL_AUS','NL_AN','NL_OK','NLGEN','F_LTEOR','F_GEN','F_RECEP','F_LREAL','F_FTRAT','F_FACT','COD_LECTOR','ACION','NUM_TPL','NL_ESTIM','NL_NO_REALIZ','F_ESTIM','USR_NUMBER1','USR_NUMBER2','USR_NUMBER3','USR_VARCHAR1','USR_VARCHA','USR_VARCHAR3','USR_DATETIME1','USR_DATETIME2','NL_REAL','TIP_NATUR'])
		#remuevo duplicados
		print('#remuevo duplicados')
		reg_cabeUnicas= etl.transform.distinct(table=reg_cabecera)
		#convierto a diccionario
		print('#convierto a diccionario')
		print(reg_cabeUnicas)
		reg_cabeRutas = etl.dicts(reg_cabeUnicas)
		print("CabeRutas {} ".format(len(reg_cabeRutas)))
		#obtengo todos los codigos antes de iterar por cada ruta
		_log.info('Obteniendo listado de códigos')
		print('Obteniendo listado de códigos')
		_codigos = Codigo.objects.all()

		#por cada ruta en la cabecera	
		#estado = EstadoRuta.objects.get(estado=1)	
		


		for _r in reg_cabeRutas:

			print("Cabecera ruta_sum: " + id_centro +  str(_r['RUTA']) + str(_r['NUM_ITIN']))
			try:		
				_rutasum = RutaSum.objects.get(oficina=id_centro,rutasum = str(_r['RUTA']), itinerario = str(_r['NUM_ITIN']))

			except Exception as e:
					print ("Error {}".format(e))
					_rutasum = None

			if _rutasum == None:
				_rutasum = RutaSum()
				_rutasum.oficina = WorkUnit.objects.get(id_workunit = id_centro)
				_rutasum.rutasum = str(_r['RUTA'])
				_rutasum.itinerario = str(_r['NUM_ITIN'])

				_rutasum.save()

			#print("Cabecera ruta "+str(_r))
			_ruta = Ruta()	
			_ruta.ruta = _rutasum
			_ruta.oficina = WorkUnit.objects.get(id_workunit = id_centro)
			_ruta.ciclo= str(_r['CICLO'])
			_ruta.ruta= str(_r['RUTA'])
			_ruta.itinerario = str(_r['NUM_ITIN'])
			_ruta.anio= str(datetime.date.today().year)+str(_r['CICLO']).strip('0').zfill(2)
			_ruta.cantidad= _r['NLGEN']
			_ruta.estado = 1
			_ruta.fecha_generacion =  datetime.datetime.strptime(_r['F_GEN'], '%Y/%m/%d').strftime('%Y-%m-%d') 
			_ruta.fecha_estimada_resolucion = datetime.datetime.strptime(_r['F_LTEOR'], '%Y/%m/%d').strftime('%Y-%m-%d')  
			

			_sfecha_generacion = datetime.datetime.strptime(_r['F_GEN'], '%Y/%m/%d').strftime('%Y%m%d') 
			#agregamos el obj a la lista
			_ĺistarutas.append(_ruta)

			print('ruta: '+ str(_ruta))


		#abro el detalle
		print('Abro el detalle')
		tabla = etl.fromtsv(_dirlocal+filenamedetalle,encoding='ISO-8859-1')
		#incluyo la cabecera de los campos
		print('incluyo la cabecera de los campos')
		tabla2 = etl.transform.pushheader(tabla, ['COD_UNICOM', 'RUTA','NUM_ITIN', 'CICLO', 'SEC_REG', 'AOL_FIN', 'NIF','COD_CALLE', 'NUM_PUERTA', 'DUPLICADOR', 'CGV_PM', 'ACC_FINCA', 'ACC_PM','NIS_RAD', 'CO_MARCA', 'NUM_APA', 'TIP_CSMO', 'F_LECT_ANT', 'LECT_ANT','LECT_MAX', 'LECT_MIN', 'CGV_SUM', 'NOM_CLI', 'NUM_RUE', 'COD_TAR','DEPTO', 'MUNICIPIO', 'LOCALIDAD', 'DIRECCION', 'SEC_NIS', 'REF_DIR','TIP_ASOC', 'CTE', 'TIP_SERV', 'NIC'])
		#remuevo duplicados
		print('remuevo duplicados')
		tabla3 = etl.transform.distinct(table=tabla2)

		#por cada ruta en la lista, filtro el detalle

		for objRuta in _ĺistarutas:
			
			_aparatos = []
			_consumos = []
			_ptoSum = []
			_ptosum_upd = []
			_ordenes = []
			_clientes = []
			_clientes_upd = []

			_log.info('Procesando ruta: ' + str(objRuta))
			print('Procesando ruta: ' + str(objRuta))
			strFiltro =  "{{{}}}  == '{}' and {{{}}}  == '{}' and {{{}}} == '{}'".format('CICLO', objRuta.ciclo,'RUTA',objRuta.ruta,'NUM_ITIN',objRuta.itinerario)

			#obtengo solo los registros de la ruta xx itinerario xxx y ciclo xx		
			print('obtengo solo los registros de la ruta xx itinerario xxx y ciclo xx')
			ItinFiltrado = etl.select(tabla3,  strFiltro )

			#creo una lista al que convierto en diccionario
			print('creo una lista al que convierto en diccionario')
			listaImport = etl.dicts(ItinFiltrado)
			print(listaImport)
			#lista de suministros
			print('lista de suministros')
			try:
				
				_marca = None
				_tipApa = None
				_tipInt = None
				_tipFase = None
				_tipTens = None
				_pref = None
				_p = None
				_pr = None
				_ts = None
				_ruta = None
				_to = None
				
				_tcsmo = None
				_cli = None

				try:
					print('Trato de leer la ruta {} {} {} {} {}'.format(id_centro,objRuta.ciclo,objRuta.ruta,objRuta.itinerario,objRuta.anio))
					_ruta = Ruta.objects.get(oficina=id_centro,ciclo=objRuta.ciclo,ruta=objRuta.ruta,itinerario=objRuta.itinerario,anio=objRuta.anio)
					
				except Exception as e:
					print ("Error {}".format(e))
					_ruta = None


				_rutasum = RutaSum.objects.get(oficina=id_centro,rutasum = objRuta.ruta, itinerario = objRuta.itinerario)


				print("Antes de _ruta is None")
				if _ruta is None:
					print('Creando ruta')
					_ruta = Ruta()
			
					_ruta.rutasum = _rutasum
					_ruta.oficina = WorkUnit.objects.get(id_workunit = id_centro)
					_ruta.ciclo=objRuta.ciclo
					_ruta.ruta=objRuta.ruta
					_ruta.itinerario = objRuta.itinerario
					_ruta.anio=objRuta.anio
					_ruta.cantidad=objRuta.cantidad
					_ruta.fecha_generacion = objRuta.fecha_generacion
					_ruta.fecha_estimada_resolucion = objRuta.fecha_estimada_resolucion
					_ruta.estado = objRuta.estado
					#_log.info('Creando ruta: ' + str(_ruta)
					#print('Creando ruta: {}'.format(_ruta))
					_ruta.save()
					#_histEstadoRuta = HistoricoEstadoRuta()
					#_histEstadoRuta.ruta = _ruta
					#_histEstadoRuta.fecha = datetime.date.today()
					#_histEstadoRuta.usuario = user
					#_histEstadoRuta.estado = 1
					#_histEstadoRuta.save()
					
				else:
					
					#verifico que las ordenes de trabajo no esten trabajadas
					if OrdenDeTrabajo.objects.filter(ruta = _ruta,estado__gt = 1).count() > 0:
						print('cantidad > 0')
						_log.info('    La ruta {} no se puede importar nuevamente. Las órdenes ya se encuentran asignadas para ser trabajadas'.format(_ruta))
						continue

					else:
						print('cantidad = 0')
						#borro todas las ordenes de trabajo
						print('Borrando ordenes de trabajo de la ruta {}'.format(str(_ruta) ))
						OrdenDeTrabajo.objects.filter(ruta = _ruta).delete()


				#borro los consumos de los suministro de la ruta

				#creo una lista de aparatos
				_la = []
				#QuerySet con las ordenes de trabajo de la ruta
				_odt = None
				try:
				   _odt = OrdenDeTrabajo.objects.select_related('punto_suministro__aparato').filter(ruta = _ruta)
				except Exception as e:
					print("Error: {}".format(e))
				
				try:
					#por cada orden, suministro -> carga en la lista el aparato del suministro
					if _odt != None:
						for x in _odt:
							print(x)
							_la.append(x.punto_suministro.aparato.aparato)
					else:
						print("ANTES 17")
				except Exception as e:
					print("error despues 17 {}".format(e))
				try:
					print("17")
					#borro todos los consumos anteriores de los aparatos de la ruta
					Consumo.objects.filter(aparato__in = _la).distinct().delete()
					print("18")				
				except Exception as e:
					print("error despues 17")
					_log.error('Error al borrar consumos: {} '.format(e))
					print('Error al borrar consumos:  {} '.format(e))
					generarPieLog(_log)

					_bfin_proceso_error = True
				
					_slogfinal = str(getLoggingFileData(_logfileName))
					cerrarLog(_log)
				
					return _slogfinal
				
				#obtengo el objeto tipo orden LECTURA
				try:
					print("19")
					_to = TipoOrden.objects.get(tipo_orden="LECT")					
				except:
					_to = None

				#si no existe lo creo
				if _to is None:
					_to = TipoOrden()
					_to.tipo_orden = "LECT"
					_to.descripcion= "LECTURA"
					_to.clase_actividad = "LECT"
					_to.descripcion_clase_actividad=""
					_to.save()

				
				#obtengo el estado de la orden IMPORTADA






				
				#por cada suministro
				for j in listaImport:


					#APARATO



					for x in _codigos:
						if x.codigo == j['CO_MARCA'].strip(' '):
							_marca = x
							break

					if _marca is None:
						_log.error('Suministro con código de marca inexistente: {} para el nis: {}'.format(j['CO_MARCA'],j['NIS_RAD']))
						print('Suministro con código de marca inexistente: {} para el nis: {}'.format(j['CO_MARCA'],j['NIS_RAD']))
					
						generarPieLog(_log)

						_bfin_proceso_error = True

						_slogfinal = str(getLoggingFileData(_logfileName))
						cerrarLog(_log)
				
						return _slogfinal

					codigo_aparato = str(_marca.codigo) + str(j['NUM_APA']).strip(' ')
					
					aparato_existe = False
					try:
						_apa = Aparato.objects.get(pk=codigo_aparato)
						aparato_existe = True
					except:
						aparato_existe = False

					if aparato_existe == False:                    
						#creo el codigo del aparato
						_apa = Aparato()
						_apa.aparato = codigo_aparato
						_apa.marca = _marca
						_apa.num_serie = j['NUM_APA'].strip(' ')
						
						if int(j['NUM_RUE']) <= int(_nnumero_ruedas):						
							_apa.num_ruedas = j['NUM_RUE'].strip(' ')
							_apa.tipo_aparato = None
							_apa.estado_aparato = 1
							_apa.tipo_intensidad = None
							_apa.tipo_fase = None
							_apa.tipo_tension = None
						else:
						
							print(j['NUM_RUE'])

							_log.error('El valor de número de ruedas supera el valor máximo configurado' \
							' para el número de aparato: {} \nValor actual: {} - Valor max: {}'.format(j['NUM_APA'],str(j['NUM_RUE']), str(_nnumero_ruedas) ) )

							_log.error('No se completó la importación para la ruta actual' )

							_bfin_proceso_error = True
						
							generarPieLog(_log)

							_slogfinal = str(getLoggingFileData(_logfileName))
							cerrarLog(_log)
				
							return _slogfinal



						#si no existe el aparato en la lista o en la base de datos lo agrego a la lista
						#if not Aparato.objects.filter(marca=_apa.marca,num_serie= _apa.num_serie).exists():						
						if not any(  (x.marca == _apa.marca and x.num_serie == _apa.num_serie)  for x in _aparatos):
							_aparatos.append(_apa)

				


					#CONSUMO
					clave = str(_apa.marca.codigo).strip(' ') + str(_apa.num_serie).strip(' ') + j['TIP_CSMO'].strip(' ')
					consumo_existe = False
					try:
						_csmo = Consumo.objects.get(pk=clave)
						consumo_existe = True
					except:
						consumo_existe = False

					if consumo_existe == False:
						_csmo = Consumo()
						_csmo.aparato = _apa

						#creo codigo de consumo
						_csmo.consumo = clave
					
						#la constante es float y se usa . como separador decimal
						_csmo.constante = float(j['CTE'].strip(' ').replace(',','.'))


						for x in _codigos:
							if x.codigo == j['TIP_CSMO'].strip(' '):
								_tcsmo = x
								break


						if _tcsmo is None:
							_log.error('Suministro con código de consumo inexistente: {} para el nis: {}'.format(j['TIP_CSMO'],j['NIS_RAD']))
							print('Suministro con código de consumo inexistente: {} para el nis: {}'.format(j['TIP_CSMO'],j['NIS_RAD']))
						
							generarPieLog(_log)

							_bfin_proceso_error = True

							_slogfinal = str(getLoggingFileData(_logfileName))
							cerrarLog(_log)
				
							return _slogfinal




						_csmo.tipo_consumo = _tcsmo
						_csmo.consumo_anterior = 0
						_csmo.lectura_anterior = j['LECT_ANT']
						_csmo.fecha_lectura_anterior = datetime.datetime.strptime(j['F_LECT_ANT'], '%Y/%m/%d').strftime('%Y-%m-%d')
						_csmo.tope_lectura_maxima = j['LECT_MAX']
						_csmo.tope_lectura_minima = j['LECT_MIN']

																	
						if not any(x.aparato.marca.codigo == _csmo.aparato.marca.codigo and x.aparato.num_serie == _csmo.aparato.num_serie and x.tipo_consumo.codigo == _csmo.tipo_consumo.codigo for x in _consumos):
							_consumos.append(_csmo)
					






					#CLIENTE
					#_cli = Cliente()
					#_cli.nombre = j['NOM_CLI']
					#_cli.codigo = j['NIC'] + j['NIS_RAD']
					
					#if not Cliente.objects.filter(codigo=_cli.codigo).exists():											
					#	if not any(x.codigo == _cli.codigo  for x in _clientes):
					#		_clientes.append(_cli)
                    
					#print("Cliente {}".format(_cli))





					#PUNTO DE SUMINISTRO
					_hashdata = getHashFromString(j)
					sum_existe = False
					try:					
						_psum = PuntoDeSuministro.objects.get(pk=j['NIS_RAD'].strip(' '))
						sum_existe = True
					except:
						sum_existe = False

					if sum_existe:
						

						if(_psum.hashdata != _hashdata):

							print( 'hash base: ' + _psum.hashdata  + '  hash generado: ' + _hashdata)

							#hacer update
							_psum.hashdata = _hashdata
							
							#CLIENTE
							clave = str(j['NIC'].strip(' ')+ j['NIS_RAD'].strip(' '))
							cli_existe = False

							try:
								_cli = Cliente.objects.get(codigo=clave)
								cli_existe = True
							except:
								cli_existe = False

							if cli_existe == False:

								#CLIENTE
								_cli = Cliente()
								_cli.nombre = j['NOM_CLI'].strip(' ')
								_cli.codigo = j['NIC'].strip(' ') + j['NIS_RAD'].strip(' ')
																		
								if not any(x.codigo == _cli.codigo  for x in _clientes):
									_clientes.append(_cli)

							_psum.cliente = _cli
							
							_psum.num_contrato = j['NIC'].strip(' ')
							_psum.punto_suministro = j['NIS_RAD'].strip(' ')

							#no viene la tarifa en la interfaz
							_psum.tarifa = None


							#busco tipo de servicio en codigos
							for x in _codigos:
								if x.codigo == j['TIP_SERV']:
									_tserv = x
									break


							if _tserv is None:
								_log.error('Suministro con código de tipo de servicio inexistente: {} para el nis: {}'.format(j['TIP_SERV'],j['NIS_RAD']))
								print('Suministro con código de tipo de servicio inexistente: {} para el nis: {}'.format(j['TIP_SERV'],j['NIS_RAD']))
								generarPieLog(_log)
								_bfin_proceso_error = True
								_slogfinal = str(getLoggingFileData(_logfileName))
								cerrarLog(_log)
								return _slogfinal

							_psum.tipo_servicio = _tserv
							
							
							_psum.gps_latitud = '0.0'
							_psum.gps_longitud = '0.0'
							_psum.ref_direccion = j['REF_DIR'].strip(' ')
							_psum.nif = j['NIF'].strip(' ')
							_psum.ref_suministro = j['ACC_PM'].strip(' ')

							if not j['NUM_APA'].strip(' ') == 'CONDIR':
								_psum.estado_suministro = 1
							else:
								_psum.estado_suministro = 0		

							_psum.rutasum = _ruta.rutasum

							_psum.calle = j['DIRECCION'].strip(' ')
							_psum.numero_puerta = j['NUM_PUERTA'].strip(' ')
							_psum.piso = j['CGV_PM'].strip(' ')
							_psum.duplicador = j['DUPLICADOR'].strip(' ')
							_psum.localidad = j['LOCALIDAD'].strip(' ')
							_psum.municipio = j['MUNICIPIO'].strip(' ')
							_psum.barrio = ""
							_psum.departamento = j['DEPTO'].strip(' ')
							_psum.codigo_postal = ""

							_psum.aparato = _apa
							_psum.tipo_asociacion = None
							
							#agrego para despues hacer upd
							_ptosum_upd.append(_psum)

							print('psum cambio: ' + j['NIS_RAD'].strip(' '))
							_log.info('psum cambio: ' + j['NIS_RAD'].strip(' '))

							#print(_orden)	
						#else:
							#print('hash no es distinto')


						#ORDEN_TRABAJO
						_orden = OrdenDeTrabajo()
						_orden.numero_orden = id_centro + _sfecha_generacion + objRuta.ruta.strip('0').zfill(2) + objRuta.itinerario.strip('0').zfill(4) + j['SEC_REG'].zfill(4)
						_orden.punto_suministro = _psum
						_orden.tipo_orden = _to
						_orden.prioridad = 1
						_orden.estado = 1
						_orden.secuencial_registro = j['SEC_REG'].strip(' ')
						_orden.secuencia_teorica = j['SEC_REG'].strip(' ')
						_orden.ruta = _ruta
						_orden.consumo = _csmo
						#print("Orden trabajo {}".format(_orden.punto_suministro.cliente))
						_ordenes.append(_orden)

					else:

						#print('no existe')

						#CLIENTE
						_cli = Cliente()
						_cli.nombre = j['NOM_CLI'].strip(' ')
						_cli.codigo = j['NIC'].strip(' ') + j['NIS_RAD'].strip(' ')
					
						if not Cliente.objects.filter(codigo=_cli.codigo).exists():											
							if not any(x.codigo == _cli.codigo  for x in _clientes):
								_clientes.append(_cli)
                    
						#print("Cliente {}".format(_cli))

						_ps = PuntoDeSuministro()
						_ps.hashdata = _hashdata
						_ps.cliente = _cli
						
						print('asocio cliente')
						#print(_cli)

						_ps.num_contrato = j['NIC'].strip(' ')
						_ps.punto_suministro = j['NIS_RAD'].strip(' ')

						_ps.tarifa = None

						for x in _codigos:
							if x.codigo == j['TIP_SERV']:
								_tserv = x
								break


						if _tserv is None:
							_log.error('Suministro con código de tipo de servicio inexistente: {} para el nis: {}'.format(j['TIP_SERV'],j['NIS_RAD']))
							print('Suministro con código de tipo de servicio inexistente: {} para el nis: {}'.format(j['TIP_SERV'],j['NIS_RAD']))

							generarPieLog(_log)
							_bfin_proceso_error = True

							_slogfinal = str(getLoggingFileData(_logfileName))
							cerrarLog(_log)
					
							return _slogfinal



						_ps.tipo_servicio = _tserv
						
						
						_ps.gps_latitud = '0.0'
						_ps.gps_longitud = '0.0'
						_ps.ref_direccion = j['REF_DIR'].strip(' ')
						_ps.nif = j['NIF'].strip(' ')
						_ps.ref_suministro = j['ACC_PM'].strip(' ')

						if not j['NUM_APA'].strip(' ') == 'CONDIR':
							_ps.estado_suministro = 1
						else:
							_ps.estado_suministro = 0		

						_ps.rutasum = _ruta.rutasum

						_ps.calle = j['DIRECCION'].strip(' ')
						_ps.numero_puerta = j['NUM_PUERTA'].strip(' ')
						_ps.piso = j['CGV_PM'].strip(' ')
						_ps.duplicador = j['DUPLICADOR'].strip(' ')
						_ps.localidad = j['LOCALIDAD'].strip(' ')
						_ps.municipio = j['MUNICIPIO'].strip(' ')
						_ps.barrio = ""
						_ps.departamento = j['DEPTO'].strip(' ')
						_ps.codigo_postal = ""

						_ps.aparato = _apa
						_ps.tipo_asociacion = None
						
						#if not PuntoDeSuministro.objects.filter(pk=_ps.punto_suministro).exists():						
						if not any(x.punto_suministro == _ps.punto_suministro for x in _ptoSum):
							_ptoSum.append(_ps)

						#ORDEN_TRABAJO
						_orden = OrdenDeTrabajo()
						_orden.numero_orden = id_centro + _sfecha_generacion + objRuta.ruta.strip('0').zfill(2) + objRuta.itinerario.strip('0').zfill(4) + j['SEC_REG'].zfill(4)
						_orden.punto_suministro = _ps
						_orden.tipo_orden = _to
						_orden.prioridad = 1
						_orden.estado = 1 
						_orden.secuencial_registro = j['SEC_REG'].strip(' ')
						_orden.secuencia_teorica = j['SEC_REG'].strip(' ')
						_orden.ruta = _ruta
						_orden.consumo = _csmo
						#print("Orden trabajo {}".format(_orden.punto_suministro.cliente))
						_ordenes.append(_orden)

						#print(_orden)								

				#Bulk Insert
			

				print('insert clientes {}'.format(len(_clientes)))
				if len(_clientes) > 0:
					Cliente.objects.bulk_create(_clientes)
					_log.info('\tClientes insertados: ' + str(len(_clientes)))
				

				print('insert aparatos {}'.format(len(_aparatos)))
				if len(_aparatos) > 0:
					Aparato.objects.bulk_create(_aparatos)
					_log.info('\tAparatos insertados: ' + str(len(_aparatos)))


				print('insert csmo  {}'.format(len(_consumos)))
				if len(_consumos) > 0:
					Consumo.objects.bulk_create(_consumos)
					_log.info('\tConsumos insertados: ' + str(len(_consumos)))
				

				print('insert ptosum  {}'.format(len(_ptoSum)))

				if len(_ptosum_upd) > 0:
					print('Suministro actualizado {}'.format(len(_ptosum_upd)))
					for x in _ptosum_upd:
						x.save()

				if len(_ptoSum) > 0:
					print(_ptoSum[0].cliente)
					PuntoDeSuministro.objects.bulk_create(_ptoSum)
					_log.info('\tSuministros insertados: ' + str(len(_ptoSum)))
				
				

				print('insert ot  {}'.format(len(_ordenes)))
				if len(_ordenes) > 0:
					OrdenDeTrabajo.objects.bulk_create(_ordenes)
					_log.info('\tOrdenes de trabajo insertados: ' + str(len(_ordenes)))
				



				print("Inserto todo")

				print('Limpio todo')
				_psum = []
				_ptosum_upd = []
				_aparatos = []
				_clientes = []
				_ordenes = []
				_consumos = []


				

			except Exception as err:
				_log.error('Ocurrió un error al procesar la ruta:  {}'.format(err))
				print('Ocurrió un error al procesar la ruta: {}'.format(err))					
				generarPieLog(_log)

				_bfin_proceso_error = True


				#abro el archivo para que muestre el log
				_slogfinal = str(getLoggingFileData(_logfileName))
				cerrarLog(_log)

				return _slogfinal

			#fin try catch

		#fin for

		#si termino todo bien finaliza el proceso
		_bfin_proceso_ok = True

		generarPieLog(_log)		
		_slogfinal = str(getLoggingFileData(_logfileName))


		_ftp = None

		try:
			#muevo el bkp del archivo
			print('Conectando a FTP bkp...')
			_log.info('Conectando a FTP bkp...')
			_ftp = FTP(_urlftp,_userftp,_passftp)
			_log.info('Conexión correcta a FTP')
			print('Conexión correcta a FTP')
		
			print('Cambiando directorio a: ' + _dirBkpImp)
			_ftp.cwd(_dirBkpImp)
			_log.info('Copiando archivo')
			print(_dirlocal + filenamecabecera)
			_ftp.storbinary('STOR ' + filenamecabecera +  datetime.datetime.today().strftime('%Y%m%d') , open(_dirlocal + filenamecabecera, 'rb'))
			_ftp.storbinary('STOR ' + filenamedetalle +  datetime.datetime.today().strftime('%Y%m%d')  , open(_dirlocal + filenamedetalle, 'rb'))


		except Exception as e:
			_log.error('Error al copiar a bkp backenv: ' + str(e))
		finally:		
			if _ftp is not None:
				_ftp.quit()

		


		cerrarLog(_log)
		return _slogfinal

	except Exception as e:
		_log.error("Ocurrió un error en el proceso de importación de ruta: {}".format(e))
		print('Ocurrió un error en el proceso de importación de ruta: {}'.format(e))	

		_bfin_proceso_error = True
					
		generarPieLog(_log)		
		_slogfinal = str(getLoggingFileData(_logfileName))
	
		cerrarLog(_log)



		#verifico que no haya otro proceso corriendo para la misma oficina
		try:

			_proceso_imp =  ProcesoImpExp.objects.get(oficina=id_centro,proceso=1,tipo_proceso='I')
			
				
			_log.info('Finalinzando proceso de importación...')
			_proceso_imp.estado_proceso = 0
			#_proceso_imp.fh_inicio_proceso = _proceso_imp.fh_inicio_proceso
			_proceso_imp.fh_fin_proceso = datetime.datetime.today().strftime('%d/%m/%Y %H:%M')

			_proceso_imp.save()

		


		except Exception as err:
			print(str(err))
			print('Registro de proceso inexistente. Creando registro de proceso')
			
			_proceso_imp = ProcesoImpExp()
			_proceso_imp.oficina = WorkUnit.objects.get(pk=id_centro)
			_proceso_imp.proceso = 1
			_proceso_imp.nombre_proceso = 'Importación'
			_proceso_imp.descripcion_proceso = 'Importación por archivo de texto'
			_proceso_imp.tipo_proceso = 'I'
			_proceso_imp.estado_proceso = 0
			_proceso_imp.fh_fin_proceso = datetime.datetime.today().strftime('%d/%m/%Y %H:%M')
			_proceso_imp.ejecutado_por = user.username

			_proceso_imp.save()




		return _slogfinal

	finally:



		#verifico que no haya otro proceso corriendo para la misma oficina
		try:

			_proceso_imp =  ProcesoImpExp.objects.get(oficina=id_centro,proceso=1,tipo_proceso='I')
			
				
			_log.info('Finalinzando proceso de importación...')
			_proceso_imp.estado_proceso = 0
			#_proceso_imp.fh_inicio_proceso = _proceso_imp.fh_inicio_proceso
			_proceso_imp.fh_fin_proceso = datetime.datetime.today().strftime('%d/%m/%Y %H:%M')

			_proceso_imp.save()

		


		except Exception as err:
			print(str(err))
			print('Registro de proceso inexistente. Creando registro de proceso')
			
			_proceso_imp = ProcesoImpExp()
			_proceso_imp.oficina = WorkUnit.objects.get(pk=id_centro)
			_proceso_imp.proceso = 1
			_proceso_imp.nombre_proceso = 'Importación'
			_proceso_imp.descripcion_proceso = 'Importación por archivo de texto'
			_proceso_imp.tipo_proceso = 'I'
			_proceso_imp.estado_proceso = 0
			_proceso_imp.fh_fin_proceso = datetime.datetime.today().strftime('%d/%m/%Y %H:%M')
			_proceso_imp.ejecutado_por = user.username

			_proceso_imp.save()




		#_slogfinal = str(getLoggingFileData(_logfileName))
		notificarFinProceso(_slogfinal,_bnotifica_error,_bfin_proceso_error,_smails_notifica_error,_bnotifica_ok,_bfin_proceso_ok,_smails_notifica_ok)

		
