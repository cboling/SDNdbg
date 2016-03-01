"""
Copyright (c) 2015 - 2016.  Boling Consulting Solutions , BCSW.net

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from core.models.node import ModelNode


@python_2_unicode_compatible
class Switch(ModelNode):
    """
    ONOS Controller Model

    A unique controller.  Multiple controllers in a culster will have the same cluster ID

    Fields / Attributes:
    uniqueId = (char):   A unique character string to identify the item.  This field is
                         combined with parent information to provide a unique path from the
                         highest level object to this item.  For the field itself, it
                         should be as short enough for display purposes but unique enough
                         not to clash with other items.  For instance, a GUID/UUID is always
                         unique.  A name like eth0 is not, so it may need to be prepended prepended
                         with it's parent unique ID. For instance, instead of 'eth0' you may want
                         to use <system-name>/eth0  or <system-name>/<bridge-name>/eth0.

    TODO: How do we set a 'cluster' id.
    TODO: Need a 'cluster master' boolean field
    TODO: Where & how to best store login credentials
    """

    address = models.GenericIPAddressField()
    port = models.IntegerField()  # TODO Place bounds 0-65535 possible?

    # TODO: Username/password is cluster-wide
    # TODO: Each node in a cluster has a unique NodeId
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50)  # TODO Remember to use forms.PasswordInput() in the forms.py

    class Meta:
        app_label = 'onos'
        db_table = 'onos_controller'

    @classmethod
    def create(cls, name, address, port, username, password):
        return cls(name=name, address=address, port=port, username=username, password=password)

    def __str__(self):
        return 'TODO: ONOS Controller'
