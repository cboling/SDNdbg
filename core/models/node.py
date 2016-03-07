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

from base import StrippedCharField, ModelBase


@python_2_unicode_compatible
class ModelNode(ModelBase):
    """
    Base Network Graph Node Model

    This class provides a simple base class from which other Graph Node models
    are derived.  In particular, this class will provide fields for a create
    and update timestamp as well as some common fields like 'Name', 'UniqueID', ...

    This model uses django Multi-table inheritance where each model in the hierarchy
    is a model all by itself. Each model corresponds to its own database table and
    can be queried and created individually. The inheritance relationship introduces
    links between the child model and each of its parents (via an
    automatically-created OneToOneField).  This will allow the 'parent' field in this
    base class to work across applications and data tables.  See the following link
    for more info: https://docs.djangoproject.com/en/1.9/topics/db/models/#multi-table-inheritance

    Fields / Attributes:
    uniqueId = (char):   A unique character string to identify the item.  This field is
                         combined with parent information to provide a unique path from the
                         highest level object to this item.  For the field itself, it
                         should be as short enough for display purposes but unique enough
                         not to clash with other items.  For instance, a GUID/UUID is always
                         unique.  A name like eth0 is not, so it may need to be prepended
                         with it's parent unique ID. For instance, instead of 'eth0' you may want
                         to use <system-name>/eth0  or <system-name>/<bridge-name>/eth0.
    rawData (char):      Raw data used to create item. Often JSON, XML, or CLI screen data
    name    (char):      Simple human readable name for the node
    parent  (ModelNode): The parent node (if not Null) of this node.  To get all children, of
                         a Node, query for it other 'nodes' parent field.
    """
    uniqueId = StrippedCharField(max_length=255, db_index=True)
    rawData = models.CharField(max_length=255, blank=True, null=True)

    name = StrippedCharField(max_length=255)  # TODO Verify max length allowed
    # TODO For some derived types, the max name may be less, figure out how best to do this

    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='%(app_label)s_%(class)s_child', help_text='Parent Node')

    class Meta:
        app_label = "core"
        db_table = "core_node"
        ordering = ['name', 'uniqueId']

    def __str__(self):
        return self.name

    @property
    def children(self):
        """
        Child objects
        :return: (list) of children
        """
        # TODO Search for all nodes with this node as a parent
        return []
