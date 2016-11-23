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

from deepdiff import DeepDiff
from keystoneclient.exceptions import ConnectionError, Unauthorized
from urllib3.util import parse_url

from core.controller import Controller as CoreController
from openstacknode import OpenStackNode

# Service name to type
_services_of_interest = {
    'keystone': 'identity',  # TODO: Add method to create/select node
    'neutron': 'network',
    # 'nova':   'compute',            # Compute nodes handled separately
    # 'heat':   'orchestration',      # TODO: Heat/Tacker support is future
    # 'tacker': 'orchestration'
}
# TODO: Look into following services: heat-cfg, nova_legacy
# TODO: Any need to support the following: glance, cinder, switch, ceilometer, ...


class Controller(CoreController):
    def __init__(self, **kwargs):
        logging.info('openstack.Controller.__init__: entry:\n{}'.format(pprint.PrettyPrinter().pformat(kwargs)))

        CoreController.__init__(self, **kwargs)

        self._process_services_list = self.process_initial_servers
        self._topology = 'unknown'  # Could be 'all-in-one' or 'multi-node'

    @staticmethod
    def create(**kwargs):
        logging.info('openstack.Controller.Create: entry:\n{}'.format(pprint.PrettyPrinter().pformat(kwargs)))
        return Controller(**kwargs)

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

    @property
    def topology(self):
        """
        Type of openstack topology
        :return: (string) 'unknown', 'all-in-one', or 'multi-node'
        """
        return self._topology

    def connect(self):
        """
        Create credentials for accessing and OpenStack Controller.  A variety of clients are used to work with
        OpenStack but at this level, we mainly need to enumerate all the services (and endpoints) that we
        will be acessing.  This requires a Keystone Client

        :return: (dict) Keystone Client & Nova Client
        """
        keystone = self.credentials.keystone_client
        nova = self.credentials.nova_client
        return {'keystone': keystone, 'nova': nova} if keystone is not None and nova is not None else None

    def perform_sync(self):
        """
        A controller is made up of one or more machines running services that we care about.  There are
        a large number of OpenStack services, but we currently only care about a few.

        :return: True if synchronization was successful, False otherwise
        """
        if self.client is None:
            return False

        services, compute_nodes = self.get_openstack_services()

        if services is not None or compute_nodes is not None:
            # Process the servers
            return self._process_services_list(services, compute_nodes)

        return False

    def get_openstack_services(self):
        """
        Get a list of services and their endpoints for this controller

        :return: (dict) Dictionary of services with service name as key.
        """
        keystone_client = self.client['keystone']
        nova_client = self.client['nova']

        # Bypass 'subjectAltName' warning.  See https://github.com/shazow/urllib3/issues/497 for more detail
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                service_list = keystone_client.services.list()
                endpoint_list = keystone_client.endpoints.list()
                hypervisor_list = nova_client.hypervisors.list()

            except ConnectionError as ex:
                logging.warning('OpenStack.get_openstack_servers[{}]: Connection Error: {}'.format(self, ex.message))
                return None

            except Unauthorized as ex:
                logging.warning('OpenStack.get_openstack_servers[{} - {}/{}]: Unauthorized: {}'.
                                format(self, self.config.username, self.config.password, ex.message))
                return None

            except Exception as e:
                logging.exception('Error accessing keystone endpoint services')
                return None

        # Collect information on services all services (for metadata).  Note that 'description'
        # may not be available in all service items

        services = {srv.name.lower(): {'enabled': srv.enabled,
                                       'description': srv.to_dict().get('description', ''),
                                       'id': srv.id.lower(),
                                       'type': srv.type.lower(),
                                       'endpoints': {}
                                       } for srv in service_list}

        logging.debug('OpenStack Controller: DBG Services:\n{}'.format(pprint.PrettyPrinter().
                                                                       pformat(services)))

        # For these services, collect endpoint information to see if they are local or are running
        # in a container/vm/server elsewhere

        for key, val in services.items():
            services[key]['endpoints'] = {endpt.interface.lower(): {'url': endpt.url,
                                                                    'id': endpt.id.lower(),
                                                                    'enabled': endpt.enabled}
                                          for endpt in endpoint_list if endpt.service_id.lower() == val['id']}

        logging.debug('OpenStack Controller: Final DBG Services:\n{}'.format(pprint.PrettyPrinter().
                                                                             pformat(services)))

        # Mix in compute nodes (hypervisors) as well

        compute_nodes = {}
        for hv in hypervisor_list:
            cd = hv.to_dict()
            compute_nodes['compute-{}'.format(cd['id'])] = {
                'name': cd.get('hypervisor_hostname'),
                'ip': cd.get('host_ip'),
                'status': cd.get('status'),
                'state': cd.get('state'),
                'cpu_info': cd.get('cpu_info'),
                'current_workload': cd.get('current_workload'),
                'type': cd.get('hypervisor_type'),

                'free_disk_gb': cd.get('free_disk_gb'),
                'free_ram_mb': cd.get('free_ram_mb'),
                'memory_mb': cd.get('memory_mb'),
                'memory_mb_used': cd.get('memory_mb_used'),

                'disk_available_least': cd.get('disk_available_least'),
                'local_gb': cd.get('local_gb'),
                'local_gb_used': cd.get('local_gb_used'),

                'service': cd.get('service'),
                'vcpus': cd.get('vcpus'),
                'vcpus_used': cd.get('vcpus_used')
            }
            logging.debug('Hypervisor: {}:\n{}'.format(hv.hypervisor_hostname,
                                                       pprint.PrettyPrinter(indent=2).pformat(hv.to_dict())))

        return services, compute_nodes

    def process_initial_servers(self, services, compute_nodes):
        """
        This method is called during synchronization the first time the servers list is created

        :param services: (dict) Collection of service and endpoint information
        :param compute_nodes: (dict) Collection of compute nodes

        :return: True if synchronization was successful, False otherwise
        """
        logging.debug('OpenStack.controller: process_initial_servers:')
        logging.debug('     Services\n{}'.format(pprint.PrettyPrinter().pformat(services)))
        logging.debug('     Computes\n{}'.format(pprint.PrettyPrinter().pformat(compute_nodes)))

        self.metadata['services'] = services
        self.metadata['compute_nodes'] = compute_nodes

        services_of_interest = {srv: val for srv, val in services.items() if srv in _services_of_interest}
        logging.debug('OpenStack.controller: interesting services:\n{}'.
                      format(pprint.PrettyPrinter().pformat(services_of_interest)))

        # Collect IP Addresses of each service and compute node

        service_ips = Controller.get_services_and_ips(services_of_interest, compute_nodes)

        rollup = {}
        for name, ip in service_ips.items():
            if str(ip) not in rollup:
                rollup[str(ip)] = []
                rollup[str(ip)].append(services[name] if name in services else compute_nodes[name])

        logging.info('IP rollup is:\n{}'.format(pprint.PrettyPrinter(indent=2).pformat(rollup)))
        self._topology = 'all-in-one' if len(rollup) == 1 else 'multi-node'

        for ip, item in rollup.items():
            os_node = OpenStackNode.create(self, **{ip: item})
            self.children.append(os_node)

        # TODO: Implement this
        # Now that we have an initial set of servers, process then differently on any update/refresh

        self._process_services_list = self.process_server_list
        return True

    def process_server_list(self, services, compute_nodes):
        """
        This method is called during synchronization for periodic update of servers list (after they
        are discovered of course.

        :param services: (dict) Collection of service and endpoint information
        :param compute_nodes: (dict) Collection of compute nodes

        :return: True if synchronization was successful, False otherwise
        """
        logging.debug('OpenStack.controller: process_server_list:\n{}'.format(pprint.PrettyPrinter().
                                                                              pformat(services)))
        old_services = self.metadata['services']
        old_computes = self.metadata['compute_nodes']

        self.metadata['services'] = services
        self.metadata['compute_nodes'] = compute_nodes

        services_deltas = DeepDiff(old_services, services)
        compute_deltas = DeepDiff(old_computes, compute_nodes)

        logging.debug('OpenStack.controller: process_server_list: service deltas:\n{}'.
                      format(pprint.PrettyPrinter(indent=2).pformat(services_deltas)))

        logging.debug('OpenStack.controller: process_server_list: compute deltas:\n{}'.
                      format(pprint.PrettyPrinter(indent=2).pformat(compute_deltas)))

        # TODO: Get a list of deltas

        # TODO: Kill children related to any ones that are missing in the new list
        # TODO: Spawn new children for any new ones in the list
        # TODO: Process differences in ones that match existing entries but important values may have changed

        return True

    @staticmethod
    def get_services_and_ips(services, compute_nodes):
        service_ips = {}

        for name, data in services.items():
            url = data['endpoints']['admin']['url'] if 'admin' in data['endpoints'] \
                else data['endpoints']['public']['url'] if 'public' in data['endpoints'] \
                else data['endpoints']['internal']['url']

            service_ips[name] = socket.gethostbyname(parse_url(url).host) if url is not None else '0.0.0.0'

        for name, data in compute_nodes.items():
            service_ips[name] = data['ip'] if data['ip'] is not None else socket.gethostbyname(data['name'])

        logging.info('Service IPs:\n{}'.format(pprint.PrettyPrinter(2).pformat(service_ips)))

        return service_ips
