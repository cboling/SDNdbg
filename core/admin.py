from django.contrib import admin

# Register your models here.

from .models.system import *
from .models.deployment import *

admin.site.register(Deployment)
admin.site.register(System)

