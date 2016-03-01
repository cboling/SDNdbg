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

from django.utils.encoding import python_2_unicode_compatible

from core.models.base import StrippedCharField
from core.models.node import ModelNode


@python_2_unicode_compatible
class Cluster(ModelNode):
    """
    ONOS Cluster Model

    This identifies a collection of ONOS Controller Nodes that form a cluster
    """

    uniqueId = StrippedCharField(db_index=True)

    class Meta:
        app_label = 'onos'
        db_table = 'onos_cluster'

    def __str__(self):
        return 'TODO: ONOS Cluster'

        # REST at: http://$OC1:8181/onos/v1/cluster
        #
        # RESULT = {"nodes": [{"id": "10.0.3.175", "ip": "10.0.3.175", "tcpPort": 9876, "status": "ACTIVE"},
        #                     {"id": "10.0.3.174", "ip": "10.0.3.174", "tcpPort": 9876, "status": "ACTIVE"},
        #                     {"id": "10.0.3.35",  "ip": "10.0.3.35",  "tcpPort": 9876, "status": "ACTIVE"}]}
