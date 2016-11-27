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

import logging
import pprint

from core.node import Node
from interface import Interface


class Port(Node):
    """
    OpenVSwitch Port
    """

    def __init__(self, **kwargs):
        logging.info('OVS.Port.__init__: entry:\n{}'.format(pprint.PrettyPrinter().pformat(kwargs)))

        port_data = kwargs.get('port_data')

        kwargs['name'] = port_data['name']
        kwargs['id'] = str(port_data['_uuid'])
        kwargs['metadata'] = port_data

        Node.__init__(self, **kwargs)

        self._ssh_credentials = kwargs.get('ssh_credentials')
        self._ip = kwargs.get('ssh_address')
        self._interfaces = None

        # {'_uuid'          : UUID('7457b6ba-8c6d-4add-9538-7ab9edc6fb6e'),
        #  'bond_downdelay' : 0,
        #  'bond_fake_iface': False,
        #  'bond_mode'      : set([]),
        #  'bond_updelay'   : 0,
        #  'external_ids'   : {},
        #  'fake_bridge'    : False,
        #  'interfaces'     : UUID('ef743632-a9e2-4ff8-9fc0-570a15bd97d5'),
        #  'lacp'           : set([]),
        #  'mac'            : set([]),
        #  'name'           : 'br-ex',
        #  'other_config'   : {},
        #  'qos'            : set([]),
        #  'statistics'     : {},
        #  'status'         : {},
        #  'tag'            : set([]),
        #  'trunks'         : set([]),
        #  'vlan_mode'      : set([])},

    @staticmethod
    def get_ports(**kwargs):
        """
        Get all ports for the node identified by the ssh credentials
        """
        ports = kwargs.get('ovs_topology').get('port', [])
        port_ids = kwargs.get('port_ids', [])

        return [Port(port_data=port, **kwargs) for port in ports if port['_uuid'] in port_ids]

    @property
    def ovs_topology(self):
        return self.parent.ovs_topology

    @property
    def ssh_address(self):
        return self._ip

    @property
    def ssh_credentials(self):
        return self._ssh_credentials

    def get_interface(self, refresh=False):
        """
        Get all interfaces on this OVS node (should only be one)
        """
        if not refresh and self._interfaces is not None:
            return self._interfaces

        self._interfaces = Interface.get_interfaces(parent=self,
                                                    interface_ids=self.metadata['interfaces'],
                                                    address=self.ssh_address,
                                                    ssh_credentials=self._ssh_credentials,
                                                    ovs_topology=self.ovs_topology)
        return self._interfaces

    def connect(self):
        """
        No OVS client is needed, the base object already has all of the OVS data referenced.

        Just return a non-None value to indicate success
        """
        return 'OVS Port connect is n/a'

    def perform_sync(self):
        """
        Enumerate all of the interfaces associated with this OVS Port

        :return: True if synchronization was successful, False otherwise
        """
        # Snapshot the OVS subsystem. Should always have one?

        ovs_topology = None  # TODO self.get_ovs_topology(refresh=True)
        if ovs_topology is None:
            return False

        # Process all the ports on this switch

        # status = self.perform_sync_interface()
        status = False  # TODO Implement this
        # TODO: Anything else?

        return status
