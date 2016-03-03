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

from base import ModelBase
from base import StrippedCharField
from node import ModelNode


@python_2_unicode_compatible
class ModelEdge(ModelBase):
    """
    Base Network Graph Edge (link) Model

    This class provides a simple base class from which other Graph Edge models
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
                         highest level object to this item.  The field itself should be
                         some type of concatenation of the source and target
    rawData (char):      Raw data used to create item. Often JSON, XML, or CLI screen data. It
                         is expected that this data is in character format. If not, use an
                         appropriate binary->ascii conversion such as Base64 and document it
                         in your derived class
    name    (char):      Simple human readable name for the node
    parent  (ModelNode): The parent node (if not Null) of this node.  To get all children, of
                         a Node, query for it other 'nodes' parent field.
    """
    uniqueId = StrippedCharField(max_length=255, db_index=True)
    rawData = models.CharField(max_length=255, blank=True, null=True)

    name = StrippedCharField(max_length=255)  # TODO Verify max length allowed
    # TODO For some derived types, the max name may be less, figure out how best to do this

    source = models.ForeignKey(ModelNode, on_delete=models.CASCADE, related_name='+',
                               help_text='Source Edge')
    target = models.ForeignKey(ModelNode, on_delete=models.CASCADE, related_name='+',
                               help_text='Target Edge')

    class Meta:
        app_label = "core"
        db_table = "core_edge"

    def __str__(self):
        return self.name
