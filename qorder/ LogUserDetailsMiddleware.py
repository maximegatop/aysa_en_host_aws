class LogUserDetailsMiddleware(object):

    def process_request(self, request):
    	print('llega 1')
        print 'user: ' + request.user
        print 'ip-address: ' + request.META.get('REMOTE_ADDR')