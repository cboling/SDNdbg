from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible

from core.models.node import ModelNode


@python_2_unicode_compatible
class Switch(ModelNode):
    """
    ONOS Switch (device) model
    """

    # TODO: Create your models here.

    class Meta:
        app_label = 'onos'
        db_table = 'onos_switch'

    def __str__(self):
        return 'TODO: ONOS Switch'
