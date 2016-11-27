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

from core.switch import Switch as CoreSwitch
from port import Port


class Switch(CoreSwitch):
    """
    Base class for nodes that support bridging functionality
    """

    def __init__(self, **kwargs):
        logging.info('OVS.Bridge.__init__: entry:\n{}'.format(pprint.PrettyPrinter().pformat(kwargs)))

        self._bridge_data = kwargs.get('bridge_data')

        kwargs['name'] = self._bridge_data['name']
        kwargs['id'] = self._bridge_data['_uuid']

        CoreSwitch.__init__(self, **kwargs)

        self._ovs_topology = kwargs.get('ovs_topology')
        self._ports = None

        # {'_uuid'                : UUID('be01ca55-ed5d-4dcf-8899-db082e3bc2b2'),
        #  'controller'           : UUID('96edd47c-1275-4355-b5e5-b075860cfa0e'),
        #  'datapath_id'          : '000056ca01becf4d',
        #  'datapath_type'        : 'system',
        #  'external_ids'         : {},
        #  'fail_mode'            : 'secure',
        #  'flood_vlans'          : set([]),
        #  'flow_tables'          : {},
        #  'ipfix'                : set([]),
        #  'mcast_snooping_enable': False,
        #  'mirrors'              : set([]),
        #  'name'                 : 'br-tun',
        #  'netflow'              : set([]),
        #  'other_config'         : {},
        #  'ports'                : set([UUID('a7be7b97-74fb-49e7-abcf-19d97a4a4632')]),
        #  'protocols'            : set(['OpenFlow10', 'OpenFlow13']),
        #  'sflow'                : set([]),
        #  'status'               : {},
        #  'stp_enable'           : False},

    @staticmethod
    def get_switches(**kwargs):
        """
        Get all OVS bridges for the node identified by the ssh credentials
        :return:
        """
        bridges = kwargs.get('ovs_topology').get('bridge', [])

        return [Switch(bridge_data=bridge, **kwargs) for bridge in bridges]

    @property
    def ovs_topology(self):
        return self._ovs_topology

    def get_ports(self, refresh=False):
        """
        Get all ports on this OVS node

        :param refresh: (boolean) If true, force refresh of all items
        :return: (list) of port nodes
        """
        if not refresh and self._ports is not None:
            return self._ports

        self._ports = Port.get_ports(parent=self,
                                     port_ids=self._bridge_data['ports'],
                                     address=self.ssh_address,
                                     ssh_credentials=self._ssh_credentials,
                                     ovs_topology=self.ovs_topology)
        return self._ports

    def connect(self):
        """
        No OVS client is needed, the base object already has all of the OVS data referenced.

        Just return a non-None value to indicate success
        """
        return 'OVS Switch connect is n/a'

    def perform_sync(self):
        """
        Enumerate all of the ports associated with this OVS Switch

        :return: True if synchronization was successful, False otherwise
        """
        # Snapshot the OVS subsystem. Should always have one?

        ovs_topology = None  # TODO self.get_ovs_topology(refresh=True)
        if ovs_topology is None:
            return False

        # Process all the ports on this switch

        status = self.perform_sync_ports()

        # TODO: Anything else?

        return status

    def perform_sync_ports(self):
        # Load switches/bridges
        ports = self.get_ports(refresh=True)

        # TODO: Remove old children not in new list first

        for port in ports:
            # TODO: Add if needed, also need to remove if no longer there

            if port in self.children:
                # Existing child
                pass
            else:
                # New child
                self.children.append(port)

        return True
