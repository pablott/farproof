#from view.models import Poll
#from view.models import Choice
from farproof.client_list.models import Client
from farproof.client_list.models import Job
from farproof.client_list.models import Item
from farproof.client_list.models import Page
from farproof.client_list.models import Revision
from farproof.client_list.models import Comment
from farproof.client_list.models import PDF
from farproof.client_list.models import Correction

from django.contrib import admin

class ItemAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['job']}),
        (None,               {'fields': ['name']}),
    ]

#admin.site.register(Poll)
#admin.site.register(Choice)
admin.site.register(Client)
admin.site.register(Job)
admin.site.register(Item, ItemAdmin)
admin.site.register(Page)
admin.site.register(Revision)
admin.site.register(Comment)
admin.site.register(PDF)
admin.site.register(Correction)
