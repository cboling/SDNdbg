from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible

from core.models.node import ModelNode


@python_2_unicode_compatible
class Switch(ModelNode):
    """
    OpenVSwitch Switch (bridge) model
    """

    # TODO: Create your models here.
    # Has ports
    # Has flows

    class Meta:
        app_label = "ovs"
        db_table = "ovs_switch"

    def __str__(self):
        return "TODO: OVS Switch"
