from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from core.models import ModelBase, StrippedCharField


@python_2_unicode_compatible
class System(ModelBase):
    """
    The System class models a physical/virtual system that can be accessed for further
    information.
    """
    # Each variable below represents a database field in this model
    name = StrippedCharField(max_length=32, default='System',
                             help_text='Human readable name for the system')
    description = StrippedCharField(max_length=1024, blank=True, null=True)

    # TODO Add system type
    # TODO Add login/access credentiols
    # TODO Add last contacted

    def __str__(self):
        return self.name


# TODO: Create more models here.
