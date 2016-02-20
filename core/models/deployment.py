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
