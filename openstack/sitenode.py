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

from core.models.base import ModelBase, StrippedCharField
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from openstack.consts import *

from .site import Site


@python_2_unicode_compatible
class SiteNode(ModelBase):
    """
    The Site Node class models an OpenStack node (controller, compute, ...) of a site
    """
    name = StrippedCharField(max_length=255, unique=True,
                             help_text='The unique name for this OpenStack node')

    description = StrippedCharField(max_length=1024, blank=True, null=True)
    site_ref = models.ForeignKey(Site, null=True, blank=True, related_name='sitenode_site')

    # TODO: may need a list of services running, or at least the few we really care about

    class Meta:
        app_label = "openstack"
        db_table = "openstack_sitenode"

    @classmethod
    def create(cls, name=DEF_SITE_NAME,
               description=DEF_SITE_DESCRIPTION):
        return SiteNode(name=name, description=description)

    def __str__(self):
        return "%s [%s]" % (self.name_text, self.site)

# TODO: May need to relate this to a 'system' or other item since we may need to login
# outside of doing it with OpenStack Python APIs
