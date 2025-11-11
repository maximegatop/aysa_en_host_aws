import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

from itertools import *
from django.db import connection

def query_to_dicts(query_string, *query_args):
    cursor = connection.cursor()
    cursor.execute(query_string, query_args)
    col_names = [desc[0] for desc in cursor.description]
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        row_dict = dict(izip(col_names, row))
        yield row_dict
    return


class Notificacion(object):
	"""docstring for Notificacion"""
	def __init__(self):
		self._message = ""
		self._subject = ""
		self._from = ""
		self._to = ""
		self._smtp_server = ""
		self._smtp_port = 0
		self._user = ""
		self._user_password = ""
		self._mail = None

	def SendMail(self):
		msg = MIMEText(self._message)
		msg['Subject'] = self._subject
		msg['From'] = self._from
		msg['To'] = self._to

		try:
			_mail = smtplib.SMTP(self._smtp_server,self._smtp_port)
			_mail.login(self._user,self._user_password)

			_mail.sendmail(self._from,self._to,msg.as_string())
			
		except Exception as e:
			raise (str(e))
		finally:
			_mail.quit()