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

class Switch(CoreSwitch):
    """
    Linux Bridge
    """
    def __init__(self, **kwargs):
        logging.info('Linux.Switch.__init__: entry:\n{}'.format(pprint.PrettyPrinter().pformat(kwargs)))

        CoreSwitch.__init__(self, **kwargs)

    @staticmethod
    def get_switches(**kwargs):
        """
        Get all bridges for the node identified by the ssh credentials
        """
        bridges = kwargs.get('ovs_topology').get('bridge', [])
        return [Switch(brctl_topology=bridge, **kwargs) for bridge in bridges]

    def connect(self):
        """
        No OVS client is needed, the base object already has all of the OVS data referenced.

        Just return a non-None value to indicate success
        """
        return 'Linux Bridge connect is n/a'

    def perform_sync(self):
        """

        :return: True if synchronization was successful, False otherwise
        """
        # Process all the ports on this switch

        status = self.perform_sync_ports()

        # TODO: Anything else?

        return status

    def perform_sync_ports(self):
        # # Load switches/bridges
        # ports = self.get_ports(refresh=True)
        #
        # # TODO: Remove old children not in new list first
        #
        # for port in ports:
        #     # TODO: Add if needed, also need to remove if no longer there
        #
        #     if port in self.children:
        #         # Existing child
        #         pass
        #     else:
        #         # New child
        #         self.children.append(port)

        return True
