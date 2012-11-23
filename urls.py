# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.conf.urls.defaults import *
from farproof.client_list.views import *

urlpatterns = patterns('',
    # Example:
    # (r'^farproof/', include('farproof.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

	# http://www.djangobook.com/en/2.0/chapter08.html
	# 
    (r'^client_list/$', client_index),
    (r'^client_list/([\w, ,-]+)/$', client_contents),
    (r'^client_list/[\w, ,-]+/client_contents/([\w, ,-]+)/$', job_contents)
)
