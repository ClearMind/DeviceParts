from parts.models import *
from django.contrib.admin import ModelAdmin, site, TabularInline

class PartInline(TabularInline):
    model = PartInStore

class StoreAdmin(ModelAdmin):
    inlines = [PartInline, ]

site.register(PartType)
site.register(DeviceType)
site.register(Brand)
site.register(Part)
site.register(Store, StoreAdmin)
site.register(Device)

