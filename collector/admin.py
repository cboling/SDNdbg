from django.contrib import admin

# Register your models here.

from .models.node import *

admin.site.register(Node)

