from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from openstack.consts import *
from core.models import ModelBase, StrippedCharField
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

    # Each variable below represents a database field in this model
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
        app_label = "openstack"
        db_table = "openstack_sitecredentials"

    def __str__(self):
        return "%s/%s of (%s/%s): %s" % (self.username, self.password, self.tenant,
                                         self.region, self.auth_url)
