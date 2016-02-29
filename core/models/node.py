from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from core.models.base import ModelBase


@python_2_unicode_compatible
class ModelNode(ModelBase):
    """
    Network Graph Node Model
    """
    name = models.CharField(max_length=255)  # TODO Verify max length allowed

    # TODO For some derived types, the max name may be less, figure out how best to do this

    # TODO: Create your models here.
