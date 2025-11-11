from django.db import connections
from django.db import connection
from django.conf import settings
import os

class SqlPrintMiddleware(object):
    def process_response(self, request, response):
        sqltime = 0 # Variable to store execution time
        for query in connections["default"].queries:
            sqltime += float(query["time"])  # Add the time that the query took to the total
        for query in connection.queries:
            sqltime += float(query["time"])  # Add the time that the query took to the total
 
        # len(connection.queries) = total number of queries
        print ("Page render: " + str(sqltime) + "sec for " + str(len(connections["default"].queries)) + " queries")
        print ("\033[1;31m[QUERIES QORDER]\033")
        indentation = 2
        if len(connections["default"].queries) > 0 and settings.DEBUG:
            width = terminal_width()
            total_time = 0.0
            for query in connections["default"].queries:
                nice_sql = query['sql'].replace('"', '').replace(',',', ')
                sql = "\033[1;31m[%s]\033[0m %s" % (query['time'], nice_sql)
                total_time = total_time + float(query['time'])
                while len(sql) > width-indentation:
                    print ("%s%s" % (" "*indentation, sql[:width-indentation]))
                    sql = sql[width-indentation:]
                print ("%s%s\n" % (" "*indentation, sql))
            replace_tuple = (" "*indentation, str(total_time))
            print ("%s\033[1;31 m[TOTAL TIME: %s seconds]\033[0m" % replace_tuple)
       



        return response

def terminal_width():
    """
    Function to compute the terminal width.
    WARNING: This is not my code, but I've been using it forever and
    I don't remember where it came from.
    """
    width = 0
    try:
        import struct, fcntl, termios
        s = struct.pack('HHHH', 0, 0, 0, 0)
        x = fcntl.ioctl(1, termios.TIOCGWINSZ, s)
        width = struct.unpack('HHHH', x)[1]
    except:
        pass
    if width <= 0:
        try:
            width = int(os.environ['COLUMNS'])
        except:
            pass
    if width <= 0:
        width = 80
    return width

class LogUserDetails(object):

    def process_request(self, request):
        print('llega')
        print ('user: {}'.format(request.user))
        print ('ip-address: {}'.format(request.META.get('REMOTE_ADDR') ))   
