from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible

from core.models.node import ModelNode


@python_2_unicode_compatible
class Port(ModelNode):
    """
    OpenVSwitch Switch (bridge) model
    """

    # TODO: Create your models here.
    # Parent is an OVS Switch

    class Meta:
        app_label = "ovs"
        db_table = "ovs_port"

    def __str__(self):
        return "TODO: OVS Port"
