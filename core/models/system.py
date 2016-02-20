"""
Copyright (c) 2015 - 2016.  Boling Consulting Solutions , BCSW.net

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible

from .base import ModelBase, StrippedCharField


@python_2_unicode_compatible
class System(ModelBase):
    """
    The System class models a physical/virtual system that can be accessed for further
    information.
    """
    # Each variable below represents a database field in this model
    name = StrippedCharField(max_length=255, unique=True,
                             help_text='Unique name for this system')
    description = StrippedCharField(max_length=1024, blank=True, null=True)

    # TODO Add system type
    # TODO Add login/access credentials
    # TODO Add last contacted

    class Meta:
        app_label = "core"
        db_table = "core_system"

    def __str__(self):
        return self.name
