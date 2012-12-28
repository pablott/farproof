from django.contrib import admin
from farproof.client_list.models import Client, Job, Item, Page, Revision, Comment, Curve, ProviderContent, ClientContent

class ItemAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['job']}),
        (None,               {'fields': ['name']}),
        (None,               {'fields': ['desc']}),
    ]

admin.site.register(Client)
admin.site.register(Job)
admin.site.register(Item, ItemAdmin)
admin.site.register(Page)
admin.site.register(Revision)
admin.site.register(Comment)
admin.site.register(Curve)
admin.site.register(ProviderContent)
admin.site.register(ClientContent)
