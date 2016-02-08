from __future__ import unicode_literals
from django.db import models


class SiteCredentials(models.Model):
    """
    The SiteCredentials class models the values need to authenticate with Keystone
    """
    # Each variable below represents a database field in this model
    username = models.CharField(max_length=255, default='admin')
    password = models.CharField(max_length=255, default='password')
    tenant = models.CharField(max_length=255, default='admin')
    auth_url = models.CharField(max_length=255, default='http://localhost:5000/v2.0')


class Site(models.Model):
    """
    The Site class models an OpenStack site
    """
    # Each variable below represents a database field in this model
    name_text = models.CharField(max_length=32, default='OpenStack Site',
                                 help_text='Human readable name for the site')
    description = models.CharField(max_length=1024, blank=True, null=True)
    credentials = models.ForeignKey(SiteCredentials, on_delete=models.CASCADE,
                                    help_text='Keystone login credentials for the site')

# TODO: Create more models here.
