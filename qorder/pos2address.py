import urllib
#mport urllib2
#import simplejson
from json import JSONDecoder
from urllib.request import urlopen

class ReverseGeocoder(object):
    def __init__(self):
        self.error = True

    def geocode(self, lat, lon, zoom = 18):
        url = base_url = "http://nominatim.openstreetmap.org/reverse?poligon=0&lat={}&lon={}&addressdetails=1&format=json".format(lat,lon)
        with urlopen(url) as data:
           i = data.read()
        response = i.decode('utf8')
        return self.parse_json(response)

    def get_error(self):
        print("adentro get_error {}".format(self.error))
        return self.error

    def parse_json(self, data):
        error = False
        try:

            #jsondata = simplejson.loads(data)
            jd = JSONDecoder()
            jsondata = jd.decode(data)

            if "error" in data:
                error = True
                jsondata['full_address'] = jsondata['error']
            elif "display_name" in data:
                error = False
                jsondata['full_address'] = jsondata['display_name']
            else:
                error = False
                jsondata['full_address'] = "S/D"
  
        except simplejson.JSONDecodeError:
            jsondata = []
        print("Error {}".format(self.error))
        self.__dict__ = jsondata 
        self.error = error