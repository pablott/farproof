﻿# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Deprecated for Django 1.5:
#from django.conf.urls import *
from django.conf.urls import *
from farproof.client_list.views import *
from farproof.uploader.uploader import *
from farproof.client_list.templatetags.review import *


urlpatterns = patterns('',
    # Example:
    # (r'^farproof/', include('farproof.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
	
	# URL manager for Dajaxice:
	url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
	
	#TODO Add 404 templates when a client, job, item or page is not found
    (r'^$', main),
	
	(r'^client_add/$', client_add),
	(r'^client_search/$', client_search),
    (r'^(\d+)/$', client_view),
	
	(r'^(\d+)/job_add/$', job_add),
	(r'^(\d+)/job_search/$', job_search),
	(r'^(\d+)/(\d+)/$', job_view),
	
	(r'^(\d+)/(\d+)/item_add/$', item_add),
    (r'^(\d+)/(\d+)/(\d+)/list/$', item_view_list),
    (r'^(\d+)/(\d+)/(\d+)/thumbs/$', item_view_thumbs),
    (r'^(\d+)/(\d+)/(\d+)/(\d+)/$', page_view),
    (r'^(\d+)/(\d+)/(\d+)/(\d+)/page_info/$', page_info),
    (r'^(\d+)/(\d+)/(\d+)/(\d+)/file_upload/$', file_upload),
	
    (r'^(\d+)/(\d+)/(\d+)/(\d+)/ajax/comment_add$', comment_add),
)
#(r'^(?P<category>\w+)/feedback/$', 'my_view') # Might be useful as wildcard capture method

import settings
if settings.DEBUG:
    from django.views.static import serve
    _media_url = settings.MEDIA_URL
    if _media_url.startswith('/'):
        _media_url = _media_url[1:]
        urlpatterns += patterns('',
                                (r'^%s(?P<path>.*)$' % _media_url,
                                serve,
                                {'document_root': settings.MEDIA_ROOT}))
    del _media_url, serve

urlpatterns += staticfiles_urlpatterns()