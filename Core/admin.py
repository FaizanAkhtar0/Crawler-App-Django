from django.contrib import admin

from Core.models import MasterURL, SubURL, Image, Document, Content

# Register your models here.

admin.site.register(MasterURL)
admin.site.register(SubURL)
admin.site.register(Image)
admin.site.register(Document)
admin.site.register(Content)