from django.contrib import admin

from .models.flow import *
from .models.link import *
from .models.port import *
from .models.switch import *

admin.model.register(Switch)
admin.model.register(Port)
admin.model.register(Flow)
admin.model.register(Link)
