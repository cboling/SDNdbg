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
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible

from core.models.base import StrippedCharField
from core.models.node import ModelNode


@python_2_unicode_compatible
class ModelEdge(models.Model):
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
    rawData (char):      Raw data used to create item. Often JSON, XML, or CLI screen data
    created (timezone):  The UTC timestamp when this model was first created
    updated (timezone):  The UTC timestamp when this model last saved a change
    name    (char):      Simple human readable name for the node
    parent  (ModelNode): The parent node (if not Null) of this node.  To get all children, of
                         a Node, query for it other 'nodes' parent field.
    """
    uniqueId = StrippedCharField(db_index=True)
    rawData = models.CharField(blank=True, null=True)

    created = models.DateTimeField(editable=False)
    updated = models.DateTimeField()

    name = StrippedCharField(max_length=255)  # TODO Verify max length allowed
    # TODO For some derived types, the max name may be less, figure out how best to do this

    source = models.ForeignKey(ModelNode, on_delete=models.CASCADE, help_text='Source Edge')
    target = models.ForeignKey(ModelNode, on_delete=models.CASCADE, help_text='Target Edge')

    class Meta:
        app_label = "core"
        db_table = "core_edge"

    def save(self, *args, **kwargs):
        # Save created if this is a new field

        now = timezone.now()

        if not self.id:
            self.created = now

        # Update 'updated' field
        self.updated = now

        # TODO do we want to modify the 'updated' here?
        super(ModelEdge, self).save(*args, **kwargs)
