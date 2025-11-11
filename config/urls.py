"""qorderweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from core.views import log_in, log_out, index,foto


admin.site.site_url = '/qorderweb/'
urlpatterns = [
    url(r'^qorderweb/admin/login/$', log_in, name='login_main'),
    url(r'^qorderweb/admin/logout/$', log_out, name='logout_main'),
    url(r'^qorderweb/admin/', include(admin.site.urls), name='admin'),
    url(r'^qorderweb/login$', log_in, name='login'),
    url(r'^qorderweb/logout$', log_out, name='logout'),
    url(r'^qorderweb/$', index, name='index'),
    url(r'^qorderweb/qorder/', include('qorder.urls', namespace='qorder')),
    url(r'^qorderweb/api/', include('api.urls')),
    url(r'^qorderweb/foto/$', foto, name='foto'),
    

    
]

def handler500(request): 
    response = render_to_response('500.html', {}, context_instance=RequestContext(request)) 
    response.status_code = 500 
    return response


admin.site.site_header = settings.TITLE_SITE
admin.site.site_title = 'settings.TITLE_SITE'
