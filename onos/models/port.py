from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible

from core.models.node import ModelNode


@python_2_unicode_compatible
class Port(ModelNode):
    """
    ONOS Device Port Model
    """

    # TODO: Create your models here.

    class Meta:
        app_label = "onos"
        db_table = "onos_port"

    def __str__(self):
        return "TODO: ONOS Port"
