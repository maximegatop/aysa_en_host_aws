import sys
import codecs
#from django.db import closing 
#import connection
from django.db import connection
from contextlib import closing
from datetime import timedelta, date, datetime
from qorder.models import *
import logging
import os
import threading
import MySQLdb
from django.template import RequestContext, Context

_fileName = ""
_logfileName = ""
	
	#string del log a retornar
_slogfinal = ""
_spath_log = ""
procesoimp=''
total_lineas= ''  



def query_to_dicts(query_string, *query_args):
    print('query_string {}'.format(query_string))
    print('query_args {}'.format(query_args))
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


def generarCabeceraLog1(_log):
	_log.info('******************************************')
	_log.info('       Qorder Importación - V1.0          ')
	_log.info('Proceso iniciado: {}'.format(datetime.today().strftime('%d/%m/%Y %H:%M') ) )
	_log.info('******************************************')

def getLoggingFileData1(filename):
	_file = open( filename, 'r')
	valor=_file.readlines()
	listatext=[]
	for v in valor:
		v=v.replace('\n','')
		print (v)
		listatext.append(v)
	
	print (listatext)
	str1 = listatext
	#lines = _file.readlines(
	_file.close()
	
	return str1

def getLoggerFileName1(self,oficina):
	logfileName = '{}{}.txt'.format(datetime.today().strftime('%Y%m%d'),oficina)
	return logfileName


def generarPieLog1(_log):
	_log.info('******************************************')	
	_log.info('Proceso finalizado: {}'.format(datetime.today().strftime('%d/%m/%Y %H:%M') ) )
	_log.info('******************************************')

def cerrarLog1(_log):
	_handlers = _log.handlers[:]

	for h in _handlers:
		h.close()
		_log.removeHandler(h)



def prueba (str):
	#print('hola')

	#str = '11202 10  8 000000000000000000010000553500005595LECT 2009475   20217981  SANCHEZ M JOSE ANTONIO                                                          83643911            20167587  Quintana Roo                  4029                 CASTILLA ESQUINA                                                                                              SUERTE AMIGO                                      Villa Española                                    Grupo V                       Guadalupe                     00322488        006Badger RCDLL-15               4A011Agua                          CComercio e Industria-Cat.6 (a C41Comercio e Industria-Cat.6 (a 0000.0000000-000.0000000                                                                                                                                                                                                                                                               2016080520160806                    ' 
	res=[]
	w =[0,18,26,29,35,41,45,55,80,110,140,141,156,159,182,185,191,197,203,208,218,226,232,236,247,255,261,265,276,284,290,293,303,313,319,322,332,342,348,351,361,371,377,380,388,394,402,414,422,424,426,427] 
	for i in range(1,len(w)): 

		res.append(str[ w[i-1] : w[i]]) 
		#print('{} {} {}'.format(i,w[i-1],str[ w[i-1] : w[i]]))
	return res


#Excepcion time data '2001--' does not match format '%Y-%m-%d'
#[2017-12-13 15:46:43,292: ERROR/Worker-1] time data '2001--' does not match format '%Y-%m-%d'

	
	


#prueba()

#def insertRuta (params):
#	hoy = datetime.now().strftime("%Y")
#
#	params1=params
##	vector1=[]
##	for v in params1:
##		if v in vector:
##			vector1=v
##	n_records=len(vector1)
#	params2 = []
#	rutas=[]
#	for p in params1:
#		encontro=False
#
#		#print('p {}'.format(p))
#		#print('rutas {}'.format(rutas))
#		for ruta in rutas:
#			
#			#print('ruta {}'.format(ruta))
#			if ruta==p[0].strip(' ')+p[1].strip(' ')+p[2].strip(' ')+p[3].strip(' ')+hoy:
#				encontro=True
#							
#		if  encontro==False:
#			rutas.append(p[0].strip(' ')+p[1].strip(' ')+p[2].strip(' ')+p[3].strip(' ')+hoy)
#			params2.append(p)
#
#	n_records=len(params2)
#	#print('rutas {}'.format(rutas))
#	#print(str(len(rutas)))				
#	
#	sql='INSERT INTO qorder_ruta (idruta, rutasum_id, oficina_id, ciclo, ruta, itinerario, plan, anio, cantidad, cantidad_leido, fecha_generacion, fecha_estimada_resolucion, estado, tecnico_id, flag_asignacion_guardada, usuario_asignacion_id, fecha_hora_asignacion) VALUES{}'.format( ', '.join(['(%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s,%s)'] * n_records), ) 
#	#print(sql)
#	#print(params)
#
#	params1 = [] 
#	for v in params2: 
#		
#		#print('v {}'.format(v))
#		params1.extend([v[0].strip(' ')+v[1].strip(' ')+v[2].strip(' ')+v[3].strip(' ')+hoy,v[0].strip(' ')+v[1].strip(' ')+v[2].strip(' '),v[0].strip(' '),v[3].strip(' '),v[1].strip(' '),v[2].strip(' '),'',hoy,'0','0',v[38].strip(' '),v[39].strip(' '),'1',None,'0',None,''])
#	try:	
#		with closing(connection.cursor()) as cursor: 
#			cursor.execute(sql, params1) 
#	except Exception as e:
#		print(e)		
#
#
#def insertRutaSum(params):
#
#	params1=params
#	#print('params1 {}'.format(params1))
#	
#	params2 = []
#	rutas=[]
#	for p in params1:
#		encontro=False
#
#		#print('p {}'.format(p))
#		#print('rutas {}'.format(rutas))
#		for ruta in rutas:
#			
#			#print('ruta {}'.format(ruta))
#			if ruta==p[0].strip(' ')+p[1].strip(' ')+p[2].strip(' '):
#				encontro=True
#							
#		if  encontro==False:
#			rutas.append(p[0].strip(' ')+p[1].strip(' ')+p[2].strip(' '))
#			params2.append(p)
#
#	n_records=len(params2)
#
#	#print('rutas {}'.format(rutas))
#	#print(str(len(rutas)))
#	sql='INSERT INTO qorder_rutasum (idrutasum,oficina_id,rutasum,itinerario)VALUES {}'.format( ', '.join(['(%s,%s,%s,%s)'] * n_records),)
#	#print(sql)
#	#print(params)
#	
#	params1 = [] 
#	for v in params2: 
#		
#		#print('v {}'.format(v))
#		params1.extend([v[0].strip(' ')+v[1].strip(' ')+v[2].strip(' '),v[0].strip(' '),v[1].strip(' '),v[2].strip(' ')])
#	#print(params1)
#	try:	
#		with closing(connection.cursor()) as cursor: 
#			cursor.execute(sql, params1) 
#	except Exception as e:
#		print(e)		

def filesuministrogu(params,oficina,_log):
	try:
		oficina=str(oficina)
		params1=params
		cadena=[]
		string=""
		valorf=''
		fecha=''
		params2=[]
		dia=datetime.now()
		semana=datetime.date(dia).isocalendar()[1]
		strsemana=str(dia.year)[2:4] + str(semana)
		path='/home/aysa'+'/'+oficina+'/'+'suministrosgu.txt'
		for p in params1:
			string=str('')+'#'+oficina+'#'+p[3].strip(' ')+'#'+p[1].strip(' ')+'#'+p[2].strip(' ')+'#'+strsemana+'#'+p[0].strip(' ')+'#'+'0'+'#'+p[5].strip(' ')+'#'+''+'#'+p[7].strip(' ')+'#'+p[8].strip(' ')+'#'+p[4].strip(' ')+'#'+''+'#'+''+'#'+p[11].strip(' ')+'#'+p[13].strip(' ')+'#'+p[50].strip(' ')+'#'+str(1)+'#'+p[47].strip(' ')+'#'+p[16].strip(' ')+'#'+p[17].strip(' ')+'#'+''+'#'+''+'#'+''+'#'+''+'#'+''+'#'+''+'#'+''+'#'+str(0)+'#'+''+'#'+''+'#'+str(0)+'#'+str(0)+'#'+str(0)+'#'+''+'#'+''+'#'+''+'#'+''+'#'+''+'#'+''+'#'+''+'#'+str(0)+'#'+p[6].strip(' ')+'#'+p[9].strip(' ')+'#'+p[15].strip(' ')+'#'+p[18].strip(' ')+'#'+p[19].strip(' ')+'#'+p[20].strip(' ')+'#'+p[21].strip(' ')+'#'+p[22].strip(' ')+'#'+p[23].strip(' ')+'#'+p[24].strip(' ')+'#'+p[25].strip(' ')+'#'+p[26].strip(' ')+'#'+p[27].strip(' ')+'#'+p[28].strip(' ')+'#'+p[29].strip(' ')+'#'+p[30].strip(' ')+'#'+p[31].strip(' ')+'#'+p[32].strip(' ')+'#'+p[33].strip(' ')+'#'+p[34].strip(' ')+'#'+p[35].strip(' ')+'#'+p[36].strip(' ')+'#'+p[37].strip(' ')+'#'+p[38].strip(' ')+'#'+p[39].strip(' ')+'#'+p[40].strip(' ')+'#'+p[41].strip(' ')+'#'+p[42].strip(' ')+'#'+p[43].strip(' ')+'#'+p[44].strip(' ')+'#'+p[45].strip(' ')+'#'+p[46].strip(' ')+'#'+p[48].strip(' ')+'#'+p[49].strip(' ')+'#'+p[12].strip(' ')+'#'+p[14].strip(' ')+'#'+''+'#'+p[10].strip(' ')+'#'+str(0)+'#'+''+'#'+str(0)+'#'+''+'#'+''+'#'+str(0)+'#'+''+'#'+''+'#'+'0'+'#'+'0'+'#'+p[1].strip(' ')+'#'+p[5].strip(' ')+'#'+p[3].strip(' ')+'#'+''+'#'+''+'#'+''+'#'+''+'#'+''+'#'+''+'#'+''+'#'+str(0)+'#'+str(0)+'#'+str(0)
			valor = ''.join(str(string))
			valorf = valorf + valor.replace('(', '').replace(')', '').replace("'", '') + '\n'
		archivo = open(path, 'w')
		archivo.write(valorf)

		archivo.close()
		print('termina de escribir archivo')
		sql = "LOAD DATA LOCAL INFILE '{}' INTO TABLE qorder_suministros_gu FIELDS TERMINATED BY '#' LINES TERMINATED BY '\\n'".format(path)
		print('entra')
		print(sql)
		try:
			with closing(connection.cursor()) as cursor:
				cursor.execute(sql)

		except Exception as e:

			_log.error(e)
	#total=len(params1)
	#for p in params1:
	#	params2.extend(['0',oficina,p[3].strip(' '),p[1].strip(' '),p[2].strip(' '),strsemana,p[0].strip(' '),'0',p[5].strip(' '),'',p[7].strip(' '),p[8].strip(' '),p[4].strip(' '),'','',p[11].strip(' '),p[13].strip(' '),p[50].strip(' '),1,p[47].strip(),p[16].strip(' '),p[17].strip(' '),'','','','','','','',0,'','',0,0,0,'','','','','','','',0,p[6].strip(' '),p[9].strip(' '),p[15].strip(' '),p[18].strip(' '),p[19].strip(' '),p[20].strip(' '),p[21].strip(' '),p[22].strip(' '),p[23].strip(' '),p[24].strip(' '),p[25].strip(' '),p[26].strip(' '),p[27].strip(' '),p[28].strip(' '),p[29].strip(' '),p[30].strip(' '),p[31].strip(' '),p[32].strip(' '),p[33].strip(' '),p[34].strip(' '),p[35].strip(' '),p[36].strip(' '),p[37].strip(' '),p[38].strip(' '),p[39].strip(' '),p[40].strip(' '),p[41].strip(' '),p[42].strip(' '),p[43].strip(' '),p[44].strip(' '),p[45].strip(' '),p[46].strip(' '),p[48].strip(' '),p[49].strip(' '),p[12].strip(' '),p[14].strip(' '),'',p[10].strip(' '),0,'',0,'','',0,'','','0','0',p[1].strip(' '),p[5].strip(' '),p[3].strip(' '),'','','','','','','',0,0,0])
	#sql='INSERT INTO qorder_suministros_gu(id,COD_UNICOM, RUTA, ITINERARIO, CICLO, ANIO, SEG_REG, DIVISION, SECUENCIA, LOCALIDAD, NOMBRE_CLIENTE, DIRECCION, NRO_PUERTA, PISO, DUPLICADOR, NRO_APARTO, COD_MARCA, RUEDAS, MULTIPLICADOR, LECTURA_ANTERIOR, LECTURA_MINIMA, LECTURA_MAXIMA, DESC_CONSUMO, ACCESO_FINCA, ACCESO_PM, ESTADO_LECT, ESTADO_SUM, ESTADO_ACT, COD_TARIFA, LECTURA_ACTUAL, TIP_CONSUMO, FH_LECTURA, CONSUMO, CANT_LECT_FORZADA, NRO_LECTURISTA, COD_COLECTOR, COD_ANOMALIA_HH_1, NOTAS1, COD_ANOMALIA_HH_2, NOTAS2, COD_ANOMALIA_HH_3, NOTAS3, SECUENCIA_REAL, NRO_CLIENTE, COMPLEMENTO, CONSUMO_ESTIMADO, COD_ANOMALIA1, LECTURA1, CONSUMO1, FECHA_LECTURA1, COD_ANOMALIA2, LECTURA2, CONSUMO2, FECHA_LECTURA2, COD_ANOMALIA3, LECTURA3, CONSUMO3, FECHA_LECTURA3, COD_ANOMALIA4, LECTURA4, CONSUMO4, FECHA_LECTURA4, COD_ANOMALIA5, LECTURA5, CONSUMO5, FECHA_LECTURA5, COD_ANOMALIA6, LECTURA6, CONSUMO6, FECHA_LECTURA6, COD_RECAMBIO, LEC_MEDIDOR_RETIRADO, CONSUMO_ULTIMO_RECAMBIO, FECHA_RECAMBIO, ACUM_CONS_VARIOS_RECAMBIOS, ANIO_INSTALACION, COD_TIPO_CONEXION, TIPO_MEDIDOR, COD_DIAMETRO, CONSULTO_HISTORICOS, COD_ESTADO_CONEXION, NRO_LECTURISTA_AUDITORIA, COD_UNICOM_LECT_AUDIT, COD_COLECTOR_AUDITORIA, COD_UNICOM_COLEC_AUDIT, FH_LECTURA_AUDIT, LECTURA_ACTUAL_AUDIT, COD_ANOMALIA_HH_1_AUDIT, NOTAS1_AUDIT, GPS_LATITUD, GPS_LONGITUD, PORCION_ORIGINAL, SEC_ORIGINAL, UNIDAD_ORIGINAL, CODPOST, DCSM, DISTRITO, CIRC, SECCION, MANZANA, ORDENADO_POR, SEC_RELACIONADA, LAT, LON)VALUES{};'.format( ', '.join(['(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'] * total), )
	
	#try:
	#	with closing(connection.cursor()) as cursor:
	#		print('try')
	#		cursor.execute(sql,params2)
	#except Exception as e:
	#	_log.error(e)
	except Exception as e:

		_log.error(e)


def filesuministrores(params,oficina,_log):
	try:
		oficina=str(oficina)
		params1=params
		cadena=[]
		string=''
		valorf=''
		fecha=''
		params2=[]
		dia=datetime.now()
		semana=datetime.date(dia).isocalendar()[1]
		strsemana=str(dia.year)[2:4] + str(semana)
		path = '/home/aysa' + '/' + oficina + '/' + 'suministrosres.txt'
		for p in params1:
			string=str('')+'#'+oficina+'#'+p[3].strip(' ')+'#'+p[1].strip(' ')+'#'+p[2].strip(' ')+'#'+strsemana+'#'+p[0].strip(' ')+'#'+'0'+'#'+p[5].strip(' ')+'#'+''+'#'+p[7].strip(' ')+'#'+p[8].strip(' ')+'#'+p[4].strip(' ')+'#'+''+'#'+''+'#'+p[11].strip(' ')+'#'+p[13].strip(' ')+'#'+p[50].strip(' ')+'#'+str(1)+'#'+p[47].strip(' ')+'#'+p[16].strip(' ')+'#'+p[17].strip(' ')+'#'+''+'#'+''+'#'+''+'#'+''+'#'+''+'#'+''+'#'+''+'#'+str(0)+'#'+''+'#'+''+'#'+str(0)+'#'+str(0)+'#'+str(0)+'#'+''+'#'+''+'#'+''+'#'+''+'#'+''+'#'+''+'#'+''+'#'+str(0)+'#'+p[6].strip(' ')+'#'+p[9].strip(' ')+'#'+p[15].strip(' ')+'#'+p[18].strip(' ')+'#'+p[19].strip(' ')+'#'+p[20].strip(' ')+'#'+p[21].strip(' ')+'#'+p[22].strip(' ')+'#'+p[23].strip(' ')+'#'+p[24].strip(' ')+'#'+p[25].strip(' ')+'#'+p[26].strip(' ')+'#'+p[27].strip(' ')+'#'+p[28].strip(' ')+'#'+p[29].strip(' ')+'#'+p[30].strip(' ')+'#'+p[31].strip(' ')+'#'+p[32].strip(' ')+'#'+p[33].strip(' ')+'#'+p[34].strip(' ')+'#'+p[35].strip(' ')+'#'+p[36].strip(' ')+'#'+p[37].strip(' ')+'#'+p[38].strip(' ')+'#'+p[39].strip(' ')+'#'+p[40].strip(' ')+'#'+p[41].strip(' ')+'#'+p[42].strip(' ')+'#'+p[43].strip(' ')+'#'+p[44].strip(' ')+'#'+p[45].strip(' ')+'#'+p[46].strip(' ')+'#'+p[48].strip(' ')+'#'+p[49].strip(' ')+'#'+p[12].strip(' ')+'#'+p[14].strip(' ')+'#'+''+'#'+p[10].strip(' ')+'#'+str(0)+'#'+''+'#'+str(0)+'#'+''+'#'+''+'#'+str(0)+'#'+''+'#'+''+'#'+'0'+'#'+'0'+'#'+p[1].strip(' ')+'#'+p[5].strip(' ')+'#'+p[3].strip(' ')+'#'+''+'#'+''+'#'+''+'#'+''+'#'+''+'#'+''+'#'+''+'#'+str(0)+'#'+str(0)+'#'+str(0)
			valor = ''.join(str(string))
			valorf = valorf + valor.replace('(', '').replace(')', '').replace("'", '') + '\n'
		archivo = open(path, 'w')
		archivo.write(valorf)

		archivo.close()
		print('termina de escribir archivo')
		sql = "LOAD DATA LOCAL INFILE '{}' INTO TABLE qorder_suministros_res FIELDS TERMINATED BY '#' LINES TERMINATED BY '\\n'".format(path)
		print('entra')
		print(sql)
		try:
			with closing(connection.cursor()) as cursor:
				cursor.execute(sql)

		except Exception as e:

			_log.error(e)
		#total=len(params1)
		#for p in params1:
		#	params2.extend(['0',oficina,p[3].strip(' '),p[1].strip(' '),p[2].strip(' '),strsemana,p[0].strip(' '),'0',p[5].strip(' '),'',p[7].strip(' '),p[8].strip(' '),p[4].strip(' '),'','',p[11].strip(' '),p[13].strip(' '),p[50].strip(' '),1,p[47].strip(),p[16].strip(' '),p[17].strip(' '),'','','','','','','',0,'','',0,0,0,'','','','','','','',0,p[6].strip(' '),p[9].strip(' '),p[15].strip(' '),p[18].strip(' '),p[19].strip(' '),p[20].strip(' '),p[21].strip(' '),p[22].strip(' '),p[23].strip(' '),p[24].strip(' '),p[25].strip(' '),p[26].strip(' '),p[27].strip(' '),p[28].strip(' '),p[29].strip(' '),p[30].strip(' '),p[31].strip(' '),p[32].strip(' '),p[33].strip(' '),p[34].strip(' '),p[35].strip(' '),p[36].strip(' '),p[37].strip(' '),p[38].strip(' '),p[39].strip(' '),p[40].strip(' '),p[41].strip(' '),p[42].strip(' '),p[43].strip(' '),p[44].strip(' '),p[45].strip(' '),p[46].strip(' '),p[48].strip(' '),p[49].strip(' '),p[12].strip(' '),p[14].strip(' '),'',p[10].strip(' '),0,'',0,'','',0,'','','0','0',p[1].strip(' '),p[5].strip(' '),p[3].strip(' '),'','','','','','','',0,0,0])
		#sql='INSERT INTO qorder_suministros_res(id,COD_UNICOM, RUTA, ITINERARIO, CICLO, ANIO, SEG_REG, DIVISION, SECUENCIA, LOCALIDAD, NOMBRE_CLIENTE, DIRECCION, NRO_PUERTA, PISO, DUPLICADOR, NRO_APARTO, COD_MARCA, RUEDAS, MULTIPLICADOR, LECTURA_ANTERIOR, LECTURA_MINIMA, LECTURA_MAXIMA, DESC_CONSUMO, ACCESO_FINCA, ACCESO_PM, ESTADO_LECT, ESTADO_SUM, ESTADO_ACT, COD_TARIFA, LECTURA_ACTUAL, TIP_CONSUMO, FH_LECTURA, CONSUMO, CANT_LECT_FORZADA, NRO_LECTURISTA, COD_COLECTOR, COD_ANOMALIA_HH_1, NOTAS1, COD_ANOMALIA_HH_2, NOTAS2, COD_ANOMALIA_HH_3, NOTAS3, SECUENCIA_REAL, NRO_CLIENTE, COMPLEMENTO, CONSUMO_ESTIMADO, COD_ANOMALIA1, LECTURA1, CONSUMO1, FECHA_LECTURA1, COD_ANOMALIA2, LECTURA2, CONSUMO2, FECHA_LECTURA2, COD_ANOMALIA3, LECTURA3, CONSUMO3, FECHA_LECTURA3, COD_ANOMALIA4, LECTURA4, CONSUMO4, FECHA_LECTURA4, COD_ANOMALIA5, LECTURA5, CONSUMO5, FECHA_LECTURA5, COD_ANOMALIA6, LECTURA6, CONSUMO6, FECHA_LECTURA6, COD_RECAMBIO, LEC_MEDIDOR_RETIRADO, CONSUMO_ULTIMO_RECAMBIO, FECHA_RECAMBIO, ACUM_CONS_VARIOS_RECAMBIOS, ANIO_INSTALACION, COD_TIPO_CONEXION, TIPO_MEDIDOR, COD_DIAMETRO, CONSULTO_HISTORICOS, COD_ESTADO_CONEXION, NRO_LECTURISTA_AUDITORIA, COD_UNICOM_LECT_AUDIT, COD_COLECTOR_AUDITORIA, COD_UNICOM_COLEC_AUDIT, FH_LECTURA_AUDIT, LECTURA_ACTUAL_AUDIT, COD_ANOMALIA_HH_1_AUDIT, NOTAS1_AUDIT, GPS_LATITUD, GPS_LONGITUD, PORCION_ORIGINAL, SEC_ORIGINAL, UNIDAD_ORIGINAL, CODPOST, DCSM, DISTRITO, CIRC, SECCION, MANZANA, ORDENADO_POR, SEC_RELACIONADA, LAT, LON)VALUES{};'.format( ', '.join(['(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'] * total), )
		
		#try:
		#	with closing(connection.cursor()) as cursor:
		#		print('try')
		#		cursor.execute(sql,params2)
		#except Exception as e:
		#	_log.error(e)
	except Exception as e:

		_log.error(e)
	



def updatetables(listporcionprocesos,_log,oficina,strsemana):
	sql = "delete from qorder_suministros_res where ANIO = {} and COD_UNICOM ={} and id not in (select x.id from(select max(n.id) as id from qorder_suministros_res n where ANIO = {} and COD_UNICOM = {} group by n.SEG_REG) x)".format(strsemana,oficina,strsemana,oficina)
	try:

		with closing(connection.cursor()) as cursor:

			cursor.execute(sql)
	# row=cursor.fetchone()
	# print(row)
	except Exception as e:
		print("Error {}".format(e))

	sql = "delete from qorder_suministros_gu where ANIO = {} and COD_UNICOM ={} and id not in (select x.id from(select max(n.id) as id from qorder_suministros_gu n where ANIO = {} and COD_UNICOM = {} group by n.SEG_REG) x)".format(strsemana,oficina,strsemana,oficina)
	try:

		with closing(connection.cursor()) as cursor:

			cursor.execute(sql)
	# row=cursor.fetchone()
	# print(row)
	except Exception as e:
		print("Error {}".format(e))
	strPorciones=''


	for s in listporcionprocesos:

		if strPorciones != "":
			strPorciones += ","
		strPorciones += "'" + s + "'";

	print('strPorciones {}'.format(strPorciones))

	#Completamos los datos CODPOST, DCSM con los datos de DatosCompletos
	#sql="UPDATE qorder_suministros_gu as t1 inner join qorder_semanasgu as t2 set t1.CODPOST=t2.CODPOST,t1.DCSM=t2.DCSM,t1.DISTRITO=Substring(t2.DCSM,1,3),t1.CIRC=Substring(t2.DCSM,4,2),t1.SECCION=Substring(t2.DCSM,6,1),t1.MANZANA=Substring(t2.DCSM,7,5) where t1.DIRECCION=t2.CALLE and t1.NRO_PUERTA=t2.NROPUERT and t1.RUTA=t2.UNIDAD and t1.COD_UNICOM={}".format(oficina)

	sql="update qorder_suministros_gu as t1 inner join qorder_semanasgu as t2 on t1.DIRECCION=t2.CALLE and t1.NRO_PUERTA=t2.NROPUERT and t1.RUTA=t2.UNIDAD set t1.CODPOST=t2.CODPOST,t1.DCSM=t2.DCSM,t1.DISTRITO=Substring(t2.DCSM,1,3),t1.CIRC=Substring(t2.DCSM,4,2),t1.SECCION=Substring(t2.DCSM,6,1),t1.MANZANA=Substring(t2.DCSM,7,5) where t1.COD_UNICOM={}".format(oficina)
	print(sql)
	try:
		
		with closing(connection.cursor()) as cursor:

			cursor.execute(sql) 
			#row=cursor.fetchone()
			#print(row)
	except Exception as e:
		print ("Error {}".format(e))
	#print('1')
	#sql ="UPDATE qorder_suministros_res as t1 inner join qorder_semanasre as t2 set t1.CODPOST=t2.CODPOST,t1.DCSM=t2.DCSM,t1.DISTRITO=Substring(t2.DCSM,1,3),t1.CIRC=Substring(t2.DCSM,4,2),t1.SECCION=Substring(t2.DCSM,6,1),t1.MANZANA=Substring(t2.DCSM,7,5) where t1.DIRECCION=t2.CALLE and t1.NRO_PUERTA=t2.NROPUERT and t1.RUTA=t2.UNIDAD and t1.COD_UNICOM={}".format(oficina)

	sql="update qorder_suministros_res as t1 inner join qorder_semanasre as t2 on t1.DIRECCION=t2.CALLE and t1.NRO_PUERTA=t2.NROPUERT  and t1.RUTA=t2.UNIDAD set t1.CODPOST=t2.CODPOST,t1.DCSM=t2.DCSM,t1.DISTRITO=Substring(t2.DCSM,1,3),t1.CIRC=Substring(t2.DCSM,4,2),t1.SECCION=Substring(t2.DCSM,6,1),t1.MANZANA=Substring(t2.DCSM,7,5) where t1.COD_UNICOM={}".format(oficina)
	print(sql)
	try:
		#print(sql)
		
		with closing(connection.cursor()) as cursor:
			cursor.execute(sql) 
			#row=cursor.fetchone()
			#print(row)
	except Exception as e:
		print ("Error {}".format(e))

	#print('2')
	if strPorciones!='':


	#Hacemos los reemplazos de PORCION y UNIDAD en los de GU
		#sql ="UPDATE qorder_suministros_gu as t1 inner join qorder_suministros_res t2 ON t1.CODPOST=t2.CODPOST set t1.ITINERARIO = t2.ITINERARIO, t1.RUTA = t2.RUTA, t1.ORDENADO_POR='CODPOST',t1.SEC_RELACIONADA=t2.SECUENCIA,t1.SECUENCIA=t2.SECUENCIA where t1.ITINERARIO in({}) and t1.ITINERARIO=t1.PORCION_ORIGINAL and t1.COD_UNICOM={} and t2.COD_UNICOM={}".format(strPorciones,oficina,oficina)

		sql="update qorder_suministros_gu as t1 inner join qorder_suministros_res as t2 on t1.CODPOST=t2.CODPOST set t1.ITINERARIO = t2.ITINERARIO, t1.RUTA = t2.RUTA, t1.ORDENADO_POR='CODPOST',t1.SEC_RELACIONADA=t2.SECUENCIA,t1.SECUENCIA=t2.SECUENCIA where  t1.ITINERARIO in ({}) and t1.ITINERARIO=t1.PORCION_ORIGINAL and t1.COD_UNICOM={} and t2.COD_UNICOM={} and t1.CODPOST<>'' and t2.CODPOST<>''".format(strPorciones,oficina,oficina)

		print(sql)
		try:
			
			with closing(connection.cursor()) as cursor:
				cursor.execute(sql) 
				#row=cursor.fetchone()
		except Exception as e:
			print ("Error {}".format(e))
		#print('3')
		#Reemplazamos por calle nro cercano
		
		#sql ="UPDATE qorder_suministros_gu as t5 JOIN (SELECT t3.ITINERARIO,t3.RUTA,'CALLE',t3.SECUENCIA from qorder_suministros_res t3 INNER JOIN qorder_suministros_gu t4 ON t3.DIRECCION = t4.DIRECCION WHERE t3.COD_UNICOM={} and t4.COD_UNICOM={} and ABS( t3.NRO_PUERTA - t4.NRO_PUERTA )=( SELECT MIN( ABS( t1.NRO_PUERTA - t2.NRO_PUERTA )) FROM qorder_suministros_gu t1 INNER JOIN qorder_suministros_res t2 ON t1.DIRECCION = t2.DIRECCION WHERE t1.ITINERARIO IN({}) AND t1.DIRECCION = t4.DIRECCION AND t1.ciclo = t2.ciclo AND t1.NRO_PUERTA = t4.NRO_PUERTA AND t4.ITINERARIO = t4.PORCION_ORIGINAL  GROUP BY t1.DIRECCION, t1.NRO_PUERTA ))as t3 SET t5.ITINERARIO = t3.ITINERARIO, t5.RUTA = t3.RUTA, t5.ORDENADO_POR = 'CALLE', t5.SEC_RELACIONADA = t3.SECUENCIA, t5.SECUENCIA = t3.SECUENCIA where t5.COD_UNICOM={}".format(oficina,oficina,strPorciones,oficina)
		sql="update qorder_suministros_gu as t5 inner join (select T4.RUTA,T3.ORDENADO_POR,T3.SEG_REG,T3.COD_UNICOM,T3.CICLO,t3.direccion as 'DIR_GU',t4.direccion as 'DIR_RES',t3.NRO_PUERTA as nro_puerta_gu,t4.nro_puerta as nro_puerta_res,t3.ITINERARIO as itinerario_gu,t4.ITINERARIO as itinerario_res,t3.secuencia as secuencia_gu,t4.secuencia as secuencia_res from qorder_suministros_res t4 inner join qorder_suministros_gu t3 on t3.DIRECCION = t4.DIRECCION and t3.COD_UNICOM ={} and t4.COD_UNICOM ={} and t3.ITINERARIO in({}) and t3.ORDENADO_POR = '' and t3.ciclo = t4.ciclo and abs( t3.NRO_PUERTA - t4.NRO_PUERTA)= (select min( abs( t1.NRO_PUERTA - t2.NRO_PUERTA )) from qorder_suministros_gu t1 inner join qorder_suministros_res t2 on t1.DIRECCION = t2.DIRECCION where t1.COD_UNICOM = {} and t2.COD_UNICOM = {} and t1.ITINERARIO in ({}) and t1.ORDENADO_POR = '' and t1.DIRECCION = t3.DIRECCION and t1.ciclo = t2.ciclo and t1.NRO_PUERTA = t3.NRO_PUERTA and t3.ITINERARIO = t3.PORCION_ORIGINAL group by t1.DIRECCION , t1.NRO_PUERTA)) as t6 on T5.SEG_REG = T6.SEG_REG and t5.COD_UNICOM={} set t5.ITINERARIO = t6.itinerario_RES,t5.RUTA = t6.RUTA,t5.ORDENADO_POR = 'CALLE',t5.SEC_RELACIONADA = t6.SECUENCIA_RES,t5.SECUENCIA = t6.SECUENCIA_RES".format(oficina,oficina,strPorciones,oficina,oficina,strPorciones,oficina)
		#sql="update  qorder_suministros_gu as t5 JOIN (select t3.ITINERARIO,t3.RUTA,'CALLE',t3.SECUENCIA from qorder_suministros_gu t3 inner join qorder_suministros_res t4 on t3.DIRECCION=t4.DIRECCION and t3.COD_UNICOM={} and t4.COD_UNICOM={} and t3.ITINERARIO IN ({}) and t3.ORDENADO_POR='' and  t3.ciclo=t4.ciclo  and ABS( t3.NRO_PUERTA - t4.NRO_PUERTA)=(SELECT MIN( ABS( t1.NRO_PUERTA - t2.NRO_PUERTA )) FROM qorder_suministros_gu t1 INNER JOIN qorder_suministros_res t2 ON t1.DIRECCION = t2.DIRECCION WHERE t1.COD_UNICOM={} and t2.COD_UNICOM={} and t1.ITINERARIO IN ({})  and t1.ORDENADO_POR='' and t1.DIRECCION = t3.DIRECCION AND t1.ciclo = t2.ciclo AND t1.NRO_PUERTA = t3.NRO_PUERTA AND t3.ITINERARIO = t3.PORCION_ORIGINAL GROUP BY t1.DIRECCION , t1.NRO_PUERTA)) as t3 SET t5.ITINERARIO = t3.ITINERARIO, t5.RUTA = t3.RUTA, t5.ORDENADO_POR = 'CALLE', t5.SEC_RELACIONADA = t3.SECUENCIA, t5.SECUENCIA = t3.SECUENCIA where t5.COD_UNICOM={} and t5.ORDENADO_POR=''".format(oficina,oficina,strPorciones,oficina,oficina,strPorciones,oficina)
		#sql="update qorder_suministros_gu as t4 inner join qorder_suministros_res as  t3 on t3.DIRECCION=t4.DIRECCION set t4.ITINERARIO = t3.ITINERARIO, t4.RUTA = t3.RUTA, t4.ORDENADO_POR='CALLE',t4.SEC_RELACIONADA=t3.SECUENCIA,t4.SECUENCIA=t3.SECUENCIA where ABS(t3.NRO_PUERTA-t4.NRO_PUERTA)=(SELECT MIN(ABS(t1.NRO_PUERTA-t2.NRO_PUERTA)) FROM qorder_suministros_gu t1 inner join qorder_suministros_res t2 on t1.DIRECCION=t2.DIRECCION where t1.ITINERARIO in ({}) and t1.DIRECCION=t4.DIRECCION and t1.CICLO=t2.CICLO and t1.NRO_PUERTA=t4.NRO_PUERTA and t4.ITINERARIO=t4.PORCION_ORIGINAL and t2.COD_UNICOM={} and t1.COD_UNICOM={} GROUP BY t1.DIRECCION,t1.NRO_PUERTA) and t4.COD_UNICOM={} and t3.COD_UNICOM={}".format(strPorciones,oficina,oficina,oficina,oficina)

		print(sql)
		try:
			
			with closing(connection.cursor()) as cursor:
				cursor.execute(sql) 
				row=cursor.fetchone()
				print(row)
		except Exception as e:
	
			print ("Error {}".format(e))
		#print('4')
			#Reemplazamos por MANZANA
		#sql ="UPDATE qorder_suministros_gu as t1 inner join qorder_suministros_res as t2 ON t1.DCSM=t2.DCSM SET t1.ITINERARIO = t2.ITINERARIO, t1.RUTA = t2.RUTA, t1.ORDENADO_POR='DCSM',t1.SEC_RELACIONADA=t2.SECUENCIA ,t1.SECUENCIA=t2.SECUENCIA WHERE t1.ITINERARIO IN ({}) AND t1.ITINERARIO=t1.PORCION_ORIGINAL and t1.COD_UNICOM={} and t2.COD_UNICOM={}".format(strPorciones,oficina,oficina)

		sql="update qorder_suministros_gu t1 inner join qorder_suministros_res t2 on t1.DCSM=t2.DCSM set t1.ITINERARIO = t2.ITINERARIO, t1.RUTA = t2.RUTA, t1.ORDENADO_POR='DCSM',t1.SEC_RELACIONADA=t2.SECUENCIA ,t1.SECUENCIA=t2.SECUENCIA WHERE t1.ITINERARIO IN ({}) AND t1.ITINERARIO=t1.PORCION_ORIGINAL and t1.COD_UNICOM={} and t2.COD_UNICOM={} and t1.DCSM<>'' and t2.DCSM<>'' and t1.ORDENADO_POR=''".format(strPorciones,oficina,oficina)

		print(sql)
		try:
			
			with closing(connection.cursor()) as cursor:
				cursor.execute(sql) 
				row=cursor.fetchone()
				#print(row)
		except Exception as e:
			print ("Error {}".format(e))
		#print('5')
		# Reemplazamos por sector
		#sql ="UPDATE qorder_suministros_gu as t1 inner join qorder_suministros_res as t2 ON t1.DISTRITO=t2.DISTRITO and t1.CIRC=t2.CIRC and t1.SECCION=t2.SECCION SET t1.ITINERARIO = t2.ITINERARIO, t1.RUTA = t2.RUTA, t1.ORDENADO_POR='DCS',t1.SEC_RELACIONADA=t2.SECUENCIA,t1.SECUENCIA=t2.SECUENCIA WHERE t1.ITINERARIO IN ({}) AND t1.ITINERARIO=t1.PORCION_ORIGINAL and t1.COD_UNICOM={} and t2.COD_UNICOM={}".format(strPorciones,oficina,oficina)

		sql="update qorder_suministros_gu t1 inner join qorder_suministros_res t2 on t1.DISTRITO=t2.DISTRITO and t1.CIRC=t2.CIRC and t1.SECCION=t2.SECCION set t1.ITINERARIO = t2.ITINERARIO, t1.RUTA = t2.RUTA, t1.ORDENADO_POR='DCS',t1.SEC_RELACIONADA=t2.SECUENCIA,t1.SECUENCIA=t2.SECUENCIA where t1.ITINERARIO in ({}) and t1.ITINERARIO=t1.PORCION_ORIGINAL and t1.COD_UNICOM={} and t2.COD_UNICOM={} and t1.DISTRITO<>'' and t2.DISTRITO<>'' and t1.CIRC<>'' and t2.CIRC<>'' and t1.SECCION<>'' and t2.SECCION<>'' and t1.ORDENADO_POR='' ".format(strPorciones,oficina,oficina)

		print(sql)
		try:
			
			with closing(connection.cursor()) as cursor:
				cursor.execute(sql) 
				#row=cursor.fetchone()
				#print(row)
		except Exception as e:
			print ("Error {}".format(e))
		#print('6')
	
	
	
		#Reemplazamos por CIRCunscripcion
		sql ="UPDATE qorder_suministros_gu as t1 inner join qorder_suministros_res t2 ON t1.DISTRITO=t2.DISTRITO and t1.CIRC=t2.CIRC SET t1.ITINERARIO = t2.ITINERARIO, t1.RUTA = t2.RUTA, t1.ORDENADO_POR='DC',t1.SEC_RELACIONADA=t2.SECUENCIA,t1.SECUENCIA=t2.SECUENCIA WHERE t1.ITINERARIO IN ({}) AND t1.ITINERARIO=t1.PORCION_ORIGINAL and t1.COD_UNICOM={} and t2.COD_UNICOM={} and t1.DISTRITO<>'' and t2.DISTRITO<>'' and t1.CIRC<>'' and t2.CIRC<>'' and t1.ORDENADO_POR=''".format(strPorciones,oficina,oficina)

		print(sql)
		try:
			#print(sql)
			
			with closing(connection.cursor()) as cursor:
				cursor.execute(sql) 
				#row=cursor.fetchone()
				#print(row)
		except Exception as e:
	
			print ("Error {}".format(e))
		#print('7')
	
		# Reemplazamos por distrito
		sql ="UPDATE qorder_suministros_gu as t1 inner join qorder_suministros_res as t2 ON t1.DISTRITO=t2.DISTRITO SET t1.ITINERARIO = t2.ITINERARIO, t1.RUTA = t2.RUTA, t1.ORDENADO_POR='D',t1.SEC_RELACIONADA=0,t1.SECUENCIA=0 WHERE t1.ITINERARIO IN ({}) AND t1.ITINERARIO=t1.PORCION_ORIGINAL and t1.COD_UNICOM={} and t2.COD_UNICOM={} and t1.DISTRITO<>'' and t2.DISTRITO<>'' and t1.ORDENADO_POR=''".format(strPorciones,oficina,oficina)
		print(sql)
		try:
			#print(sql)
			
			with closing(connection.cursor()) as cursor:
				cursor.execute(sql) 
				#row=cursor.fetchone()
				#print(row)
		except Exception as e:
			print ("Error {}".format(e))
		#print('8')
		# Reemplazamos por interloc
		sql ="UPDATE qorder_suministros_gu inner join qorder_suministros_gu  as t2 ON qorder_suministros_gu.SEG_REG =t2.SEG_REG SET qorder_suministros_gu.ITINERARIO = t2.ITINERARIO, qorder_suministros_gu.RUTA = t2.RUTA, qorder_suministros_gu.ORDENADO_POR='INTERLOC',qorder_suministros_gu.SEC_RELACIONADA=t2.SECUENCIA,qorder_suministros_gu.SECUENCIA=t2.SECUENCIA WHERE qorder_suministros_gu.ITINERARIO IN ({}) AND  T2.ITINERARIO<>T2.PORCION_ORIGINAL AND qorder_suministros_gu.ITINERARIO=qorder_suministros_gu.PORCION_ORIGINAL and qorder_suministros_gu.COD_UNICOM={} and t2.COD_UNICOM={} and qorder_suministros_gu.ORDENADO_POR=''  ".format(strPorciones,oficina,oficina)
		print(sql)
		try:
			#print(sql)
			
			with closing(connection.cursor()) as cursor:
				cursor.execute(sql) 
				#row=cursor.fetchone()
				#print(row)
		except Exception as e:
			print ("Error {}".format(e))
		#print('9')
		# Volcamostodo en SUMINISTROS
		sql = 'INSERT INTO qorder_suministros (COD_UNICOM, RUTA, ITINERARIO, CICLO, ANIO, SEG_REG, DIVISION, SECUENCIA, LOCALIDAD, NOMBRE_CLIENTE, DIRECCION, NRO_PUERTA, PISO, DUPLICADOR, NRO_APARTO, COD_MARCA, RUEDAS, MULTIPLICADOR, LECTURA_ANTERIOR,\
		LECTURA_MINIMA, LECTURA_MAXIMA, DESC_CONSUMO, ACCESO_FINCA, ACCESO_PM, ESTADO_LECT, ESTADO_SUM, ESTADO_ACT, COD_TARIFA, LECTURA_ACTUAL, TIP_CONSUMO, FH_LECTURA, CONSUMO, CANT_LECT_FORZADA, NRO_LECTURISTA, COD_COLECTOR, COD_ANOMALIA_HH_1, NOTAS1,\
		COD_ANOMALIA_HH_2, NOTAS2, COD_ANOMALIA_HH_3, NOTAS3, SECUENCIA_REAL, NRO_CLIENTE, COMPLEMENTO, CONSUMO_ESTIMADO, COD_ANOMALIA1, LECTURA1, CONSUMO1, FECHA_LECTURA1, COD_ANOMALIA2, LECTURA2, CONSUMO2, FECHA_LECTURA2, COD_ANOMALIA3, LECTURA3, CONSUMO3,\
		FECHA_LECTURA3, COD_ANOMALIA4, LECTURA4, CONSUMO4, FECHA_LECTURA4, COD_ANOMALIA5, LECTURA5, CONSUMO5, FECHA_LECTURA5, COD_ANOMALIA6, LECTURA6, CONSUMO6, FECHA_LECTURA6, COD_RECAMBIO, LEC_MEDIDOR_RETIRADO, CONSUMO_ULTIMO_RECAMBIO, FECHA_RECAMBIO,\
		ACUM_CONS_VARIOS_RECAMBIOS, ANIO_INSTALACION, COD_TIPO_CONEXION, TIPO_MEDIDOR, COD_DIAMETRO, CONSULTO_HISTORICOS, COD_ESTADO_CONEXION, NRO_LECTURISTA_AUDITORIA, COD_UNICOM_LECT_AUDIT, COD_COLECTOR_AUDITORIA, COD_UNICOM_COLEC_AUDIT, FH_LECTURA_AUDIT, \
		LECTURA_ACTUAL_AUDIT, COD_ANOMALIA_HH_1_AUDIT, NOTAS1_AUDIT, GPS_LATITUD, GPS_LONGITUD, PORCION_ORIGINAL, SEC_ORIGINAL, UNIDAD_ORIGINAL, CODPOST, DCSM, DISTRITO, CIRC, SECCION, MANZANA, ORDENADO_POR, SEC_RELACIONADA, LAT, LON) SELECT COD_UNICOM, RUTA, \
		ITINERARIO, CICLO, ANIO, SEG_REG, DIVISION, SECUENCIA, LOCALIDAD, NOMBRE_CLIENTE, DIRECCION, NRO_PUERTA, PISO, DUPLICADOR, NRO_APARTO, COD_MARCA, RUEDAS, MULTIPLICADOR, LECTURA_ANTERIOR, LECTURA_MINIMA, LECTURA_MAXIMA, DESC_CONSUMO, ACCESO_FINCA, ACCESO_PM,\
		ESTADO_LECT, ESTADO_SUM, ESTADO_ACT, COD_TARIFA, LECTURA_ACTUAL, TIP_CONSUMO, FH_LECTURA, CONSUMO, CANT_LECT_FORZADA, NRO_LECTURISTA, COD_COLECTOR, COD_ANOMALIA_HH_1, NOTAS1, COD_ANOMALIA_HH_2, NOTAS2, COD_ANOMALIA_HH_3, NOTAS3, SECUENCIA_REAL, NRO_CLIENTE, \
		COMPLEMENTO, CONSUMO_ESTIMADO, COD_ANOMALIA1, LECTURA1, CONSUMO1, FECHA_LECTURA1, COD_ANOMALIA2, LECTURA2, CONSUMO2, FECHA_LECTURA2, COD_ANOMALIA3, LECTURA3, CONSUMO3, FECHA_LECTURA3, COD_ANOMALIA4, LECTURA4, CONSUMO4, FECHA_LECTURA4, COD_ANOMALIA5, LECTURA5, \
		CONSUMO5, FECHA_LECTURA5, COD_ANOMALIA6, LECTURA6, CONSUMO6, FECHA_LECTURA6, COD_RECAMBIO, LEC_MEDIDOR_RETIRADO, CONSUMO_ULTIMO_RECAMBIO, FECHA_RECAMBIO, ACUM_CONS_VARIOS_RECAMBIOS, ANIO_INSTALACION, COD_TIPO_CONEXION, TIPO_MEDIDOR, COD_DIAMETRO, CONSULTO_HISTORICOS,\
		COD_ESTADO_CONEXION, NRO_LECTURISTA_AUDITORIA, COD_UNICOM_LECT_AUDIT, COD_COLECTOR_AUDITORIA, COD_UNICOM_COLEC_AUDIT, FH_LECTURA_AUDIT, LECTURA_ACTUAL_AUDIT, COD_ANOMALIA_HH_1_AUDIT, NOTAS1_AUDIT, GPS_LATITUD, GPS_LONGITUD, PORCION_ORIGINAL, SEC_ORIGINAL, UNIDAD_ORIGINAL,\
		CODPOST, DCSM, DISTRITO, CIRC, SECCION, MANZANA, ORDENADO_POR, SEC_RELACIONADA, LAT, LON FROM qorder_suministros_res where COD_UNICOM={}'.format(oficina)
		print(sql)
		try:
			
			with closing(connection.cursor()) as cursor:
				cursor.execute(sql) 
	
		except Exception as e:
			print ("Error {}".format(e))
		#print('10')
	
		sql = 'INSERT INTO qorder_suministros (COD_UNICOM, RUTA, ITINERARIO, CICLO, ANIO, SEG_REG, DIVISION, SECUENCIA, LOCALIDAD, NOMBRE_CLIENTE, DIRECCION, NRO_PUERTA, PISO, DUPLICADOR, NRO_APARTO, COD_MARCA, RUEDAS, MULTIPLICADOR, LECTURA_ANTERIOR, LECTURA_MINIMA, LECTURA_MAXIMA, DESC_CONSUMO, ACCESO_FINCA, ACCESO_PM, ESTADO_LECT, ESTADO_SUM, ESTADO_ACT, COD_TARIFA, \
			LECTURA_ACTUAL, TIP_CONSUMO, FH_LECTURA, CONSUMO, CANT_LECT_FORZADA, NRO_LECTURISTA, COD_COLECTOR, COD_ANOMALIA_HH_1, NOTAS1, COD_ANOMALIA_HH_2, NOTAS2, COD_ANOMALIA_HH_3, NOTAS3, SECUENCIA_REAL, NRO_CLIENTE, COMPLEMENTO, CONSUMO_ESTIMADO, COD_ANOMALIA1, LECTURA1, CONSUMO1, FECHA_LECTURA1, COD_ANOMALIA2, LECTURA2, CONSUMO2, FECHA_LECTURA2, COD_ANOMALIA3, LECTURA3, \
			CONSUMO3, FECHA_LECTURA3, COD_ANOMALIA4, LECTURA4, CONSUMO4, FECHA_LECTURA4, COD_ANOMALIA5, LECTURA5, CONSUMO5, FECHA_LECTURA5, COD_ANOMALIA6, LECTURA6, CONSUMO6, FECHA_LECTURA6, COD_RECAMBIO, LEC_MEDIDOR_RETIRADO, CONSUMO_ULTIMO_RECAMBIO, FECHA_RECAMBIO, ACUM_CONS_VARIOS_RECAMBIOS, ANIO_INSTALACION, COD_TIPO_CONEXION, TIPO_MEDIDOR, COD_DIAMETRO, CONSULTO_HISTORICOS,\
			COD_ESTADO_CONEXION, NRO_LECTURISTA_AUDITORIA, COD_UNICOM_LECT_AUDIT, COD_COLECTOR_AUDITORIA, COD_UNICOM_COLEC_AUDIT, FH_LECTURA_AUDIT, LECTURA_ACTUAL_AUDIT, COD_ANOMALIA_HH_1_AUDIT, NOTAS1_AUDIT, GPS_LATITUD, GPS_LONGITUD, PORCION_ORIGINAL, SEC_ORIGINAL, UNIDAD_ORIGINAL, CODPOST, DCSM, DISTRITO, CIRC, SECCION, MANZANA, ORDENADO_POR, SEC_RELACIONADA, LAT, LON) \
			SELECT COD_UNICOM, RUTA, ITINERARIO, CICLO, ANIO, SEG_REG, DIVISION, SECUENCIA, LOCALIDAD, NOMBRE_CLIENTE, DIRECCION, NRO_PUERTA, PISO, DUPLICADOR, NRO_APARTO, COD_MARCA, RUEDAS, MULTIPLICADOR, LECTURA_ANTERIOR, LECTURA_MINIMA, LECTURA_MAXIMA, DESC_CONSUMO, ACCESO_FINCA, ACCESO_PM, ESTADO_LECT, ESTADO_SUM, ESTADO_ACT, COD_TARIFA, LECTURA_ACTUAL, TIP_CONSUMO, FH_LECTURA,\
			CONSUMO, CANT_LECT_FORZADA, NRO_LECTURISTA, COD_COLECTOR, COD_ANOMALIA_HH_1, NOTAS1, COD_ANOMALIA_HH_2, NOTAS2, COD_ANOMALIA_HH_3, NOTAS3, SECUENCIA_REAL, NRO_CLIENTE, COMPLEMENTO, CONSUMO_ESTIMADO, COD_ANOMALIA1, LECTURA1, CONSUMO1, FECHA_LECTURA1, COD_ANOMALIA2, LECTURA2, CONSUMO2, FECHA_LECTURA2, COD_ANOMALIA3, LECTURA3, CONSUMO3, FECHA_LECTURA3, COD_ANOMALIA4, LECTURA4,\
			CONSUMO4, FECHA_LECTURA4, COD_ANOMALIA5, LECTURA5, CONSUMO5, FECHA_LECTURA5, COD_ANOMALIA6, LECTURA6, CONSUMO6, FECHA_LECTURA6, COD_RECAMBIO, LEC_MEDIDOR_RETIRADO, CONSUMO_ULTIMO_RECAMBIO, FECHA_RECAMBIO, ACUM_CONS_VARIOS_RECAMBIOS, ANIO_INSTALACION, COD_TIPO_CONEXION, TIPO_MEDIDOR, COD_DIAMETRO, CONSULTO_HISTORICOS, COD_ESTADO_CONEXION, NRO_LECTURISTA_AUDITORIA, COD_UNICOM_LECT_AUDIT,\
			COD_COLECTOR_AUDITORIA, COD_UNICOM_COLEC_AUDIT, FH_LECTURA_AUDIT, LECTURA_ACTUAL_AUDIT, COD_ANOMALIA_HH_1_AUDIT, NOTAS1_AUDIT, GPS_LATITUD, GPS_LONGITUD, PORCION_ORIGINAL, SEC_ORIGINAL, UNIDAD_ORIGINAL, CODPOST, DCSM, DISTRITO, CIRC, SECCION, MANZANA, ORDENADO_POR, SEC_RELACIONADA, LAT, LON FROM qorder_suministros_gu where COD_UNICOM={}'.format(oficina)
		print(sql)
		try:
			
			with closing(connection.cursor()) as cursor:
				cursor.execute(sql) 
	
		except Exception as e:
			print ("Error {}".format(e))
		#print('11')


	else:
		# Volcamos todo en SUMINISTROS
		sql = 'INSERT INTO qorder_suministros (COD_UNICOM, RUTA, ITINERARIO, CICLO, ANIO, SEG_REG, DIVISION, SECUENCIA, LOCALIDAD, NOMBRE_CLIENTE, DIRECCION, NRO_PUERTA, PISO, DUPLICADOR, NRO_APARTO, COD_MARCA, RUEDAS, MULTIPLICADOR, LECTURA_ANTERIOR,\
		LECTURA_MINIMA, LECTURA_MAXIMA, DESC_CONSUMO, ACCESO_FINCA, ACCESO_PM, ESTADO_LECT, ESTADO_SUM, ESTADO_ACT, COD_TARIFA, LECTURA_ACTUAL, TIP_CONSUMO, FH_LECTURA, CONSUMO, CANT_LECT_FORZADA, NRO_LECTURISTA, COD_COLECTOR, COD_ANOMALIA_HH_1, NOTAS1,\
		COD_ANOMALIA_HH_2, NOTAS2, COD_ANOMALIA_HH_3, NOTAS3, SECUENCIA_REAL, NRO_CLIENTE, COMPLEMENTO, CONSUMO_ESTIMADO, COD_ANOMALIA1, LECTURA1, CONSUMO1, FECHA_LECTURA1, COD_ANOMALIA2, LECTURA2, CONSUMO2, FECHA_LECTURA2, COD_ANOMALIA3, LECTURA3, CONSUMO3,\
		FECHA_LECTURA3, COD_ANOMALIA4, LECTURA4, CONSUMO4, FECHA_LECTURA4, COD_ANOMALIA5, LECTURA5, CONSUMO5, FECHA_LECTURA5, COD_ANOMALIA6, LECTURA6, CONSUMO6, FECHA_LECTURA6, COD_RECAMBIO, LEC_MEDIDOR_RETIRADO, CONSUMO_ULTIMO_RECAMBIO, FECHA_RECAMBIO,\
		ACUM_CONS_VARIOS_RECAMBIOS, ANIO_INSTALACION, COD_TIPO_CONEXION, TIPO_MEDIDOR, COD_DIAMETRO, CONSULTO_HISTORICOS, COD_ESTADO_CONEXION, NRO_LECTURISTA_AUDITORIA, COD_UNICOM_LECT_AUDIT, COD_COLECTOR_AUDITORIA, COD_UNICOM_COLEC_AUDIT, FH_LECTURA_AUDIT, \
		LECTURA_ACTUAL_AUDIT, COD_ANOMALIA_HH_1_AUDIT, NOTAS1_AUDIT, GPS_LATITUD, GPS_LONGITUD, PORCION_ORIGINAL, SEC_ORIGINAL, UNIDAD_ORIGINAL, CODPOST, DCSM, DISTRITO, CIRC, SECCION, MANZANA, ORDENADO_POR, SEC_RELACIONADA, LAT, LON) SELECT COD_UNICOM, RUTA, \
		ITINERARIO, CICLO, ANIO, SEG_REG, DIVISION, SECUENCIA, LOCALIDAD, NOMBRE_CLIENTE, DIRECCION, NRO_PUERTA, PISO, DUPLICADOR, NRO_APARTO, COD_MARCA, RUEDAS, MULTIPLICADOR, LECTURA_ANTERIOR, LECTURA_MINIMA, LECTURA_MAXIMA, DESC_CONSUMO, ACCESO_FINCA, ACCESO_PM,\
		ESTADO_LECT, ESTADO_SUM, ESTADO_ACT, COD_TARIFA, LECTURA_ACTUAL, TIP_CONSUMO, FH_LECTURA, CONSUMO, CANT_LECT_FORZADA, NRO_LECTURISTA, COD_COLECTOR, COD_ANOMALIA_HH_1, NOTAS1, COD_ANOMALIA_HH_2, NOTAS2, COD_ANOMALIA_HH_3, NOTAS3, SECUENCIA_REAL, NRO_CLIENTE, \
		COMPLEMENTO, CONSUMO_ESTIMADO, COD_ANOMALIA1, LECTURA1, CONSUMO1, FECHA_LECTURA1, COD_ANOMALIA2, LECTURA2, CONSUMO2, FECHA_LECTURA2, COD_ANOMALIA3, LECTURA3, CONSUMO3, FECHA_LECTURA3, COD_ANOMALIA4, LECTURA4, CONSUMO4, FECHA_LECTURA4, COD_ANOMALIA5, LECTURA5, \
		CONSUMO5, FECHA_LECTURA5, COD_ANOMALIA6, LECTURA6, CONSUMO6, FECHA_LECTURA6, COD_RECAMBIO, LEC_MEDIDOR_RETIRADO, CONSUMO_ULTIMO_RECAMBIO, FECHA_RECAMBIO, ACUM_CONS_VARIOS_RECAMBIOS, ANIO_INSTALACION, COD_TIPO_CONEXION, TIPO_MEDIDOR, COD_DIAMETRO, CONSULTO_HISTORICOS,\
		COD_ESTADO_CONEXION, NRO_LECTURISTA_AUDITORIA, COD_UNICOM_LECT_AUDIT, COD_COLECTOR_AUDITORIA, COD_UNICOM_COLEC_AUDIT, FH_LECTURA_AUDIT, LECTURA_ACTUAL_AUDIT, COD_ANOMALIA_HH_1_AUDIT, NOTAS1_AUDIT, GPS_LATITUD, GPS_LONGITUD, PORCION_ORIGINAL, SEC_ORIGINAL, UNIDAD_ORIGINAL,\
		CODPOST, DCSM, DISTRITO, CIRC, SECCION, MANZANA, ORDENADO_POR, SEC_RELACIONADA, LAT, LON FROM qorder_suministros_res where COD_UNICOM={}'.format(oficina)
		print(sql)
		try:
			
			with closing(connection.cursor()) as cursor:
				cursor.execute(sql) 
	
		except Exception as e:
			print ("Error {}".format(e))
		#print('10')
	
		sql = 'INSERT INTO qorder_suministros (COD_UNICOM, RUTA, ITINERARIO, CICLO, ANIO, SEG_REG, DIVISION, SECUENCIA, LOCALIDAD, NOMBRE_CLIENTE, DIRECCION, NRO_PUERTA, PISO, DUPLICADOR, NRO_APARTO, COD_MARCA, RUEDAS, MULTIPLICADOR, LECTURA_ANTERIOR, LECTURA_MINIMA, LECTURA_MAXIMA, DESC_CONSUMO, ACCESO_FINCA, ACCESO_PM, ESTADO_LECT, ESTADO_SUM, ESTADO_ACT, COD_TARIFA, \
			LECTURA_ACTUAL, TIP_CONSUMO, FH_LECTURA, CONSUMO, CANT_LECT_FORZADA, NRO_LECTURISTA, COD_COLECTOR, COD_ANOMALIA_HH_1, NOTAS1, COD_ANOMALIA_HH_2, NOTAS2, COD_ANOMALIA_HH_3, NOTAS3, SECUENCIA_REAL, NRO_CLIENTE, COMPLEMENTO, CONSUMO_ESTIMADO, COD_ANOMALIA1, LECTURA1, CONSUMO1, FECHA_LECTURA1, COD_ANOMALIA2, LECTURA2, CONSUMO2, FECHA_LECTURA2, COD_ANOMALIA3, LECTURA3, \
			CONSUMO3, FECHA_LECTURA3, COD_ANOMALIA4, LECTURA4, CONSUMO4, FECHA_LECTURA4, COD_ANOMALIA5, LECTURA5, CONSUMO5, FECHA_LECTURA5, COD_ANOMALIA6, LECTURA6, CONSUMO6, FECHA_LECTURA6, COD_RECAMBIO, LEC_MEDIDOR_RETIRADO, CONSUMO_ULTIMO_RECAMBIO, FECHA_RECAMBIO, ACUM_CONS_VARIOS_RECAMBIOS, ANIO_INSTALACION, COD_TIPO_CONEXION, TIPO_MEDIDOR, COD_DIAMETRO, CONSULTO_HISTORICOS,\
			COD_ESTADO_CONEXION, NRO_LECTURISTA_AUDITORIA, COD_UNICOM_LECT_AUDIT, COD_COLECTOR_AUDITORIA, COD_UNICOM_COLEC_AUDIT, FH_LECTURA_AUDIT, LECTURA_ACTUAL_AUDIT, COD_ANOMALIA_HH_1_AUDIT, NOTAS1_AUDIT, GPS_LATITUD, GPS_LONGITUD, PORCION_ORIGINAL, SEC_ORIGINAL, UNIDAD_ORIGINAL, CODPOST, DCSM, DISTRITO, CIRC, SECCION, MANZANA, ORDENADO_POR, SEC_RELACIONADA, LAT, LON) \
			SELECT COD_UNICOM, RUTA, ITINERARIO, CICLO, ANIO, SEG_REG, DIVISION, SECUENCIA, LOCALIDAD, NOMBRE_CLIENTE, DIRECCION, NRO_PUERTA, PISO, DUPLICADOR, NRO_APARTO, COD_MARCA, RUEDAS, MULTIPLICADOR, LECTURA_ANTERIOR, LECTURA_MINIMA, LECTURA_MAXIMA, DESC_CONSUMO, ACCESO_FINCA, ACCESO_PM, ESTADO_LECT, ESTADO_SUM, ESTADO_ACT, COD_TARIFA, LECTURA_ACTUAL, TIP_CONSUMO, FH_LECTURA,\
			CONSUMO, CANT_LECT_FORZADA, NRO_LECTURISTA, COD_COLECTOR, COD_ANOMALIA_HH_1, NOTAS1, COD_ANOMALIA_HH_2, NOTAS2, COD_ANOMALIA_HH_3, NOTAS3, SECUENCIA_REAL, NRO_CLIENTE, COMPLEMENTO, CONSUMO_ESTIMADO, COD_ANOMALIA1, LECTURA1, CONSUMO1, FECHA_LECTURA1, COD_ANOMALIA2, LECTURA2, CONSUMO2, FECHA_LECTURA2, COD_ANOMALIA3, LECTURA3, CONSUMO3, FECHA_LECTURA3, COD_ANOMALIA4, LECTURA4,\
			CONSUMO4, FECHA_LECTURA4, COD_ANOMALIA5, LECTURA5, CONSUMO5, FECHA_LECTURA5, COD_ANOMALIA6, LECTURA6, CONSUMO6, FECHA_LECTURA6, COD_RECAMBIO, LEC_MEDIDOR_RETIRADO, CONSUMO_ULTIMO_RECAMBIO, FECHA_RECAMBIO, ACUM_CONS_VARIOS_RECAMBIOS, ANIO_INSTALACION, COD_TIPO_CONEXION, TIPO_MEDIDOR, COD_DIAMETRO, CONSULTO_HISTORICOS, COD_ESTADO_CONEXION, NRO_LECTURISTA_AUDITORIA, COD_UNICOM_LECT_AUDIT,\
			COD_COLECTOR_AUDITORIA, COD_UNICOM_COLEC_AUDIT, FH_LECTURA_AUDIT, LECTURA_ACTUAL_AUDIT, COD_ANOMALIA_HH_1_AUDIT, NOTAS1_AUDIT, GPS_LATITUD, GPS_LONGITUD, PORCION_ORIGINAL, SEC_ORIGINAL, UNIDAD_ORIGINAL, CODPOST, DCSM, DISTRITO, CIRC, SECCION, MANZANA, ORDENADO_POR, SEC_RELACIONADA, LAT, LON FROM qorder_suministros_gu where COD_UNICOM={}'.format(oficina)
		print(sql)
		try:
			
			with closing(connection.cursor()) as cursor:
				cursor.execute(sql) 
	
		except Exception as e:
			print ("Error {}".format(e))

		#print('11')

# Actualizar aca la tabla Suministros , con la tabla reubicación de suministros GU 




def insertDatosSuministro(_log,oficina):
	dia=datetime.now()
	semana=datetime.date(dia).isocalendar()[1]
	strsemana=str(dia.year)[2:4] + str(semana)
	sql="INSERT INTO qorder_puntodesuministro (num_contrato, punto_suministro, gps_latitud, gps_longitud, ref_finca, ref_direccion, ref_suministro, nif, estado_suministro, calle, numero_puerta, piso, duplicador, localidad, municipio, barrio, departamento, codigo_postal, hashdata, aparato_id, cliente_id, rutasum_id, tarifa_id, tipo_asociacion_id, tipo_servicio_id, secuencia_teorica, fecha_actualizacion_secuencia, secuencia_anterior)\
	select NRO_CLIENTE,SEG_REG,GPS_LATITUD,GPS_LONGITUD,ACCESO_FINCA,'',ACCESO_PM,'',1,DIRECCION,NRO_PUERTA,PISO,DUPLICADOR,LOCALIDAD,'','','',CODPOST,'',concat(COD_MARCA,NRO_APARTO),NRO_CLIENTE,concat(COD_UNICOM,RUTA,ITINERARIO),null,null,1,SECUENCIA,null,0 from qorder_suministros where COD_UNICOM='{}' and ANIO='{}'\
	ON DUPLICATE KEY UPDATE num_contrato=VALUES(num_contrato),gps_latitud=VALUES(gps_latitud),gps_longitud=VALUES(gps_longitud),ref_finca=VALUES(ref_finca),ref_direccion=VALUES(ref_direccion),ref_suministro=VALUES(ref_suministro),nif=VALUES(nif),estado_suministro=VALUES(estado_suministro),calle=VALUES(calle),numero_puerta=VALUES(numero_puerta),piso=VALUES(piso),duplicador=VALUES(duplicador),localidad=VALUES(localidad),municipio=VALUES(municipio),barrio=VALUES(barrio),departamento=VALUES(departamento),codigo_postal=VALUES(codigo_postal),hashdata=VALUES(hashdata),aparato_id=VALUES(aparato_id),cliente_id=VALUES(cliente_id),rutasum_id=VALUES(rutasum_id),tarifa_id=VALUES(tarifa_id),tipo_asociacion_id=VALUES(tipo_asociacion_id),tipo_servicio_id=VALUES(tipo_servicio_id),municipio=VALUES(municipio),barrio=VALUES(barrio),departamento=VALUES(departamento),codigo_postal=VALUES(codigo_postal),hashdata=VALUES(hashdata),secuencia_teorica=VALUES(secuencia_teorica),fecha_actualizacion_secuencia=VALUES(fecha_actualizacion_secuencia),secuencia_anterior=VALUES(secuencia_anterior)".format(oficina,strsemana)
	try: 
		with closing(connection.cursor()) as cursor: 
			cursor.execute(sql)

	except Exception as e:
		print ("Error {}".format(e))




	print('pasa')
def insertAparatosSuministro(_log,oficina):
	dia=datetime.now()
	semana=datetime.date(dia).isocalendar()[1]
	strsemana=str(dia.year)[2:4] + str(semana)
	sql="INSERT INTO qorder_aparato\
	(aparato, num_serie, num_ruedas, estado_aparato, fecha_fabricacion, fecha_instalacion, fecha_proxima_calibracion, diametro, presion, coef_perdida, marca_id, tipo_aparato_id, tipo_fase_id, tipo_intensidad_id, tipo_tension_id)\
	select concat(COD_MARCA,NRO_APARTO),NRO_APARTO,RUEDAS,'',null,null,null,'','',0,COD_MARCA,null,1,1,1 from qorder_suministros where ANIO='{}' and COD_UNICOM='{}'\
	ON DUPLICATE KEY UPDATE num_serie=VALUES(num_serie),num_ruedas=VALUES(num_ruedas),estado_aparato=VALUES(estado_aparato),fecha_fabricacion=VALUES(fecha_fabricacion),fecha_instalacion=VALUES(fecha_instalacion),fecha_proxima_calibracion=VALUES(fecha_proxima_calibracion),diametro=VALUES(diametro),presion=VALUES(presion),coef_perdida=VALUES(coef_perdida)".format(strsemana,oficina)

	#print(p[10])
	#print('llego')
	try: 
		#print('aca')
		with closing(connection.cursor()) as cursor: 
			cursor.execute(sql)
	except Exception as e:
		_log.error(e)

	print('pasa1')

def insertAparatoConsumo(_log,oficina):
	dia=datetime.now()
	semana=datetime.date(dia).isocalendar()[1]
	strsemana=str(dia.year)[2:4] + str(semana)
	sql="INSERT INTO qorder_consumo (consumo, constante, lectura_anterior, consumo_anterior, fecha_lectura_anterior, tope_lectura_maxima, tope_lectura_minima, aparato_id, tipo_consumo_id) \
	select concat(COD_MARCA,NRO_APARTO,'CO011'),1,LECTURA_ANTERIOR,CONSUMO1,FECHA_LECTURA1,LECTURA_MAXIMA,LECTURA_MINIMA,concat(COD_MARCA,NRO_APARTO),'CO011' from qorder_suministros where ANIO='{}' and COD_UNICOM='{}'\
 	ON DUPLICATE KEY UPDATE constante=VALUES(constante),lectura_anterior=VALUES(lectura_anterior),consumo_anterior=VALUES(consumo_anterior),fecha_lectura_anterior=VALUES(fecha_lectura_anterior),tope_lectura_maxima=VALUES(tope_lectura_maxima),tope_lectura_minima=VALUES(tope_lectura_minima),aparato_id=VALUES(aparato_id),tipo_consumo_id=VALUES(tipo_consumo_id)".format(strsemana,oficina)
	try:

		with closing(connection.cursor()) as cursor: 
			cursor.execute(sql) 
	except Exception as e:

		print ("Error {}".format(e))

def insertCliente(_log,oficina):
	dia=datetime.now()
	semana=datetime.date(dia).isocalendar()[1]
	strsemana=str(dia.year)[2:4] + str(semana)
	sql="INSERT INTO qorder_cliente (codigo, nombre, apellido_1, apellido_2, calle, numero_puerta, piso, duplicador, localidad, municipio, barrio, departamento, codigo_postal, estado_cliente, fecha_alta, observacion)select NRO_CLIENTE,'',NOMBRE_CLIENTE,'',DIRECCION,NRO_PUERTA,PISO,DUPLICADOR,LOCALIDAD,\
	'','','',CODPOST,1,'','' from qorder_suministros where ANIO='{}' and COD_UNICOM='{}' ON DUPLICATE KEY UPDATE nombre=VALUES(nombre),apellido_1=VALUES(apellido_1),apellido_2=VALUES(apellido_2),calle=VALUES(calle),numero_puerta=VALUES(numero_puerta),piso=VALUES(piso),duplicador=VALUES(duplicador),localidad=VALUES(localidad),municipio=VALUES(municipio),barrio=VALUES(barrio),departamento=VALUES(departamento),codigo_postal=VALUES(codigo_postal),estado_cliente=VALUES(estado_cliente),fecha_alta=VALUES(fecha_alta),observacion=VALUES(observacion)".format(strsemana,oficina)
	#print('cont1 {}'.format(cont))
	#print(params)
			#print('params1 {}'.format(carga))	
	try: 
		#print('aca')
		with closing(connection.cursor()) as cursor: 
			cursor.execute(sql) 

	except Exception as e:

		_log.error(e)

	print('pasa3')
	clientes=Cliente.objects.filter(codigo='')
	clientes.delete()

def insertrutasum(_log,oficina):
	dia=datetime.now()
	semana=datetime.date(dia).isocalendar()[1]
	strsemana=str(dia.year)[2:4] + str(semana)
	sql="INSERT INTO qorder_rutasum(idrutasum, rutasum, itinerario, oficina_id, Frecuencia)\
	select concat(COD_UNICOM,RUTA,ITINERARIO),RUTA,ITINERARIO,COD_UNICOM,null from qorder_suministros where COD_UNICOM='{}' and ANIO='{}' ON DUPLICATE KEY UPDATE rutasum=VALUES(rutasum),itinerario=VALUES(itinerario)".format(oficina,strsemana)

	try:
	#print('aca')
		with closing(connection.cursor()) as cursor: 
			cursor.execute(sql) 

	except Exception as e:
			_log.error(e)
	print('pasa4')		

def insertruta(_log,oficina,user):
	dia=datetime.now()
	semana=datetime.date(dia).isocalendar()[1]
	strsemana=str(dia.year)[2:4] + str(semana)
	suministros=[]
	fechaimp=datetime.now().strftime('%Y%m%d%H%M%S')
	fer =datetime.today().strftime('%Y-%m-%d')

	suministros=list(query_to_dicts("select distinct cod_unicom,ruta,itinerario,ciclo,anio,COUNT(*)as cant from qorder_suministros where cod_unicom='{}' and anio='{}' group by cod_unicom,ruta,itinerario,ciclo,anio ORDER BY itinerario,ruta;".format(oficina,strsemana)))
	for s in suministros:
		cod_unicom=''
		ruta=''
		itinerario=''
		ciclo=''
		anio=''
		cant=''
		#print(s)
		lista=''.join(s)
		#print(lista)
		cod_unicom=''.join(s['cod_unicom'])
		#print(cod_unicom)
		ruta=''.join(s['ruta'])
		itinerario=''.join(s['itinerario'])
		ciclo=''.join(s['ciclo'])
		anio=''.join(s['anio'])
		cant=''.join(str(s['cant']))
		sql="INSERT into qorder_ruta(idruta, ciclo, ruta, itinerario, plan, anio, cantidad, cantidad_leido, fecha_generacion, fecha_estimada_resolucion, estado, flag_asignacion_guardada, fecha_hora_asignacion, oficina_id, rutasum_id, tecnico_id, usuario_asignacion_id, fecha_hora_exportacion, fecha_hora_importacion)\
		VALUES(%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s)ON DUPLICATE KEY UPDATE ciclo=VALUES(ciclo),ruta=VALUES(ruta),itinerario=VALUES(itinerario),plan=VALUES(plan),anio=VALUES(anio),cantidad=VALUES(cantidad),cantidad_leido=VALUES(cantidad_leido),fecha_generacion=VALUES(fecha_generacion),\
		fecha_estimada_resolucion=VALUES(fecha_estimada_resolucion),estado=VALUES(estado),flag_asignacion_guardada=VALUES(flag_asignacion_guardada),fecha_hora_exportacion=VALUES(fecha_hora_exportacion),fecha_hora_importacion=VALUES(fecha_hora_importacion)"
		args=(cod_unicom+ruta+itinerario.zfill(5)+ciclo+anio.zfill(4),ciclo,ruta,itinerario,'',anio,cant,0,str(fer),fer,1,0,None,cod_unicom,cod_unicom+ruta+itinerario,None,None,None,fechaimp)


		try: 
		#print('aca')
			with closing(connection.cursor()) as cursor: 
				cursor.execute(sql,args) 
				log_rutas.objects.create(estado='Importación',fecha_log=datetime.now(),observacion='ruta generada',ruta_id=cod_unicom+ruta+itinerario.zfill(5)+ciclo+anio.zfill(4),usuario=user)
		except Exception as e:

			_log.error(e)

	print('pasa5')			


def insertorden(_log,oficina):
	dia=datetime.now()
	semana=datetime.date(dia).isocalendar()[1]
	strsemana=str(dia.year)[2:4] + str(semana)
	date=datetime.now().strftime('%Y%m%d')
	tipo_orden =TipoOrden.objects.get(tipo_orden='LECT')

	sql="INSERT INTO qorder_ordendetrabajo(numero_orden, prioridad, estado, secuencial_registro, secuencia_teorica, orden_terreno, generada_desde_num_os, flag_asignacion_guardada, fecha_hora_asignacion, fecha_hora_importacion, fecha_hora_exportacion, fecha_hora_anulacion, fecha_hora_ult_modificacion, fecha_hora_carga, consumo_id, punto_suministro_id, ruta_id, tecnico_id, tipo_orden_id, usuario_asignacion_id)\
    select concat(COD_UNICOM,{},RUTA,lpad(ITINERARIO,5,'0'),CICLO,@rownum:=@rownum+1),1,1,SECUENCIA,SECUENCIA,0,null,0,null,null,null,null,null,null,concat(COD_MARCA,NRO_APARTO,'CO011'),SEG_REG,concat(COD_UNICOM,RUTA,lpad(ITINERARIO,5,'0'),CICLO,lpad(ANIO,4,'0')),null,{},null from (SELECT @rownum:=0) r, qorder_suministros where COD_UNICOM='{}' and ANIO='{}' ON DUPLICATE KEY UPDATE prioridad=VALUES(prioridad),estado=VALUES(estado),secuencial_registro=VALUES(secuencial_registro),\
    secuencia_teorica=VALUES(secuencia_teorica),orden_terreno=VALUES(orden_terreno),generada_desde_num_os=VALUES(generada_desde_num_os),flag_asignacion_guardada=VALUES(flag_asignacion_guardada),fecha_hora_asignacion=VALUES(fecha_hora_asignacion),estado=VALUES(estado),fecha_hora_importacion=VALUES(fecha_hora_importacion),fecha_hora_exportacion=VALUES(fecha_hora_exportacion),fecha_hora_anulacion=VALUES(fecha_hora_anulacion),fecha_hora_ult_modificacion=VALUES(fecha_hora_ult_modificacion),fecha_hora_carga=VALUES(fecha_hora_carga)".format(date,tipo_orden.id,oficina,strsemana)


	try: 
		#print('aca')
		with closing(connection.cursor()) as cursor: 
			cursor.execute(sql) 

	except Exception as e:

		_log.error(e)		


	print('pasa6')		

def inserthistconsumo(_log,oficina):
	print('entra hist')
	dia=datetime.now()
	semana=datetime.date(dia).isocalendar()[1]
	strsemana=str(dia.year)[2:4] + str(semana)
	string=''
	contador=0
	contador2=0
	valorf = ''
	updatereg=0
	suministros=list(query_to_dicts("select o.numero_orden as num_os,s.COD_MARCA,s.SEG_REG,s.NRO_APARTO,s.COD_ANOMALIA1 as cod_anomalia1,s.LECTURA1 as lectura1,s.CONSUMO1 as consumo1,s.FECHA_LECTURA1 as fecha_lectura1,s.COD_ANOMALIA2 as cod_anomalia2,s.LECTURA2 as lectura2,s.CONSUMO2 as consumo2,s.FECHA_LECTURA2 as fecha_lectura2,s.COD_ANOMALIA3 as cod_anomalia3,s.LECTURA3 as lectura3,s.CONSUMO3 as consumo3,s.FECHA_LECTURA3 as fecha_lectura3,s.COD_ANOMALIA4 as cod_anomalia4,s.LECTURA4 as lectura4,s.CONSUMO4 as consumo4,s.FECHA_LECTURA4 as fecha_lectura4,s.COD_ANOMALIA5 as cod_anomalia5,s.LECTURA5 as lectura5,s.CONSUMO5 as consumo5,s.FECHA_LECTURA5 as fecha_lectura5,s.COD_ANOMALIA6 as cod_anomalia6,s.LECTURA6 as lectura6,s.CONSUMO6 as consumo6,s.FECHA_LECTURA6 as fecha_lectura6\
	from qorder_suministros as s inner join qorder_ordendetrabajo as o on s.SEG_REG=o.punto_suministro_id inner join qorder_ruta as r on o.ruta_id=r.idruta and r.oficina_id='{}' and r.anio='{}' where s.COD_UNICOM='{}' and s.ANIO='{}'".format(oficina,strsemana,oficina,strsemana)))

	for s in suministros:


		#fecha1 = str(s['fecha_lectura1'])
		# print(fecha)
		#if fecha1 == '':
	#		True
		#else:
		#	fanio1 = int(fecha1[0:2]) + 2000
		#	fmes1= fecha1[2:4]
		#	fdia1 = fecha1[4:6]
		#	fecha_lectura1 = datetime.strptime(str(fanio1) + '-' + fmes1 + '-' + fdia1, '%Y-%m-%d').date()
		#	strfecha_lectura1 = fecha_lectura1.strftime('%Y%m%d')
		#	anio1 = fecha_lectura1.strftime('%Y%m')
			# print('pasa')


		#fecha2 = str(s['fecha_lectura2'])
		# print(fecha)
		#if fecha2 == '':
		#	True
		#else:
		#	fanio2 = int(fecha2[0:2]) + 2000
		#	fmes2 = fecha2[2:4]
		#	fdia2 = fecha2[4:6]
		#	fecha_lectura2 = datetime.strptime(str(fanio2) + '-' + fmes2 + '-' + fdia2, '%Y-%m-%d').date()
		#	strfecha_lectura2 = fecha_lectura2.strftime('%Y%m%d')
		#	anio2 = fecha_lectura2.strftime('%Y%m')
			# print('pasa')


		#fecha3 = str(s['fecha_lectura3'])
		# print(fecha)
		#if fecha3 == '':
		#	True
		#else:
		#	fanio3 = int(fecha3[0:2]) + 2000
		#	fmes3 = fecha3[2:4]
		#	fdia3 = fecha3[4:6]
		#	fecha_lectura3 = datetime.strptime(str(fanio3) + '-' + fmes3 + '-' + fdia3, '%Y-%m-%d').date()
		#	strfecha_lectura3 = fecha_lectura3.strftime('%Y%m%d')
		#	anio3 = fecha_lectura3.strftime('%Y%m')
		#	# print('pasa')


		#fecha4 = str(s['fecha_lectura4'])
		# print(fecha)
		#if fecha4 == '':
		#	True
		#else:
		#	fanio4 = int(fecha4[0:2]) + 2000
		#	fmes4 = fecha4[2:4]
		#	fdia4 = fecha4[4:6]
		#	fecha_lectura4 = datetime.strptime(str(fanio4) + '-' + fmes4 + '-' + fdia4, '%Y-%m-%d').date()
		#	strfecha_lectura4 = fecha_lectura4.strftime('%Y%m%d')
		#	anio4 = fecha_lectura4.strftime('%Y%m')
			# print('pasa')


		#fecha5 = str(s['fecha_lectura5'])
		# print(fecha)
		#if fecha5 == '':
		#	True
		#else:
		#	fanio5 = int(fecha5[0:2]) + 2000
		#	fmes5 = fecha5[2:4]
		#	fdia5 = fecha5[4:6]
		#	fecha_lectura5 = datetime.strptime(str(fanio5) + '-' + fmes5 + '-' + fdia5, '%Y-%m-%d').date()
		#	strfecha_lectura5 = fecha_lectura5.strftime('%Y%m%d')
		#	anio5 = fecha_lectura5.strftime('%Y%m')
		#	# print('pasa')


		#fecha6 = str(s['fecha_lectura6'])
		# print(fecha)
		#if fecha6 == '':
		#	True
		#else:
		#	fanio6 = int(fecha6[0:2]) + 2000
		#	fmes6 = fecha6[2:4]
		#	fdia6 = fecha6[4:6]
		#	fecha_lectura6 = datetime.strptime(str(fanio6) + '-' + fmes6 + '-' + fdia6, '%Y-%m-%d').date()
		#	strfecha_lectura6 = fecha_lectura6.strftime('%Y%m%d')
		#	anio6 = fecha_lectura6.strftime('%Y%m')
		#	anio6 = fecha_lectura6.strftime('%Y%m')
			# print('pasa')

		string=str('')+'|'+s['num_os']+'|'+ str(s['cod_anomalia1'])+'|'+ str(s['lectura1']) +'|'+ str(s['consumo1']) +'|'+ s['fecha_lectura1']+'|'+str(s['cod_anomalia2'])+'|'+ str(s['lectura2']) +'|'+ str(s['consumo2']) +'|'+s['fecha_lectura2']+'|'+str(s['cod_anomalia3'])+'|'+ str(s['lectura3']) +'|'+ str(s['consumo3']) +'|'+ s['fecha_lectura3']+'|'+str(s['cod_anomalia4'])+'|'+ str(s['lectura4']) +'|'+ str(s['consumo4']) +'|'+ s['fecha_lectura4']+'|'+str(s['cod_anomalia5'])+'|'+ str(s['lectura5']) +'|'+ str(s['consumo5']) +'|'+ s['fecha_lectura5']+'|'+str(s['cod_anomalia6'])+'|'+ str(s['lectura6']) +'|'+ str(s['consumo6']) +'|'+ s['fecha_lectura6']

		valor = ''.join(str(string))
		valorf = valorf + valor.replace('(', '').replace(')', '').replace("'", '') + '\n'
	path='/home/aysa'+'/'+oficina+'/'+'importar_historico.txt'
	archivo = open(path, 'w')
	archivo.write(valorf)

	archivo.close()
	print('termina de escribir archivo')
	sql = "LOAD DATA LOCAL INFILE '{}' INTO TABLE qorder_importacion_historico FIELDS TERMINATED BY '|' LINES TERMINATED BY '\\n'".format(path)
	print('entra')
	print(sql)
	try:
		with closing(connection.cursor()) as cursor:
			cursor.execute(sql)

	except Exception as e:

		_log.error(e)
	print('termina el bulk insert')
	#	sql = "INSERT INTO aysa.qorder_importacion_historico(orden_trabajo_id, cod_anomalia1, lectura1, consumo1, fecha_lectura1, cod_anomalia2, lectura2, consumo2, fecha_lectura2, cod_anomalia3, lectura3, consumo3, fecha_lectura3, cod_anomalia4, lectura4, consumo4, fecha_lectura4, cod_anomalia5, lectura5, consumo5, fecha_lectura5, cod_anomalia6, lectura6, consumo6, fecha_lectura6)\
	#	VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	#	args = (s['num_os'], s['cod_anomalia1'], s['lectura1'] , s['consumo1'] , s['fecha_lectura1'],s['cod_anomalia2'], s['lectura2'] , s['consumo2'] ,s['fecha_lectura2'],s['cod_anomalia3'], s['lectura3'] , s['consumo3'] , s['fecha_lectura3'],s['cod_anomalia4'], s['lectura4'] , s['consumo4'] , s['fecha_lectura4'],s['cod_anomalia5'], s['lectura5'] , s['consumo5'] , s['fecha_lectura5'],s['cod_anomalia6'], s['lectura6'] , s['consumo6'] , s['fecha_lectura6'])
	#	#
	#	try:
			# print('aca')
	#		with closing(connection.cursor()) as cursor:
	#			cursor.execute(sql, args)
			#
	#	except Exception as e:
	#		_log.error(e)

	#	if contador2==cantsum:
	#		print(contador2)
	#		confparam=ProcesoImpExp.objects.get(oficina=oficina,nombre_proceso='Importación')
	#		confparam.estado_proceso=confparam.estado_proceso+1
	#		confparam.save()


	'''
	for s in suministros:


		contador2=contador2+1
		contador=contador+1
		resultado=int(int(cantsum)/20)

		if contador==resultado:
			contador=0
			updatereg=updatereg+1

			if updatereg<20:
				proceso=ProcesoImpExp.objects.get(oficina=oficina,nombre_proceso='Importación')
				proceso.estado_proceso=proceso.estado_proceso+1
				proceso.save()



		fecha=str(s['FECHA_LECTURA1'])
		#print(fecha)
		if fecha=='':
			True
		else:
			fanio=int(fecha[0:2])+2000
			fmes=fecha[2:4]
			fdia=fecha[4:6]
			fecha_lectura=datetime.strptime(str(fanio)+'-'+fmes+'-'+fdia,'%Y-%m-%d').date()
			strfecha_lectura=fecha_lectura.strftime('%Y%m%d')
			anio=fecha_lectura.strftime('%Y%m')
			#print('pasa')
			sql="INSERT INTO aysa.qorder_historicoconsumo(fecha_lectura, lectura, consumo_id, incidencia_1, incidencia_2, incidencia_3, anio, codigo, valor_consumo, tipo_consumo_id,cod_anomalia)\
			VALUES(%s, %s, %s,%s, %s, %s,%s, %s, %s,%s,%s)ON DUPLICATE KEY UPDATE fecha_lectura=VALUES(fecha_lectura),lectura=VALUES(lectura),incidencia_1=VALUES(incidencia_1),incidencia_2=VALUES(incidencia_2),incidencia_3=VALUES(incidencia_3),anio=VALUES(anio),valor_consumo=VALUES(valor_consumo),cod_anomalia=VALUES(cod_anomalia)"
			args=(fecha_lectura,s['LECTURA1'],s['COD_MARCA']+s['NRO_APARTO']+'CO011',None,None,None,anio,s['COD_MARCA']+s['NRO_APARTO']+'CO011'+'_'+strfecha_lectura,s['CONSUMO1'],'CO011',s['COD_ANOMALIA1'])
#	
			try:
				#print('aca')
				with closing(connection.cursor()) as cursor:
					cursor.execute(sql,args) 
#	
			except Exception as e:
				_log.error(e)		


		fecha=str(s['FECHA_LECTURA2'])
		#print(fecha)
		if fecha=='':
			True
		else:
			fanio=int(fecha[0:2])+2000
			fmes=fecha[2:4]
			fdia=fecha[4:6]
			fecha_lectura=datetime.strptime(str(fanio)+'-'+fmes+'-'+fdia,'%Y-%m-%d').date()
			strfecha_lectura=fecha_lectura.strftime('%Y%m%d')
			anio=fecha_lectura.strftime('%Y%m')
			#print('pasa')
			sql="INSERT INTO aysa.qorder_historicoconsumo(fecha_lectura, lectura, consumo_id, incidencia_1, incidencia_2, incidencia_3, anio, codigo, valor_consumo, tipo_consumo_id,cod_anomalia)\
			VALUES(%s, %s, %s,%s, %s, %s,%s, %s, %s,%s,%s)ON DUPLICATE KEY UPDATE fecha_lectura=VALUES(fecha_lectura),lectura=VALUES(lectura),incidencia_1=VALUES(incidencia_1),incidencia_2=VALUES(incidencia_2),incidencia_3=VALUES(incidencia_3),anio=VALUES(anio),valor_consumo=VALUES(valor_consumo),cod_anomalia=VALUES(cod_anomalia)"
			args=(fecha_lectura,s['LECTURA2'],s['COD_MARCA']+s['NRO_APARTO']+'CO011',None,None,None,anio,s['COD_MARCA']+s['NRO_APARTO']+'CO011'+'_'+strfecha_lectura,s['CONSUMO2'],'CO011',s['COD_ANOMALIA2'])
#	
			try:
				#print('aca')
				with closing(connection.cursor()) as cursor:
					cursor.execute(sql,args) 
#	
			except Exception as e:
				_log.error(e)


		fecha=str(s['FECHA_LECTURA3'])
		#print(fecha)
		if fecha=='':
			True
		else:
			fanio=int(fecha[0:2])+2000
			fmes=fecha[2:4]
			fdia=fecha[4:6]
			fecha_lectura=datetime.strptime(str(fanio)+'-'+fmes+'-'+fdia,'%Y-%m-%d').date()
			strfecha_lectura=fecha_lectura.strftime('%Y%m%d')
			anio=fecha_lectura.strftime('%Y%m')
			#print('pasa')
			sql="INSERT INTO aysa.qorder_historicoconsumo(fecha_lectura, lectura, consumo_id, incidencia_1, incidencia_2, incidencia_3, anio, codigo, valor_consumo, tipo_consumo_id,cod_anomalia)\
			VALUES(%s, %s, %s,%s, %s, %s,%s, %s, %s,%s,%s)ON DUPLICATE KEY UPDATE fecha_lectura=VALUES(fecha_lectura),lectura=VALUES(lectura),incidencia_1=VALUES(incidencia_1),incidencia_2=VALUES(incidencia_2),incidencia_3=VALUES(incidencia_3),anio=VALUES(anio),valor_consumo=VALUES(valor_consumo),cod_anomalia=VALUES(cod_anomalia)"
			args=(fecha_lectura,s['LECTURA3'],s['COD_MARCA']+s['NRO_APARTO']+'CO011',None,None,None,anio,s['COD_MARCA']+s['NRO_APARTO']+'CO011'+'_'+strfecha_lectura,s['CONSUMO3'],'CO011',s['COD_ANOMALIA3'])
#	
			try:
				#print('aca')
				with closing(connection.cursor()) as cursor:
					cursor.execute(sql,args) 
#	
			except Exception as e:
				_log.error(e)		


		fecha=str(s['FECHA_LECTURA4'])
		#print(fecha)
		if fecha=='':
			True
		else:
			fanio=int(fecha[0:2])+2000
			fmes=fecha[2:4]
			fdia=fecha[4:6]
			fecha_lectura=datetime.strptime(str(fanio)+'-'+fmes+'-'+fdia,'%Y-%m-%d').date()
			strfecha_lectura=fecha_lectura.strftime('%Y%m%d')
			anio=fecha_lectura.strftime('%Y%m')
			#print('pasa')
			sql="INSERT INTO aysa.qorder_historicoconsumo(fecha_lectura, lectura, consumo_id, incidencia_1, incidencia_2, incidencia_3, anio, codigo, valor_consumo, tipo_consumo_id,cod_anomalia)\
			VALUES(%s, %s, %s,%s, %s, %s,%s, %s, %s,%s,%s)ON DUPLICATE KEY UPDATE fecha_lectura=VALUES(fecha_lectura),lectura=VALUES(lectura),incidencia_1=VALUES(incidencia_1),incidencia_2=VALUES(incidencia_2),incidencia_3=VALUES(incidencia_3),anio=VALUES(anio),valor_consumo=VALUES(valor_consumo),cod_anomalia=VALUES(cod_anomalia)"
			args=(fecha_lectura,s['LECTURA4'],s['COD_MARCA']+s['NRO_APARTO']+'CO011',None,None,None,anio,s['COD_MARCA']+s['NRO_APARTO']+'CO011'+'_'+strfecha_lectura,s['CONSUMO4'],'CO011',s['COD_ANOMALIA4'])
#	
			try:
				#print('aca')
				with closing(connection.cursor()) as cursor:
					cursor.execute(sql,args) 
#	
			except Exception as e:
				_log.error(e)


		fecha=str(s['FECHA_LECTURA5'])
		#print(fecha)
		if fecha=='':
			True
		else:
			fanio=int(fecha[0:2])+2000
			fmes=fecha[2:4]
			fdia=fecha[4:6]
			fecha_lectura=datetime.strptime(str(fanio)+'-'+fmes+'-'+fdia,'%Y-%m-%d').date()
			strfecha_lectura=fecha_lectura.strftime('%Y%m%d')
			anio=fecha_lectura.strftime('%Y%m')
			#print('pasa')
			sql="INSERT INTO aysa.qorder_historicoconsumo(fecha_lectura, lectura, consumo_id, incidencia_1, incidencia_2, incidencia_3, anio, codigo, valor_consumo, tipo_consumo_id,cod_anomalia)\
			VALUES(%s, %s, %s,%s, %s, %s,%s, %s, %s,%s,%s)ON DUPLICATE KEY UPDATE fecha_lectura=VALUES(fecha_lectura),lectura=VALUES(lectura),incidencia_1=VALUES(incidencia_1),incidencia_2=VALUES(incidencia_2),incidencia_3=VALUES(incidencia_3),anio=VALUES(anio),valor_consumo=VALUES(valor_consumo),cod_anomalia=VALUES(cod_anomalia)"
			args=(fecha_lectura,s['LECTURA5'],s['COD_MARCA']+s['NRO_APARTO']+'CO011',None,None,None,anio,s['COD_MARCA']+s['NRO_APARTO']+'CO011'+'_'+strfecha_lectura,s['CONSUMO5'],'CO011',s['COD_ANOMALIA5'])
#	
			try:
				#print('aca')
				with closing(connection.cursor()) as cursor:
					cursor.execute(sql,args) 
#	
			except Exception as e:
				_log.error(e)		


		fecha=str(s['FECHA_LECTURA6'])
		#print(fecha)
		if fecha=='':
			True
		else:
			fanio=int(fecha[0:2])+2000
			fmes=fecha[2:4]
			fdia=fecha[4:6]
			fecha_lectura=datetime.strptime(str(fanio)+'-'+fmes+'-'+fdia,'%Y-%m-%d').date()
			strfecha_lectura=fecha_lectura.strftime('%Y%m%d')
			anio=fecha_lectura.strftime('%Y%m')
			#print('pasa')
			sql="INSERT INTO aysa.qorder_historicoconsumo(fecha_lectura, lectura, consumo_id, incidencia_1, incidencia_2, incidencia_3, anio, codigo, valor_consumo, tipo_consumo_id,cod_anomalia)\
			VALUES(%s, %s, %s,%s, %s, %s,%s, %s, %s,%s,%s)ON DUPLICATE KEY UPDATE fecha_lectura=VALUES(fecha_lectura),lectura=VALUES(lectura),incidencia_1=VALUES(incidencia_1),incidencia_2=VALUES(incidencia_2),incidencia_3=VALUES(incidencia_3),anio=VALUES(anio),valor_consumo=VALUES(valor_consumo),cod_anomalia=VALUES(cod_anomalia)"
			args=(fecha_lectura,s['LECTURA6'],s['COD_MARCA']+s['NRO_APARTO']+'CO011',None,None,None,anio,s['COD_MARCA']+s['NRO_APARTO']+'CO011'+'_'+strfecha_lectura,s['CONSUMO6'],'CO011',s['COD_ANOMALIA6'])
#	
			try:
				#print('aca')
				with closing(connection.cursor()) as cursor:
					cursor.execute(sql,args) 
#	
			except Exception as e:
				_log.error(e)

		'''



	print('pasa7')			

#ordt=[]
#date=''
#tipo_orden =TipoOrden.objects.get(tipo_orden='LECT')
#print('entra')
#ruta=Ruta.objects.all()
#suministros=''
#for r in ruta:
#	print(r)
#	print('pasa')
#	suministros=suministros.objects.filter(RUTA=r.ruta,CICLO=r.ciclo,ANIO=r.anio,ITINERARIO=r.itinerario)
#	print('pasa1')
#	date=(str(r.ciclo) + str(datetime.now().day))
#	print('llega')
#	for s in suministros:
#		ordt.append(OrdenDeTrabajo(numero_orden=s.COD_UNICOM+date+s.RUTA+s.ITINERARIO.zfill(4)+str(s.SECUENCIA).zfill(4),
#			punto_suministro= s.SEG_REG,
#			tipo_orden=tipo_orden,
#			secuencial_registro = s.SECUENCIA,
#			secuencia_teorica = s.SECUENCIA,
#			ruta = r.ruta,
#			consumo = s.NRO_APARTO+'CO011' 

#			))
#print('llega1')		

#OrdenDeTrabajo.objects.bulk_create(ordt)	

#def insertordenes(_log):

#	suministros=[]
#	sql="INSERT INTO aysa_backup.qorder_ordendetrabajo\
#(numero_orden, prioridad, estado, secuencial_registro, secuencia_teorica, orden_terreno, generada_desde_num_os, flag_asignacion_guardada, fecha_hora_asignacion, fecha_hora_importacion, fecha_hora_exportacion, fecha_hora_anulacion, fecha_hora_ult_modificacion, fecha_hora_carga, consumo_id, punto_suministro_id, ruta_id, tecnico_id, tipo_orden_id, usuario_asignacion_id)"


#def insertOrdenes(params): 
#	hoy = datetime.now().strftime("%Y")
#
#	params1=params
#
#	params2 = []
#	Ordentrabajo=[]
#	for p in params1:
#		encontro=False
#
#
#		#print('Ordentrabajo' + str (len(Ordentrabajo)))
#		for Ordenes in Ordentrabajo:
#			
#			#print('Ordenes {}'.format(Ordenes))
#			if Ordenes==p[0].strip(' ')+p[38].strip(' ')+p[1].strip(' ')+p[2].strip(' ')+p[5].strip(' '):
#				encontro=True
#				#print(Ordenes)
#				#print(encontro)			
#		if  encontro==False:
#			Ordentrabajo.append(p[0].strip(' ')+p[38].strip(' ')+p[1].strip(' ')+p[2].strip(' ')+p[5].strip(' '))
#			params2.append(p)
#	#print('Ordentrabajo' + str (len(Ordentrabajo)))
#	n_records=len(params2)
#
#	#print('n_records {}'.format(n_records))	
#	#print(str(len(ordenes)))
#	sql = 'INSERT INTO qorder_ordendetrabajo  (numero_orden, prioridad, secuencial_registro, secuencia_teorica, orden_terreno, generada_desde_num_os, flag_asignacion_guardada, fecha_hora_asignacion, fecha_hora_importacion, fecha_hora_exportacion, fecha_hora_anulacion, fecha_hora_ult_modificacion, fecha_hora_carga, estado, punto_suministro_id, ruta_id, tecnico_id, tipo_orden_id, usuario_asignacion_id) VALUES{}'.format( ', '.join(['(%s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s)'] * n_records), ) 
#	#print(sql)
#	#print(params)
# 	
#	params1 = [] 
#	for v in params2: 
#		
#		#print('v {}'.format(v))
#		params1.extend([v[0].strip(' ')+v[38].strip(' ')+v[1].strip(' ')+v[2].strip(' ')+v[5].strip(' '),'1',v[5].strip(' '),v[5].strip(' '),'0',None,'0','','','','','','','1',v[9].strip(' '),v[0].strip(' ')+v[1].strip(' ')+v[2].strip(' ')+v[3].strip(' ')+hoy,None,1,None ]) 
#	
#	try:	
#		with closing(connection.cursor()) as cursor: 
#			cursor.execute(sql,params1) 
#
#	except Exception as e:
#		print(e)



def parceararchivo(_ruta,lista1,oficina,user,_log):

	try:
		lineas=[]
		DataList=[]
		DataFileIn=[]
		lista=[]
		listdistritos=[]
		listporcionesgu=[]
		listporcionprocesos=[]
		listporciones=[]
		files=''
		valor=0
		total_lineas=0
		bExistePorcionGU = False
		dia = datetime.now()
		semana = datetime.date(dia).isocalendar()[1]
		strsemana = str(dia.year)[2:4] + str(semana)


		confparam=ProcesoImpExp.objects.filter(oficina=oficina,nombre_proceso='Importación')
		confparam.update(total=100,estado ='PROGRESO')




		semanaporciones=porcionessemana.objects.filter(REGION='Grandes Clientes').values('DISTRITO','PORCION')
		#print(semanaporciones)
		for p in semanaporciones:
			listporciones.append(p['PORCION'])

		for s in semanaporciones:
			listdistritos.append(s['DISTRITO'])

		
		for ar in lista1:

			distritos="'101','102','103','201','202','203'"

			files=ar
			#print (files)


			if listporciones.count(files)>0:
				#print('entra aca')
				for s in semanaporciones:
					if s['PORCION']!=files:
						continue;
					else:

						#print('entro')
						if distritos.find(str(s['DISTRITO']))>0:
							listporcionprocesos.append(s['PORCION'])

						listporcionesgu.append(s['PORCION'])
						listporcionesgu=list(set(listporcionesgu))
						bExistePorcionGU=True

			else:
				continue;


		#print(listporcionprocesos)
		#print(listporcionesgu)		
		if bExistePorcionGU==False:
			_log.info('No hay porciones de GU para trabajar ')	
		print('entra for lineas')
		for a in lista1:
			#print(a)
			DataList=[]
			lineas=[]
			ruta=_ruta+'/'+ a
			#print(a)			
			DataFileIn = codecs.open(ruta, encoding='ISO 8859-1')
			#print(DataFileIn) 
			DataList =DataList+DataFileIn.readlines()
			#print('datalist' + str (len(DataList)))
			DataFileIn.close()
		
#			print(a)	

			for item in DataList:  # Iterar sobre las filas - cada elemento es la cadena de datos
				if item.startswith('//'):
					continue


				if item.startswith('FFFF'):
					break
				else:

					if len(item) < 427:
						lista.append(item)
					else:
						if str(item[45:55])=='          ':
							_log.error('Registros incompletos {} del archivo {} '.format( str(item[0:18]), str(a)))
							continue
						else:
							item=item.replace("#","n")
							lineas.append(prueba(item))

	

			#print('lista {}'.format(len(lista)))
			#print('lineas {}'.format(len(lineas)))
			_log.info('El archivo {} contiene {} registros incorrectos '.format(str(a),len(lista)))
			_log.info('Se Importaron {} registros del archivo {} '.format(len(lineas),str(a)))
			total_lineas=total_lineas+len(lineas)
			DataFileIn.close()
			# Cerrar este archivo en concreto
			
			files=a
			print(files)
			if listporcionesgu.count(files)>0:
				#print('entrasumgu')
				#print(files)
				filesuministrogu(lineas,oficina,_log)
	
			else:
				#print('entrasumres')
				#print(files)
				filesuministrores(lineas,oficina,_log)

		print('sale for lineas')
		confparam.update(estado_proceso=10,estado ='PROGRESO')
		listporcionprocesos=list(set(listporcionprocesos)) 
		#
		#print('listporcionprocesos{}'.format(listporcionprocesos))
#
		updatetables(listporcionprocesos,_log,oficina,strsemana)

		confparam.update(estado_proceso=20,estado ='PROGRESO')
		codigos=list(query_to_dicts("SELECT DISTINCT COD_MARCA FROM qorder_suministros where ANIO='{}' and COD_UNICOM='{}'".format(strsemana,oficina)))

		for c in codigos:
			sql="INSERT INTO qorder_codigo(codigo, descripcion, activo, prefijo_id)\
            VALUES(%s, %s, %s,%s)ON DUPLICATE KEY UPDATE descripcion=VALUES(descripcion),activo=VALUES(activo),prefijo_id=VALUES(prefijo_id)"
			args = (c['COD_MARCA'],str('AGU')+ str(c['COD_MARCA']),1,'MC')
			try:
				# print('aca')
				with closing(connection.cursor()) as cursor:
					cursor.execute(sql, args)
				#
			except Exception as e:
				_log.error(e)
		insertCliente(_log,oficina)
			#_log.info('Se Importaron Clientes Correctamente')
		insertAparatosSuministro(_log,oficina)
			#_log.ino('Se Importaron Aparatos Correctamente')
		insertAparatoConsumo(_log,oficina)
			#_log.info('Se Importaron Consumos Correctamente')
		insertrutasum(_log,oficina)
		insertDatosSuministro(_log,oficina)
		insertruta(_log,oficina,user)
		insertorden(_log,oficina)
		inserthistconsumo(_log,oficina)
			#_log.info('Se Importaron Puntos Suministros Correctamente')
		if len(lista) ==0:
			_log.info('Cantidad total de suministros importados: {}'.format(total_lineas))
			_log.info('Se realizó Correctamente la Importación')
		else:

			_log.info('---Revisar los siguientes registros no insertados---')
			for l in lista:

				_log.info('Registro incorrecto: Suministro {}'.format(l[0:18]))
		
		generarPieLog1(_log)
		cerrarLog1(_log)				
	except Exception as e:
		print("Excepcion {}".format(e))
		_log.error(e)
