from django.conf.urls import patterns, include, url 
from rest_framework.urlpatterns import format_suffix_patterns 
from . import views



urlpatterns = patterns('api.views',
 	url(r'getflag', views.getflag),
 	url(r'getfechahora', views.getfechahora),
 	url(r'getpasswordqorder', views.getpasswordqorder),
 	url(r'getcodigosiddesc', views.getcodigosiddesc),
 	url(r'getdata', views.getdata),
   )