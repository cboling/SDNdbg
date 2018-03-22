# Copyright (c) 2015 - present.  Boling Consulting Solutions, BCSW.net
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import unicode_literals

import logging
import pprint
import socket

from keystoneclient.v3.services import Service
from novaclient.v2.hypervisors import Hypervisor
from urllib3.util import parse_url

from OVS.client import Client as OvsClient
from core.node import Node
from core.switch import Switch
from linux.client import Client as BrctlClient


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

    Links

    Keystone Servers have the following unique properties:
    Property    Description
    --------    -----------------------------------------------------------------------------------
    Tenants     Project Tenants

    Neutron Servers have the following unique properties:
    Property    Description
    --------    -----------------------------------------------------------------------------------
    TODO:       Lots of work here to keep networks and subnets straight..

    Nova Compute Servers have the following unique properties:

    Property    Description
    --------    -----------------------------------------------------------------------------------
    Instances   VM Instances running
    """

    def __init__(self, **kwargs):
        logging.debug('openstack.node.__init__: entry:\n{}'.format(pprint.PrettyPrinter().pformat(kwargs)))

        Node.__init__(self, **kwargs)
        self._service_info = kwargs.get('service_info')  # A List of tuples -> (service-type, NodeInfo obj)
        self._ip = kwargs.get('ip_address')
        self._openstack_credentials = kwargs.get('credentials')
        self._ssh_credentials = kwargs.get('ssh_credentials')
        self._ssh_valid = False
        self._ovs_topology = None
        self._brctl_topology = None
        self._switches = None
        self._ports = None
        self._links = None
        self._projects = None
        self._instances = None

    @staticmethod
    def create(parent, **kwargs):
        logging.info('openstack.node.Create: entry:\n{}'.format(pprint.PrettyPrinter().pformat(kwargs)))

        kwargs['parent'] = parent
        kwargs['name'] = '{} - {}'.format(kwargs['ip_address'],
                                          NodeInfo.service_names(kwargs['service_info']))
        kwargs['config'] = parent.config

        return OpenStackNode(**kwargs)

    @property
    def ssh_address(self):
        return self._ip

    @property
    def ssh_username(self):
        return self._ssh_credentials.username

    @property
    def ssh_password(self):
        return self._ssh_credentials.password

    @property
    def edges(self):
        """
        Get all edges (links) associated with this node

        :return: (list) Links
        """
        return self.get_links()

    @property
    def credentials(self):
        """
        Get OpenStack Credentials object

        :return: (Credentials) OpenStack admin access credentials
        """
        return self._openstack_credentials

    def get_ovs_topology(self, refresh=False):
        """
        Get all the entire OVS database of interest for this node.  Centralized here since
        it is the focal point for the local system

        :param refresh: (boolean) If true, force refresh of all items
        :return: (list) of bridge nodes
        """
        if not refresh and self._ovs_topology is not None:
            return self._ovs_topology

        if 'ssh' not in self.client or self.client['ssh'] is None:
            return None  # TODO: Probably best to throw an exception

        self._ovs_topology = OvsClient.get_topology(self.ssh_address, self.ssh_username, self.ssh_password)
        return self._ovs_topology

    def get_brctl_topology(self, refresh=False):
        """
        Get all the entire linux bridge configuration.  Centralized here since
        it is the focal point for the local system

        :param refresh: (boolean) If true, force refresh of all items
        :return: (list) of bridge nodes
        """
        if not refresh and self._brctl_topology is not None:
            return self._brctl_topology

        if 'ssh' not in self.client or self.client['ssh'] is None:
            return None  # TODO: Probably best to throw an exception

        self._brctl_topology = BrctlClient.get_topology(self.ssh_address, self.ssh_username, self.ssh_password)
        return self._brctl_topology

    def get_switches(self, refresh=False):
        """
        Get all bridges (OVS & Linux) for this node.
        All nodes will have zero or more bridges associated to them

        :param refresh: (boolean) If true, force refresh of all items
        :return: (list) of bridge nodes
        """
        if not refresh and self._switches is not None:
            return self._switches

        if 'ssh' not in self.client or self.client['ssh'] is None:
            return None  # TODO: Probably best to throw an exception

        self._switches = Switch.get_switches(parent=self,
                                             address=self.ssh_address,
                                             ssh_credentials=self._ssh_credentials,
                                             ovs_topology=self._ovs_topology,
                                             brctl_topology=self._brctl_topology)
        return self._switches

    def get_ports(self, refresh=False):
        """
        Get all networking ports (physical and veths) for this node.
        All nodes will have one or more ports associated to them

        :param refresh: (boolean) If true, force refresh of all items
        :return: (list) of port nodes
        """
        if not refresh and self._ports is not None:
            return self._ports

        self._ports = []  # TODO: Need to implement

        return self._ports

    def get_links(self, refresh=False):
        """
        Get all networking links (physical and veths) for this node.
        All nodes will have one or more links associated to them

        :param refresh: (boolean) If true, force refresh of all items
        :return: (list) of link nodes
        """
        if not refresh and self._links is not None:
            return self._links

        self._links = []  # TODO: Need to implement

        # TODO: Once SDN controllers supported, check OVS and other flows for duplicates

        return self._links

    def get_projects(self, refresh=False):
        """
        Get all projects/tenants for this node.
        Available on KeyStone nodes only

        :param refresh: (boolean) If true, force refresh of all items
        :return: (list) of project nodes
        """
        if (not refresh and self._projects is not None) or not self.supports_service('keystone'):
            return self._projects

        self._projects = []  # TODO: Need to implement

        return self._projects

    def get_instances(self, refresh=False):
        """
        Get all VM instances for this node.
        Nova API and Nova compute nodes support VM instances

        :param refresh: (boolean) If true, force refresh of all items
        :return: (list) of instance nodes
        """
        if not refresh and self._instances is not None:
            return self._instances

        # TODO: Need to experiment with Nova Cells v2 and instances that fail to launch

        if not self.supports_service('compute'):
            return None

        self._instances = []  # TODO: Need to implement

        return self._instances

    def supports_service(self, service):
        """
        Search through service list and return true if given service is supported

        :param service: (unicode) Service to match (case-insensitive)
        :return: True if the services list has the requested service
        """
        for srv in self._service_info:
            if srv[1].name.lower() == service.lower():
                return True
            if isinstance(srv[1], ComputeInfo) and service.lower() == 'compute':
                return True
        return False

    def set_ssh_credentials(self):
        # For SSH, determine find a matching username password
        if self._ssh_valid:
            return

        user_pwd_list = self._ssh_credentials.get_ssh_credentials(self.ssh_address)

        for username, password in user_pwd_list.items():
            ssh_client = self._ssh_credentials.ssh_client(self.ssh_address, username, password)

            if ssh_client is not None:
                ssh_client.close()

                # Cached the last ones we used successfully
                self._ssh_credentials.save_ssh_creds(self.ssh_address, username, password)
                self._ssh_valid = True
                return

    def connect(self):
        """
        Create credentials for accessing and OpenStack Controller.  A variety of clients are used to work with
        OpenStack but at this level, we mainly need to enumerate all the services (and endpoints) that we
        will be acessing.  This requires a Keystone Client

        :return: (dict) Keystone Client and/or Nova Client
        """
        keystone = self.credentials.keystone_client if self.supports_service('keystone') else None
        nova = self.credentials.nova_client if self.supports_service('compute') else None

        self.set_ssh_credentials()
        ssh = {'username': self.ssh_username, 'password': self.ssh_password}

        return {'keystone': keystone, 'nova': nova, 'ssh': ssh}

    def perform_sync(self):
        """
        A controller is made up of one or more machines running services that we care about.  There are
        a large number of OpenStack services, but we currently only care about a few.

        :return: True if synchronization was successful, False otherwise
        """
        if self.client is None:
            return False

        # Snapshot the OVS subsystem.  It may not exist but we will always create a basic one and
        # use it as the basis of the entire topology.  Other commands and interfaces will augment the
        # existing data and create some new first-level items (such as 'VMs')

        brctl_topology = self.get_brctl_topology(refresh=True)
        if brctl_topology is None:
            return False

        ovs_topology = self.get_ovs_topology(refresh=True)
        if ovs_topology is None:
            return False

        # First all bridges and switches

        status = self.perform_sync_switches()

        # TODO: Need to implement lots more !!!

        return status

    def perform_sync_switches(self):
        # Load switches/bridges
        switches = self.get_switches(refresh=True)

        # TODO: Remove old children not in new list first

        for switch in switches:
            # TODO: Add if needed, also need to remove if no longer there

            if switch in self.children:
                # Existing child
                pass
            else:
                # New child
                self.children.append(switch)

        return True

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

    def __repr__(self):
        return '%s.(%s, type: %s, ip: %s, descr: %s, %r)' % (self.__class__, self.name, self.type,
                                                             self.ip, self.description, self.__dict__)

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

    @staticmethod
    def service_names(services):
        """
        Convert service types to names
        :param services: (list or inst) Each instances is a tuple composed of (Service Type, NodeInfo object)
        :return: (unicode) Service types converted to names
        """

        if isinstance(services, list):
            output = ''
            for srv in services:
                output += '{}{}'.format('' if len(output) == 0 else ' - ',
                                        NodeInfo.service_names(srv))
            return output

        else:
            return '{}/{}'.format(services[1].name, services[1].type)

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def description(self):
        return self._description

    @property
    def enabled(self):
        return self._enabled

    @property
    def ip(self):
        return self._ip

    def to_dict(self):
        return self.__dict__


class ServiceInfo(NodeInfo):
    """
    Base class to wrap some common OpenStack service/compute-node information
    """
    def __init__(self, srv_info, **kwargs):
        NodeInfo.__init__(self, srv_info)

        self._name = srv_info.name.lower()
        self._type = srv_info.type.lower()
        self._description = srv_info.to_dict().get('description', '')
        self._enabled = srv_info.enabled
        self._ip = '0.0.0.0'
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
                        self._ip = socket.gethostbyname(parse_url(self.endpoints[endpt_type]['url']).host)
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

        self._name = compute_info.hypervisor_hostname
        self._description = 'Compute Node at {}'.format(self.name)
        self._type = 'compute-{}'.format(self.id)
        self.status = compute_info.status
        self.state = compute_info.state

        # Pull less common properties from dictionary version
        cd = compute_info.to_dict()
        self._ip = cd.get('host_ip')
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

    @property
    def enabled(self):
        return self.status.lower() == 'enabled'
