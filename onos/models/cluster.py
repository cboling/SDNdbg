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

from core import json_decode
from core.logger import logger
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

    @staticmethod
    def create(uniqueId, name, username, password, json_data):
        """
        Create a Cluster object from JSON data and recurse into
        any found controllers and perform discovery of them as well.

        For the 1.4 ONOS Emu release, the expected JSON looks similar to the following:

        REST at: http://<ip-addr>:8181/onos/v1/cluster

        RESULT = {"nodes": [{"id": "10.0.3.175", "ip": "10.0.3.175", "tcpPort": 9876, "status": "ACTIVE"},
                            {"id": "10.0.3.174", "ip": "10.0.3.174", "tcpPort": 9876, "status": "ACTIVE"},
                            {"id": "10.0.3.35",  "ip": "10.0.3.35",  "tcpPort": 9876, "status": "ACTIVE"}]}

        :param uniqueId:  Unique ID for the cluster
        :param name:      A name for the cluster
        :param username:  Username to use for REST GET invocation, default is 'onos'
        :param password:  Password to use for REST GET invocation, default is 'rocks'
        :param json_data: JSON data for Cluster

        :return: (Cluster) The Cluster or None on error
        """
        if Cluster.__NODES not in json_data:
            raise SyntaxError("Expected field %s not found in Cluster JSON data: '%s'",
                              Cluster.__NODES, json_data)

        cluster = Cluster(uniqueId=id, name='TODO: need a name', rawData=json_data)

        for node in json_data[Cluster.__NODES]:
            # id = json_decode(json_data, Cluster.__ID, '', True)
            ip = json_decode(json_data, Cluster.__IP, '', True)
            # port = json_decode(json_data, Cluster.__PORT, '', True)
            port = DEFAULT_REST_PORT
            status_str = json_decode(json_data, Cluster.__STATUS, '', True)

            # TODO: Validate Status string and assign enumeration, then pass it into controller

            controller_name = 'ONOS [%s:%d]' % (ip, port)

            Controller.create(controller_name, ip, port, username, password,
                              status=Controller.ACTIVE, parent=cluster)

        return cluster

    @classmethod
    def find_all_controllers(cls, ip_address, port_number=None, username=None, password=None):
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
        port_number = get_default_rest_port() if port_number is None else port_number
        username = get_default_username() if username is None else username
        password = get_default_password() if password is None else password

        url = ulr_prefix(ip_address, port_number) + Cluster.__URL_LEAF

        response = requests.get(url, auth=(username, password))

        logger.info('Cluster: Request Status for %s: %s' % (url, str(response.status_code)))

        # TODO: Insert logging here

        if response.status_code != requests.codes.ok:
            # TODO: Should we throw an exception?
            return None

        cluster_id = 'Test-1234'  # TODO: A UUID or something else may be better...
        name = 'Test-987'  # TODO: A capture time or user input would be good here...

        return Cluster.create(cluster_id, name, username, password, response.json())
