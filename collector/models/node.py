from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from core.models import ModelBase, StrippedCharField


@python_2_unicode_compatible
class Node(ModelBase):
    """
    The Node class models a node in the network graph.

    The node may be a physical interface, computer, bridge, port, ...
    """
    # Each variable below represents a database field in this model
    name = StrippedCharField(max_length=2552, default='',
                             help_text='Human readable name for the node')
    description = StrippedCharField(max_length=1024, blank=True, null=True)

    class Meta:
        app_label = "collector"
        db_table = "collector_node"

    def __str__(self):
        return self.name

