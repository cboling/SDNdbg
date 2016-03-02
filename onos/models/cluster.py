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

import requests
from django.utils.encoding import python_2_unicode_compatible

from core.models.node import ModelNode
from onos.models import *


@python_2_unicode_compatible
class Cluster(ModelNode):
    """
    ONOS Cluster Model

    This identifies a collection of ONOS Controller Nodes that form a cluster
    """
    __URL_LEAF = 'cluster'
    __NODES = 'nodes'
    __ID = 'id'
    __IP = 'ip'
    __PORT = 'tcpPort'
    __STATUS = 'status'

    class Meta:
        app_label = 'onos'
        db_table = 'onos_cluster'

    def __str__(self):
        return 'TODO: ONOS Cluster'

    @classmethod
    def from_json(cls, json_data):
        """
        Create an ONOS Cluster object from JSON returned from a controller

        For the 1.4 Release, the expected JSON looks similar to the following:

        REST at: http://$OC1:8181/onos/v1/cluster

        RESULT = {"nodes": [{"id": "10.0.3.175", "ip": "10.0.3.175", "tcpPort": 9876, "status": "ACTIVE"},
                            {"id": "10.0.3.174", "ip": "10.0.3.174", "tcpPort": 9876, "status": "ACTIVE"},
                            {"id": "10.0.3.35",  "ip": "10.0.3.35",  "tcpPort": 9876, "status": "ACTIVE"}]}

        :param json_data: Input JSON string

        :return: Cluster object or None on error
        """

        # TODO: Implement this
        raise SyntaxError("Expected field %s not found. JSON:'%s'", ('XYZ', json_data))

        return None

    @classmethod
    def find_all_controllers(cls, ip_address, port_number=8181, username=DEFAULT_USERNAME, password=DEFAULT_PASSWORD):
        """
        Given one ONOS Controller address and credentials, find all (if any) other controllers
        in the cluster and return an ONOS Cluster object.  For each controller found, an
        appropriate ONOS Controller object will be created.

        :param ip_address:  IP Address or hostname for ONOS Controller
        :param port_number: Port number, default is 8181
        :param username:    Username to use for REST GET invocation, default is 'onos'
        :param password:    Password to use for REST GET invocation, default is 'rocks'

        :return: Cluster object with appropriate Controller objects created as needed
        """
        url = ulr_prefix + Cluster.__URL_LEAF
        response = requests.get(url, auth=(username, password))

        if response.status_code != requests.codes.ok:
            return None

        return cluster
