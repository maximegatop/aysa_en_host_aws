from datetime import timedelta, date, datetime
import os


class Logger(object):

	def __init__(self):
		self.tipo=''
		self.isDebug=False
		self.isInfo=False
		self.isError=False
		self.dato=''
		self._ruta=''
		self.rutadef=''
		self._sLogName=''






	def logsetlevel(self,tipo):
		print('entro log')					# Tipo de logger
		if tipo=='DEBUG':
			self.isDebug=True

		if tipo=='INFO':
			self.isInfo=True
			print(tipo)
			print(self.isInfo)

		if tipo=='ERROR':
			self.isError=True
	
		return tipo		


	def getDateFolder(self):							#Dato de la hora

		self.dato=datetime.now().strftime("%Y%m%d")
							
		return self.dato

	def Debug(self,mensaje ):
	    
		if  self.isDebug==True and self.isInfo==False and self.isError==False:

			self.Writelog( "[DEBUG] - " + mensaje) 
		

	    

	def Info(self,mensaje ):
		print(self.isDebug)
		print(self.isInfo)
		print(self.isError)

		if  (self.isDebug==True or self.isInfo==True) and self.isError==False:
			print('paso')
			self.Writelog( "[INFO] - " + mensaje )
			print('entro')

	def Error(self,mensaje ):
	    
		if self.isDebug==True or self.isInfo==True or self.isError==True: 
		
			self.Writelog( "[ERROR] - " + mensaje)
	    
	
	def setpath(self,path1):							#Ruta que se utiliza
		self._ruta=path1		
		print('_ruta {}'.format(self._ruta))
	
	def Writelog(self,_sMensaje,):						#Creacion archivo y directorio de la ruta
		self.rutadef=self._ruta + self.getDateFolder()
		print(self.rutadef)
		escribir=datetime.now().strftime ('%H%M%S') + ' - ' + _sMensaje
		if not os.path.exists(self.rutadef): 
			os.makedirs(self.rutadef)

		_file=open( self.rutadef + '/'  + self.getLogFileName(),'a')

		_file.write('\n' + escribir)

		_file.close()


	def getLogFileName(self):
		_sLogName= datetime.now().strftime('%Y%m%d_%H') + ".txt"
		return _sLogName


	def Writelog_N(self,_sMensaje,):						#Creacion archivo y directorio de la ruta
		self.rutadef=self._ruta
		print(self.rutadef)
		escribir=datetime.now().strftime ('%H:%M:%S') + ' - ' + _sMensaje

		try:

			if not os.path.exists(self.rutadef): 
				os.makedirs(self.rutadef)

			_file=open( self.rutadef + self.getLogFileName_N(),'a')

			_file.write('\n' + escribir)

			_file.close()

		except Exception as e:
			
			print(e)


	def getLogFileName_N(self):
		_sLogName= datetime.now().strftime('%Y%m%d') + ".txt"
		return _sLogName


	

