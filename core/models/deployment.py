from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from core.models import ModelBase, StrippedCharField


@python_2_unicode_compatible
class Deployment(ModelBase):
    """
    The Deployment class models a grouping of Sites (OpenStack installations)
    """
    # Each variable below represents a database field in this model
    name = StrippedCharField(max_length=64, unique=True,
                             help_text='Name of the deployment')
    description = StrippedCharField(max_length=1024, blank=True, null=True)

    class Meta:
        app_label = "core"
        db_table = "core_deployment"

    def __str__(self):
        return self.name

# TODO: Eventually may want to support Access Control lists to limit what a user can do within a deployment.
# The ACL would allow users to log in, each site within the deployment would allow what they
# could actually perform in that site.
