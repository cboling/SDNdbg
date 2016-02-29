from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible

from core.models.node import ModelNode


@python_2_unicode_compatible
class Switch(ModelNode):
    """
    LINUX Bridge model
    """

    # TODO: Create your models here.
    # Has ports
    # Has macs, ...

    class Meta:
        app_label = "linux"
        db_table = "linux_switch"

    def __str__(self):
        return "TODO: Linux Bridge"
