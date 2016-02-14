from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from consts import *
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

    def __str__(self):
        return "%s/%s of (%s/%s): %s" % (self.username, self.password, self.tenant, self.region, self.auth_url)


@python_2_unicode_compatible
class Site(ModelBase):
    """
    The Site class models an OpenStack site
    """
    KILO = 'K'
    LIBERTY = 'L'
    SUPPORTED_VERSIONS = (
        (KILO, 'kilo'),
        (LIBERTY, 'liberty'),
    )
    __valid_versions = (KILO, LIBERTY)

    # Each variable below represents a database field in this model
    name = StrippedCharField(max_length=32, default=DEF_SITE_NAME,
                             help_text='Human readable name for the site')

    description = StrippedCharField(max_length=1024, blank=True, null=True)

    version = models.CharField(max_length=2, choices=SUPPORTED_VERSIONS, default=DEF_SITE_VERSION)

    credentials = models.ForeignKey(SiteCredentials, on_delete=models.CASCADE,
                                    help_text='Keystone login credentials for the site')

    # TODO: credentials really needs to be a map where the key is the 'username' and 'tenant' tuple to use
    #       May even want to use the region as a key as well.

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
