"""
Copyright (c) 2015 - present.  Boling Consulting Solutions, BCSW.net

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



class VEthPort(ModelNode):
    """
    Linux vEth model
    """

    # TODO: Create your models here.
    # Has ports
    # Has flows

    class Meta:
        app_label = "linux"
        db_table = "linux_vethport"

    def __str__(self):
        return "TODO: Linux Virtual Ethernet port"


@python_2_unicode_compatible
class VEthLink(ModelEdge):
    """
    Linux vEth model
    """

    # TODO: Create your models here.
    # Has ports
    # Has flows

    class Meta:
        app_label = "linux"
        db_table = "linux_vethlink"

    def __str__(self):
        return "TODO: Linux Virtual Ethernet Link"
