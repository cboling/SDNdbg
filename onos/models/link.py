from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible

from core.models.edge import ModelEdge


@python_2_unicode_compatible
class Link(ModelEdge):
    """
    ONOS Topology Link Model
    """

    # TODO: Create your models here.

    class Meta:
        app_label = "onos"
        db_table = "onos_link"

    def __str__(self):
        return "TODO: ONOS Link"
