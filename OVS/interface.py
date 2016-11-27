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


class Interface(Node):
    """
    OpenVSwitch Interface
    """

    def __init__(self, **kwargs):
        logging.info('OVS.Interface.__init__: entry:\n{}'.format(pprint.PrettyPrinter().pformat(kwargs)))

        self._intf_data = kwargs.get('interface_data')

        kwargs['name'] = self._bridge_data['name']
        kwargs['id'] = self._bridge_data['_uuid']

        Node.__init__(self, **kwargs)

        self._ssh_credentials = kwargs.get('ssh_credentials')
        self._ip = kwargs.get('ssh_address')
        self._type = self._intf_data['type']

    # {'_uuid'                 : UUID('4512037a-3b23-498a-a7be-c87297601b56'),
    #  'admin_state'           : 'up',
    #  'bfd'                   : {},
    #  'bfd_status'            : {},
    #  'cfm_fault'             : set([]),
    #  'cfm_fault_status'      : set([]),
    #  'cfm_flap_count'        : set([]),
    #  'cfm_health'            : set([]),
    #  'cfm_mpid'              : set([]),
    #  'cfm_remote_mpids'      : set([]),
    #  'cfm_remote_opstate'    : set([]),
    #  'duplex'                : set([]),
    #  'error'                 : set([]),
    #  'external_ids'          : {},
    #  'ifindex'               : 10,
    #  'ingress_policing_burst': 0,
    #  'ingress_policing_rate' : 0,
    #  'lacp_current'          : set([]),
    #  'link_resets'           : 1,
    #  'link_speed'            : set([]),
    #  'link_state'            : 'up',
    #  'mac'                   : set([]),
    #  'mac_in_use'            : 'b6:94:25:51:13:45',
    #  'mt'                    : 1500,
    #  'name'                  : 'br-ext',
    #  'ofport'                : 65534,
    #  'ofport_request'        : set([]),
    #  'options'               : {},
    #  'other_config'          : {},
    #  'statistics'            : {'collisions'  : 0,
    #                             'rx_bytes'    : 13036,
    #                             'rx_crc_err'  : 0,
    #                             'rx_dropped'  : 0,
    #                             'rx_errors'   : 0,
    #                             'rx_frame_err': 0,
    #                             'rx_over_err' : 0,
    #                             'rx_packets'  : 103,
    #                             'tx_bytes'    : 1910,
    #                             'tx_dropped'  : 0,
    #                             'tx_errors'   : 0,
    #                             'tx_packets'  : 37},
    #  'status'                : {'driver_name': 'openvswitch'},
    #  'type'                  : 'internal'},

    @staticmethod
    def get_interfaces(**kwargs):
        """
        Get all bridges for the node identified by the ssh credentials
        :return:
        """
        interfaces = kwargs.get('ovs_topology').get('interface', [])
        intf_ids = kwargs['parent'].ports

        return [Interface(interface_data=port, **kwargs) for port in ports if port['_uuid'] in port_ids]

    @property
    def type(self):
        return self._type

    @property
    def ovs_topology(self):
        return self.parent.ovs_topology

    @property
    def ssh_address(self):
        return self._ip

    @property
    def ssh_credentials(self):
        return self._ssh_credentials

    def connect(self):
        """
        No OVS client is needed, the base object already has all of the OVS data referenced.

        Just return a non-None value to indicate success
        """
        return 'OVS Interface connect is n/a'

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
