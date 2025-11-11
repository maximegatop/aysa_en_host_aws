from qorder.models import *
from core.models import *
from hashlib import md5
from ftplib import FTP
from qorder.utils import *
from django.core.exceptions import ObjectDoesNotExist
import petl as etl
import datetime
import time
import logging
import os
import errno
import csv


def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def compararIntegridadArchivo(ftp,pathremote,pathlocal,  filename):
	md5file = getMD5FromFile(pathlocal + filename)
	md5FtpFile = getMD5(ftp,pathremote+filename)
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


def placeFile(ftp,localdir, filename):
	#filename = 'lese0350_20160814.txt'
	print ('STOR ' + filename)
	ftp.storbinary('STOR ' + filename, open(localdir+filename, 'rb'))


def getLoggerFileName(oficina,proceso,usuario):
	logfileName = '{}_{}_{}_{}.txt'.format(oficina,proceso,usuario,datetime.datetime.today().strftime('%Y%m%d_%H%M%S'))
	return logfileName


def generarCabeceraLog(_log):
	_log.info('******************************************')
	_log.info('       Qorder exportación - V1.0          ')
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
				_notif._to = 'daniel.jor.gonzalez@gmail.com'
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
				_notif._to = 'daniel.jor.gonzalez@gmail.com'
				_notif._smtp_server = "mail.emser.net"
				_notif._smtp_port = 2525
				_notif._user = 'daniel.gonzalez@emser.net'
				_notif._user_password = 'arcangel2012'				

				_notif.SendMail()



def getHashFromString(item):
	_shash = item['NIS_RAD'] + item['NIC'] + item['TIP_SERV'] + item['REF_DIR'] + item['ACC_PM'] + item['CO_MARCA'] + item['NUM_APA'] +  item['DIRECCION'] + item['NUM_PUERTA']+ item['CGV_PM'] + item['DUPLICADOR'] + item['LOCALIDAD'] + item['MUNICIPIO'] + item['DEPTO']
	_hash = md5()
	_hash.update(_shash.encode('utf-8'))

	_val = _hash.hexdigest()
	return _val

def setBit(int_type, offset):
    mask = 1 << offset
    return(int_type | mask)	




#////////////////////////////////////////////////////////
#inicio del proceso de exportacion
#////////////////////////////////////////////////////////


def exportar(id_centro, user):

	#variables
	_ftp = None
	_ĺistarutas=[]
	_codigos = []
	_logfileName = ""

	#ruta de suministros
	_rutasum = None

	#proceso de impexp
	_proceso_imp = None


	_btxtexport = False
	_bwsexport  = False
	_bftpexport = False


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



	#CREACION DEL LOGGER
	_log = logging.getLogger('ImportExport')
	_logfileName = getLoggerFileName(id_centro,'EXP',user.first_name + '_' + user.last_name)

	_log.setLevel(logging.INFO)
	handler = logging.FileHandler(filename=_logfileName)
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

			_param = Parametro.objects.get(parametro='P_MAIL_SMTP_SERVER')
			_smail_server = _param.valor_1
			_nmail_server_port = _param.valor_2

			print('P_MAIL_SMTP_SERVER: ' + _smail_server + ' - ' + _nmail_server_port)

		#_param = Parametro.objects.get(parametro='P_MAIL_USER')
		#_smail_from = _param.valor_1
		#_smail_from_password = _param.valor_2

			print('P_MAIL_USER: ' + _smail_from + ' - ' + _smail_from_password)


		except Exception as errOf:
			print('Ocurrió un error al obtener parametros de configuración: {}'.format(errOf))
			_log.error('Ocurrió un error al obtener parametros de configuración: {}'.format(errOf))

			_bfin_proceso_error = True

			generarPieLog(_log)			
			_slogfinal = str(getLoggingFileData(_logfileName))
			cerrarLog(_log)
					
			return _slogfinal


		
		#_log.error('verifico que no haya otro proceso corriendo para la misma oficina: ')

		#verifico que no haya otro proceso corriendo para la misma oficina
		try:

			_proceso_imp =  ProcesoImpExp.objects.get(oficina=id_centro,proceso=1,tipo_proceso='E')
			
			if _proceso_imp.estado_proceso == 0:

				print('Proceso disponible para ejecución')
				_log.info('Iniciando proceso de exportación...')

				_proceso_imp.estado_proceso = 1
				_proceso_imp.fh_inicio_proceso = datetime.datetime.today().strftime('%d/%m/%Y %H:%M')

				_proceso_imp.ejecutado_por = user.username

				_proceso_imp.save()

			else:

				print('Proceso no disponible para ejecución')
				_log.info('El proceso de exportación ya se encuentra iniciado por el usuario: {} - {}'.format(str(_proceso_imp.ejecutado_por),_proceso_imp.fh_inicio_proceso) )

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
			_proceso_imp.nombre_proceso = 'Exportación'
			_proceso_imp.descripcion_proceso = 'Exportación por archivo de texto'
			_proceso_imp.tipo_proceso = 'E'
			_proceso_imp.estado_proceso = 1
			_proceso_imp.fh_inicio_proceso = datetime.datetime.today().strftime('%d/%m/%Y %H:%M')
			_proceso_imp.ejecutado_por = user.username

			_proceso_imp.save()

		#_log.error('obtengo el obj parametro de config de oficina para la exportacion ')

		#obtengo el obj parametro de config de oficina para la exportacion
		try:
			print("Exportando oficina {}".format(id_centro))
			_log.info("Exportando oficina {}".format(id_centro))
			configoficina = ConfigParamsImpExp.objects.get(oficina=id_centro)			
			print(configoficina)

			#obtengo los datos del parametro de notificacion del proceso de importacion

			if configoficina.notificar_ok == 1:				
				_bnotifica_ok = True

			if configoficina.notificar_error == 1:				
				_bnotifica_error = True

			_smails_notifica_ok = configoficina.mails_ok
			_smails_notifica_error = configoficina.mails_error
			_urlftp = configoficina.url_ftp_import
			_userftp = configoficina.ftp_user
			_passftp = configoficina.ftp_user_password
			_dirftp = configoficina.dir_ftp_export
			_dirlocal = configoficina.path_txt_export
			make_sure_path_exists(_dirlocal)
		except Exception as errOf:
			print('La oficina {} no se encuentra configurada {}'.format(id_centro,errOf))
			_log.error('La oficina {} no se encuentra configurada'.format(id_centro))

			_bfin_proceso_error = True

			generarPieLog(_log)			
			_slogfinal = str(getLoggingFileData(_logfileName))
			cerrarLog(_log)
					
			return _slogfinal

		#verifico el medio de exportacion que se debe realizar

		if configoficina.txt_export == 1:
			_btxtexport = True
			_log.info('Exportación por archivo de texto')
		elif configoficina.ws_export == 1:
			_bwsexport = True
			_log.info('Exportación por web service')
		elif configoficina.ftp_export == 1:
			_bftpexport = True
			_log.info('Exportación por archivo de texto vía FTP')

		#busco las rutas que estan en condición de ser exportadas

		centro = WorkUnit.objects.get(pk=id_centro)

		ordpend = OrdenDeTrabajo.objects.filter(estado__in = [265,273,401])
		ordpend.query.group_by = ['ruta']
		rut = []
		for item in ordpend.values_list('ruta'):		
			cantord = OrdenDeTrabajo.objects.filter(ruta=item[0],estado__in = [265,273,401]).count()
			try:
				ruta = Ruta.objects.get(oficina=centro,id=item[0])
				print('{} {} {}'.format(item[0],cantord,ruta.cantidad))
				if cantord==ruta.cantidad:
					rut.append(item[0])  
			except ObjectDoesNotExist:
				print("")
		if len(rut)==0:
			print('No hay rutas en condiciones de ser exportadas')
			_log.error('La oficina {} no tiene rutas en condiciones de ser exportadas'.format(id_centro))
			_proceso_imp =  ProcesoImpExp.objects.get(oficina=id_centro,proceso=1,tipo_proceso='E')
			_log.info('Finalinzando proceso de exportación...')
			_proceso_imp.estado_proceso = 0
			#_proceso_imp.fh_inicio_proceso = _proceso_imp.fh_inicio_proceso
			_proceso_imp.fh_fin_proceso = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
			_proceso_imp.save()
			_bfin_proceso_error = True

			generarPieLog(_log)			
			_slogfinal = str(getLoggingFileData(_logfileName))
			cerrarLog(_log)
					
			return _slogfinal

		rutas = Ruta.objects.filter(oficina=centro,id__in=rut)


		f = open(_dirlocal+'_lese0451.dat', 'w', newline='')
		fo = open(_dirlocal+'_lese0452.dat','w', newline='')
		try:
			writer_ruta = csv.writer(f, delimiter='\t', quoting=csv.QUOTE_NONE)
			writer_orden = csv.writer(fo, delimiter='\t', quoting=csv.QUOTE_NONE)
			for ruta in rutas:
				#generar cabecera
				registro=[]
				registro.append(user.username)
				registro.append(datetime.datetime.now().strftime("%Y/%m/%d"))
				registro.append('QORDERWEB')
				registro.append(centro.id_workunit)
				registro.append(ruta.ruta)
				registro.append(ruta.itinerario)
				registro.append(ruta.ciclo)
				registro.append(datetime.datetime.now().strftime("%Y/%m/%d"))
				registro.append(ruta.tecnico.codigo)
				registro.append(1)
				registro.append(2)
				registro.append(2)
				registro.append(0)
				registro.append(datetime.datetime.now().strftime("%Y/%m/%d"))
				registro.append(0)
				registro.append(0)
				registro.append(0)
				registro.append(' ')
				registro.append(' ')
				registro.append(' ')
				registro.append('2999/12/31')
				registro.append('2999/12/31')
				print(registro)		
				writer_ruta.writerow(registro)

				ordenes = OrdenDeTrabajo.objects.filter(ruta=ruta)
				print(ordenes)
				for orden in ordenes:
					regorden = []
					if 'CONDIR' not in orden.consumo_id:
						regorden.append(user.username[ 0 : 30])
						regorden.append(datetime.datetime.now().strftime("%Y/%m/%d"))
						regorden.append('QORDERWEB')
						regorden.append(centro.id_workunit)
						regorden.append(ruta.ruta)
						regorden.append(ruta.ciclo)					
						regorden.append(ruta.itinerario)
						regorden.append(orden.secuencial_registro)
						regorden.append(orden.punto_suministro.nif)
						regorden.append(orden.punto_suministro.piso)
						
						try:
							desc_anomalia = Desc_Anomalia.objects.filter(orden_trabajo=orden).order_by('prioridad')[0]
							regorden.append(desc_anomalia.id_anomalia.id_anomalia)
							regorden.append(0)
						except:
							regorden.append('')
							regorden.append(0)
						try:
							lectura = Desc_Lectura.objects.get(orden_trabajo=orden.numero_orden)
	
							regorden.append(lectura.num_serie)
	
							regorden.append(lectura.marca_id)
	
							regorden.append(lectura.tipo_consumo_id)
						
							desc_orden = Desc_Orden.objects.get(orden_trabajo=orden)
	
							regorden.append(lectura.lectura)
							regorden.append(desc_orden.fh_fin.strftime("%Y/%m/%d"))
							regorden.append(desc_orden.fh_fin.strftime("%H%M%S"))
							regorden.append(orden.punto_suministro.tipo_servicio_id)
							regorden.append(orden.punto_suministro.num_contrato)
						except:
							print(orden.numero_orden)
						print(regorden)
						
						writer_orden.writerow(regorden)
						nuevo = setBit(orden.estado,9)
						orden.estado = nuevo
						orden.save()
					else:
						nuevo = setBit(orden.estado,9)
						orden.estado = nuevo
						orden.save()
						print('Orden {} - CONDIR quitado de exportacion'.format(orden.numero_orden))
				
				ruta.estado = 777
				ruta.save()


			#fin for	

		finally:
			f.close()
			fo.close()
		

		data0 = open(_dirlocal+'_lese0451.dat', "r", newline="").read()
		data1 = open(_dirlocal+'_lese0452.dat', "r", newline="").read()

		newdata0 = data0.replace("\r", "")
		newdata1 = data1.replace("\r", "")

		if newdata0 != data0:
			f0= open(_dirlocal+'lese0451.dat', "w", newline="")
			f0.write(newdata0)
			f0.close()

		if newdata1 != data1:
			f1 = open(_dirlocal+'lese0452.dat', "w", newline="")
			f1.write(newdata1)
			f1.close()

		#ejecutar envío según configuración
		_bftpexport=False
		if _bftpexport == True:

			filenamecabecera = 'lese0451.dat'		
			filenamedetalle = 'lese0452.dat'

			#obtengo los datos de configuracion
			_urlftp = configoficina.url_ftp_export
			_userftp = configoficina.ftp_user
			_passftp = configoficina.ftp_user_password
			_dirftp = configoficina.dir_ftp_export
			_dirlocal = configoficina.path_txt_export
			print(_urlftp)
			print(_userftp)
			print(_passftp)
			print(_dirftp)
			print(_dirlocal)
			make_sure_path_exists(_dirlocal)
			#proceso de copiado de archivo al FTP
			

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
			#md5archivoenftp = getMD5FromFile(_dirlocal+filenamecabecera)			
			
			placeFile(_ftp,_dirlocal,filenamecabecera)
            
			#verifico integridad de la cabecera
			#if compararIntegridadArchivo(_ftp,_dirftp,_dirlocal, filenamecabecera):
			#	_log.info('Archivo cabcera copiado correctamente')
			#else:
			#	_log.info('Archivo cabcera no se copió correctamente')
			#	generarPieLog(_log)
			#	
			#	_bfin_proceso_error = True
#
			#	_slogfinal = str(getLoggingFileData(_logfileName))
			#	cerrarLog(_log)
			#	
			#	return _slogfinal
			
			#verifico integridad detalle
			placeFile(_ftp,_dirlocal,filenamedetalle)

			#verifico integridad del detalle
			#if compararIntegridadArchivo(_ftp,_dirftp,_dirlocal, filenamedetalle):
			#	_log.info('Archivo detalle copiado correctamente')
			#else:
			#	_log.info('Archivo detalle no se copió correctamente')
			#	generarPieLog(_log)
#
			#	_bfin_proceso_error = True
#
			#	_slogfinal = str(getLoggingFileData(_logfileName))
			#	cerrarLog(_log)
			#	
			#	return _slogfinal

			

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
		




		#verifico que no haya otro proceso corriendo para la misma oficina
		try:

			_proceso_imp =  ProcesoImpExp.objects.get(oficina=id_centro,proceso=1,tipo_proceso='E')
			
				
			_log.info('Finalinzando proceso de exportación...')
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
			_proceso_imp.nombre_proceso = 'Exportación'
			_proceso_imp.descripcion_proceso = 'Exportación por archivo de texto'
			_proceso_imp.tipo_proceso = 'E'
			_proceso_imp.estado_proceso = 0
			_proceso_imp.fh_fin_proceso = datetime.datetime.today().strftime('%d/%m/%Y %H:%M')
			_proceso_imp.ejecutado_por = user.username

			_proceso_imp.save()

	




		

		#si termino todo bien finaliza el proceso
		_bfin_proceso_ok = True
		generarPieLog(_log)		
		_slogfinal = str(getLoggingFileData(_logfileName))
		cerrarLog(_log)
		
		#_slogfinal = str(getLoggingFileData(_logfileName))
		notificarFinProceso(_slogfinal,_bnotifica_error,_bfin_proceso_error,_smails_notifica_error,_bnotifica_ok,_bfin_proceso_ok,_smails_notifica_ok)
		return _slogfinal
