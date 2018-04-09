from django.contrib import admin

from .models import MaBrand, MaModel, MaItemType

admin.site.register(MaItemType)
admin.site.register(MaModel)
admin.site.register(MaBrand)
