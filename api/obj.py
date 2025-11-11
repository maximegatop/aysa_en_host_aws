class Posicionesgps(object):
	"""docstring for ClassName"""
	
	def __init__(self):

		self.Fecha=''
		self.Hora=''
		self.Posicion=''




	def posgps(self,fecha_registro,hora,Posiciones):

		self.Fecha=fecha_registro

		self.Hora=hora
		self.Posicion=Posiciones
		print(self.Fecha)
		print(self.Hora)
		print(self.Posicion)