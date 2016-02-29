from django.contrib import admin

from .models.port import *
from .models.switch import *

admin.model.register(Switch)
admin.model.register(Port)
admin.model.register(VEth)
