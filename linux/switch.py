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

from core.models.node import ModelNode
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Switch(ModelNode):
    """
    LINUX Bridge model
    """

    # TODO: Create your models here.
    # Has ports
    # Has macs, ...

    class Meta:
        app_label = "linux"
        db_table = "linux_switch"
        verbose_name_plural = 'Switches'

    def __str__(self):
        return "TODO: Linux Bridge"
