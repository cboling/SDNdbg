from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible

from core.models.edge import ModelEdge


@python_2_unicode_compatible
class Flow(ModelEdge):
    """
    ONOS Switch/Device Flow model
    """

    # TODO: Create your models here.

    class Meta:
        app_label = "onos"
        db_table = "onos_flow"

    def __str__(self):
        return "TODO: ONOS Flow"
