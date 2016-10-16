from django.contrib import admin


admin.autodiscover()
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import *
from farproof.core.views import *
from farproof.uploader.uploader import *
from farproof.core.templatetags.review import *


urlpatterns = [
                        # Uncomment the admin/doc line below to enable admin documentation:
                        url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                        # Uncomment the next line to enable the admin:
                        url(r'^admin/', include(admin.site.urls)),
                        # TODO Add 404 templates when a client, job, item or page is not found
                        url(r'^$', main),

                        url(r'^client_add/$', client_add),
                        url(r'^client_search/$', client_search),
                        url(r'^(\d+)/$', client_view),

                        url(r'^(\d+)/job_add/$', job_add),
                        url(r'^(\d+)/job_search/$', job_search),
                        url(r'^(\d+)/(\d+)/$', job_view),

                        url(r'^(\d+)/(\d+)/item_add/$', item_add),
                        url(r'^(\d+)/(\d+)/(\d+):(\w+)/list/$', item_view_list),
                        url(r'^(\d+)/(\d+)/(\d+):(\w+)/thumbs/$', item_view_thumbs),
                        url(r'^(\d+)/(\d+)/(\d+):(\w+)/(\d+)/$', page_view),
                        url(r'^(\d+)/(\d+)/(\d+)/(\d+)/page_info/$', page_info),
                        url(r'^(\d+)/(\d+)/(\d+):(\w+)/file_upload/$', file_upload),  # URL for file uploader page
                        url(r'^(\d+)/(\d+)/(\d+)/uploader$', uploader),  # URL for AJAX file catcher
                        url(r'^uploads/$', uploads),  # URL for uploads list
                        url(r'^queue_poll$', queue_poll),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

