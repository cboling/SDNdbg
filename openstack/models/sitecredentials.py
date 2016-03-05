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

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from core.models.base import ModelBase
from openstack.consts import *


# TODO: As this file gets huge, break it up

@python_2_unicode_compatible
class SiteCredentials(ModelBase):
    """
    The SiteCredentials class models the values need to authenticate with Keystone

    Fields / Attributes:
        username (str): The Keystone username, the default is 'admin'
        password (str): Password, the default is 'empty'
        tenant (str):   The tenant project name, the default is 'admin'
        auth_url (str): The authorization URL. The default is the non-administative
                        V2.0 URL on the localhost.
        region (str):   The OpenStack region / zone. The default is 'RegionOne'
    """
    username = models.CharField(max_length=255, default=DEF_KEYSTONE_USERNAME)
    password = models.CharField(max_length=255, default=DEF_KEYSTONE_PASSWORD)
    tenant = models.CharField(max_length=255, default=DEF_KEYSTONE_TENANT)
    auth_url = models.CharField(max_length=255, default=DEF_KEYSTONE_AUTH_URL)
    region = models.CharField(max_length=255, default=DEF_KEYSTONE_REGION)

    @classmethod
    def create(cls, username=DEF_KEYSTONE_USERNAME,
               password=DEF_KEYSTONE_PASSWORD,
               tenant=DEF_KEYSTONE_TENANT,
               auth_url=DEF_KEYSTONE_AUTH_URL,
               region=DEF_KEYSTONE_REGION):
        return SiteCredentials(username=username, password=password, tenant=tenant,
                               auth_url=auth_url, region=region)

    class Meta:
        app_label = 'openstack'
        db_table = 'openstack_sitecredentials'
        verbose_name_plural = 'Site Credentials'

    def __str__(self):
        return "%s/%s of (%s/%s): %s" % (self.username, self.password, self.tenant,
                                         self.region, self.auth_url)
