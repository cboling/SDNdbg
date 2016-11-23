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


class OpenStackNode(Node):
    """
    Class to wrap an OpenStack node (system with a unique IP address).

    This is used to wrap KeyStone, Neutron, and Nova-compute service nodes and can wrap a single service
    or multiple.  All Services have the following properties in common.

    Property    Description
    --------    -----------------------------------------------------------------------------------
    Bridges     OVS, Linux, and other bridges. These can be part of the base operating system configuration
                or could have been created by Neutron networking. Also 'docker' and 'libvirt' may have also
                created some of these bridges. Note that not all may be part of the SDN/NFV environment

    Ports       Physical ports as well as virtual ports (vEths). Some could be part of the OS or created
                by Neutron or another package.  Note that not all may be part of the SDN/NFV environment

    Keystone Servers have the following unique properties:
    Property    Description
    --------    -----------------------------------------------------------------------------------
    Tenants     Project Tenants
    Instances   VM Instances running

    Neutron Servers have the following unique properties:
    Property    Description
    --------    -----------------------------------------------------------------------------------
    TODO:       Lots of work here to keep networks and subnets straight..

    Nova Compute Servers have the following unique properties:

    Property    Description
    --------    -----------------------------------------------------------------------------------

    """

    def __init__(self, **kwargs):
        logging.info('openstack.node.__init__: entry:\n{}'.format(pprint.PrettyPrinter().pformat(kwargs)))

        Node.__init__(self, **kwargs)

    @staticmethod
    def create(parent, **kwargs):
        logging.info('openstack.node.Create: entry:\n{}'.format(pprint.PrettyPrinter().pformat(kwargs)))

        kwargs['parent'] = parent
        return OpenStackNode(**kwargs)

    @property
    def ssh_address(self):
        """
        Get address/target for SSH commands

        :return: (String) IP or hostname
        """
        return self.config.get_address()

    @property
    def credentials(self):
        """
        Get OpenStack Credentials object

        :return: (Credentials) OpenStack admin access credentials
        """
        return self.config.to_credentials()

    def connect(self):
        """
        Create credentials for accessing and OpenStack Controller.  A variety of clients are used to work with
        OpenStack but at this level, we mainly need to enumerate all the services (and endpoints) that we
        will be acessing.  This requires a Keystone Client

        :return: (dict) Keystone Client and/or Nova Client
        """
        # TODO: Need to implement

        return None  # {'keystone': keystone, 'nova': nova} if keystone is not None and nova is not None else None

    def perform_sync(self):
        """
        A controller is made up of one or more machines running services that we care about.  There are
        a large number of OpenStack services, but we currently only care about a few.

        :return: True if synchronization was successful, False otherwise
        """
        if self.client is None:
            return False

        # TODO: Need to implement

        return False
