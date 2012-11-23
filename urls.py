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
    #(r'^main/$', 'client_list'), # ESTÁ MAL VER TUTORIAL 3 (AL FINAL)
    (r'^client_list/$', client_index), # EST`MAL VER TUTORIAL 3 (AL FINAL)
    #(r'^client_contents/$', client_contents), # EST`MAL VER TUTORIAL 3 (AL FINAL)
    #(r'^client_list/()/$', client_contents), # EST`MAL VER TUTORIAL 3 (AL FINAL)
    (r'^client_list/(\w*[a-z _0-9-])/$', client_contents), # EST`MAL VER TUTORIAL 3 (AL FINAL)
)
