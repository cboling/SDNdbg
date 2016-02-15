from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from openstack.consts import *
from core.models import ModelBase, StrippedCharField
from .site import Site


@python_2_unicode_compatible
class SiteNode(ModelBase):
    """
    The Site Node class models an OpenStack node (controller, compute, ...) of a site
    """
    name = StrippedCharField(max_length=255, unique=True,
                             help_text='The unique name for this OpenStack node')

    description = StrippedCharField(max_length=1024, blank=True, null=True)
    site = models.ForeignKey(Site, null=True, blank=True, related_name='nodes')

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
