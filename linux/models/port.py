from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible

from core.models.node import ModelNode


@python_2_unicode_compatible
class Port(ModelNode):
    """
    LINUX Bridge Port model
    """

    # TODO: Create your models here.
    # Parent is an OVS Switch

    class Meta:
        app_label = "linux"
        db_table = "linux_port"

    def __str__(self):
        return "TODO: Linux bridge Port"
