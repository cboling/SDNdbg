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
from core.models.deployment import Deployment
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from openstack.consts import *

from .sitecredentials import SiteCredentials


@python_2_unicode_compatible
class Site(ModelBase):
    """
    The Site class models an OpenStack site

    An individual OpenStack site could be a member of multiple deployments.  An example
    would be when you want
    """
    KILO = 'K'
    LIBERTY = 'L'
    SUPPORTED_VERSIONS = (
        (KILO, 'kilo'),
        (LIBERTY, 'liberty'),
    )
    __valid_versions = (KILO, LIBERTY)

    # Each variable below represents a database field in this model
    name = StrippedCharField(max_length=64, default=DEF_SITE_NAME,
                             help_text='The name for this site')

    description = StrippedCharField(max_length=1024, blank=True, null=True)

    deployments = models.ManyToManyField('core.Deployment', through='SiteDeployment',
                                         blank=True,
                                         help_text='Select which sites are part of this deployment',
                                         related_name='site_deployments')

    version = models.CharField(max_length=2, choices=SUPPORTED_VERSIONS, default=DEF_SITE_VERSION)

    credentials = models.ForeignKey(SiteCredentials, on_delete=models.CASCADE,
                                    help_text='Keystone login credentials for the site')

    # TODO: credentials really needs to be a map where the key is the 'username' and 'tenant' tuple to use
    #       May even want to use the region as a key as well.

    class Meta:
        app_label = "openstack"
        db_table = "openstack_site"

    @classmethod
    def create(cls, name=DEF_SITE_NAME,
               description=DEF_SITE_DESCRIPTION,
               version=DEF_SITE_VERSION):
        return Site(name=name, description=description, version=version)

    def __str__(self):
        return "%s [%s]" % (self.name_text,
                            self.SUPPORTED_VERSIONS[self.version] if self.version in self.SUPPORTED_VERSION[0]
                            else '???')

    def is_versionvalid(self):
        """ Is this a supported OpenStack version
        :return: (bool) True if this version is support, False otherwise.
        """
        return self.version in self.__valid_versions

# TODO: Eventually may want to support Access Control lists to limit what a user can do within a deployment.
# The ACL would allow users to log in, each site within the deployment would allow what they
# could actually perform in that site.


@python_2_unicode_compatible
class SiteDeployment(ModelBase):
    site_ref = models.ForeignKey(Site, related_name='sitedeployments_site')
    deployment_ref = models.ForeignKey(Deployment, related_name='sitedeployments_deployment')
    '''
    TODO: Is this best here or elsewhere?
    availability_zone = StrippedCharField(max_length=200, null=True, blank=True,
                                          help_text="OpenStack availability zone")
    '''

    class Meta:
        app_label = "openstack"
        db_table = "openstack_sitedeployment"
        unique_together = ('site_ref', 'deployment_ref')

    def __str__(self):
        return '%s %s' % (self.deployment, self.site)

