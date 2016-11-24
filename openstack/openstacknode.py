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
import socket

from keystoneclient.v3.services import Service
from novaclient.v2.hypervisors import Hypervisor
from urllib3.util import parse_url

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


# ########################################################################################################3
# Support classes to wrap OpenStack information related to Service and Compute nodes
# ########################################################################################################3


class NodeInfo(object):
    """
    Class to wrap an OpenStack node (service and/or compute) information
    """

    def __init__(self, info):
        """
        Initialization
        :param info: OpenStack (Service/Hypervisor) Object to wrap
        """
        self.id = str(info.id).lower()

    @staticmethod
    def create(service, **kwargs):
        """
        Create the appropriate Service or Compute Node wrappers for each item in the list

        :param service: (OpenStack objects) List of OpenStack Service/Compute nodes to wrap
        :return: (ComputeInfo or ServiceInfo)
        """
        if isinstance(service, list):
            return [ServiceInfo.create(srv, **kwargs) for srv in service]
        else:
            _info_ctors = {
                Service   : ServiceInfo,
                Hypervisor: ComputeInfo
            }
            return _info_ctors.get(type(service))(service, **kwargs)

    def to_dict(self):
        return self.__dict__


class ServiceInfo(NodeInfo):
    """
    Base class to wrap some common OpenStack service/compute-node information
    """

    def __init__(self, srv_info, **kwargs):
        logging.info('openstack.ServiceInfo.__init__: entry:\n{}'.format(pprint.PrettyPrinter().pformat(srv_info)))

        NodeInfo.__init__(self, srv_info)

        self.name = srv_info.name.lower()
        self.type = srv_info.type.lower()
        # self.id = srv_info.id.lower()
        self.description = srv_info.to_dict().get('description', '')
        self.enabled = srv_info.enabled
        self.ip = '0.0.0.0'
        self.endpoints = {}

        if 'endpoints' in kwargs:
            self.endpoints = {endpt.interface.lower(): {'url'    : endpt.url,
                                                        'id'     : endpt.id.lower(),
                                                        'enabled': endpt.enabled}
                              for endpt in kwargs['endpoints'] if endpt.service_id.lower() == self.id}

            # Attempt to get an ip address for one of the endpoint
            for endpt_type in ['admin', 'public', 'internal']:
                try:
                    if endpt_type in self.endpoints:
                        self.ip = socket.gethostbyname(parse_url(self.endpoints[endpt_type]['url']).host)
                        break
                except Exception:
                    pass


class ComputeInfo(NodeInfo):
    """
    Class to wrap Compute-Node specific information
    """

    def __init__(self, compute_info):
        """
        Initialization
        """
        NodeInfo.__init__(self, compute_info)

        # Pull common properties from object itself

        # self.id = compute_info.id.lower()
        self.name = compute_info.hypervisor_hostname
        self.status = compute_info.status
        self.state = compute_info.state

        # Pull less common properties from dictionary version
        cd = compute_info.to_dict()
        self.ip = cd.get('host_ip')
        self.service = cd.get('service')

        self.cpu_info = {'info'            : cd.get('cpu_info'),
                         'type'            : cd.get('hypervisor_type'),
                         'current_workload': cd.get('current_workload'),
                         'vcpus'           : cd.get('vcpus'),
                         'vcpus_used'      : cd.get('vcpus_used'),
                         }
        self.disk_info = {'disk_available_least': cd.get('disk_available_least'),
                          'free_disk_gb'        : cd.get('free_disk_gb'),
                          'local_gb'            : cd.get('local_gb'),
                          'local_gb_used'       : cd.get('local_gb_used')
                          }
        self.memory_info = {'free_ram_mb'   : cd.get('free_ram_mb'),
                            'memory_mb'     : cd.get('memory_mb'),
                            'memory_mb_used': cd.get('memory_mb_used')
                            }
