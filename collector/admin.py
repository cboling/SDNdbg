from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Site)
admin.site.register(SiteCredentials)
admin.site.register(System)

