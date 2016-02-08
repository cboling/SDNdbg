from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


class StrippedCharField(models.CharField):
    """ CharField that strips trailing and leading spaces."""
    def clean(self, value, *args, **kwds):
        if value is not None:
            value = value.strip()
        return super(StrippedCharField, self).clean(value, *args, **kwds)


class SiteCredentials(models.Model):
    """
    The SiteCredentials class models the values need to authenticate with Keystone
    """
    # Each variable below represents a database field in this model
    username = models.CharField(max_length=255, default='admin')
    password = models.CharField(max_length=255, default='password')
    tenant = models.CharField(max_length=255, default='admin')
    auth_url = models.CharField(max_length=255, default='http://localhost:5000/v2.0')

    @python_2_unicode_compatible
    def __str__(self):
        return "%s/%s/%s/%s" % (self.username, self.password, self.tenant, self.auth_url)

class Site(models.Model):
    """
    The Site class models an OpenStack site
    """
    # Each variable below represents a database field in this model
    name = models.StrippedCharField(max_length=32, default='OpenStack Site',
                                    help_text='Human readable name for the site')
    description = models.StrippedCharField(max_length=1024, blank=True, null=True)
    credentials = models.ForeignKey(SiteCredentials, on_delete=models.CASCADE,
                                    help_text='Keystone login credentials for the site')

    @python_2_unicode_compatible
    def __str__(self):
        return self.name_text


class System(models.Model):
    """
    The System class models a physical/virtual system that can be accessed for further
    information.
    """
    # Each variable below represents a database field in this model
    name = models.StrippedCharField(max_length=32, default='System',
                                    help_text='Human readable name for the system')
    description = models.StrippedCharField(max_length=1024, blank=True, null=True)

    # TODO Add system type
    # TODO Add login/access credentiols
    # TODO Add last contacted


    @python_2_unicode_compatible
    def __str__(self):
        return self.name


# TODO: Create more models here.
