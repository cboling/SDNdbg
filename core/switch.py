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

import logging
import pprint

from core.node import Node


class Switch(Node):
    """
    Base class for nodes that support bridging functionality
    """

    def __init__(self, **kwargs):
        logging.info('Bridge.__init__: entry:\n{}'.format(pprint.PrettyPrinter().pformat(kwargs)))

        Node.__init__(self, **kwargs)

        self._ssh_credentials = kwargs.get('ssh_credentials')
        self._ip = kwargs.get('ssh_address')

    @staticmethod
    def get_switches(**kwargs):
        """
        Get all bridges/switches for the node identified by the ssh credentials

        :return: (list) Switch objects
        """
        from OVS.switch import Switch as OvsSwitch
        from linux.switch import Switch as LinuxBridge

        # TODO: What can neutron provide us that OVS/Linux cannot?

        return OvsSwitch.get_switches(**kwargs) + LinuxBridge.get_switches(**kwargs)

    @property
    def ssh_address(self):
        return self._ip

    @property
    def ssh_credentials(self):
        return self._ssh_credentials
