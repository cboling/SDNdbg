from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible

from core.models.edge import ModelEdge
from core.models.node import ModelNode


@python_2_unicode_compatible
class VEthPort(ModelNode):
    """
    Linux vEth model
    """

    # TODO: Create your models here.
    # Has ports
    # Has flows

    class Meta:
        app_label = "linux"
        db_table = "linux_vethport"

    def __str__(self):
        return "TODO: Linux Virtual Ethernet port"


@python_2_unicode_compatible
class VEthLink(ModelEdge):
    """
    Linux vEth model
    """

    # TODO: Create your models here.
    # Has ports
    # Has flows

    class Meta:
        app_label = "linux"
        db_table = "linux_vethlink"

    def __str__(self):
        return "TODO: Linux Virtual Ethernet Link"
