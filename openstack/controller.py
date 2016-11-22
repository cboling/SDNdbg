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

from keystoneclient.exceptions import ConnectionError, ConnectionRefused, Unauthorized

from core.controller import Controller as CoreController

# Service name to type
_services_of_interest = {
    'keystone': 'identity',
    'nova'    : 'compute',
    'neutron' : 'network',
    # 'heat': 'orchestration',      # TODO: Heat/Tacker support is future
    # 'tacker': 'orchestration'
}
# TODO: Look into following services: heat-cfg, nova_legacy
# TODO: Any need to support the following: glance, cinder, switch, ceilometer, ...


class Controller(CoreController):
    def __init__(self, **kwargs):
        logging.info('openstack.Controller.__init__: entry:\n{}'.format(pprint.PrettyPrinter().pformat(kwargs)))

        CoreController.__init__(self, **kwargs)

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

    def connect(self):
        """
        Create credentials for accessing and OpenStack Controller.  A variety of clients are used to work with
        OpenStack but at this level, we mainly need to enumerate all the services (and endpoints) that we
        will be acessing.  This requires a Keystone Client

        :return: (KeystoneCLient) Keystone Client
        """
        return self.credentials.keystone_client

    def perform_sync(self):
        """
        A controller is made up of one or more machines running services that we care about.  There are
        a large number of OpenStack services, but we currently only care about a few.

        :return: True if synchronization was successful, False otherwise
        """
        if self.client is None:
            return False

        servers = self.get_openstack_servers()

        return False

    def get_openstack_servers(self):
        keystone_client = self.client

        # Bypass 'subjectAltName' warning.  See https://github.com/shazow/urllib3/issues/497 for more detail
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                services = keystone_client.services.list()
                endpoints = keystone_client.endpoints.list()

            except ConnectionError as ex:
                logging.warning('OpenStack.get_openstack_servers[{}]: Connection Error: {}'.format(self, ex.message))
                return None

            except ConnectionRefused as ex:
                logging.warning('OpenStack.get_openstack_servers[{}]: Connection Refused: {}'.format(self, ex.message))
                return None

            except Unauthorized as ex:
                logging.warning('OpenStack.get_openstack_servers[{} - {}/{}]: Unauthorized: {}'.
                                format(self, self.config.username, self.config.password, ex.message))
                return None

            except Exception as e:
                logging.exception('Error accessing keystone endpoint services')
                return None

        # Collect information on services of interest

        dbg_services = [srv for srv in services if srv.name.lower() in _services_of_interest]
        dbg_ids = [srv.id for srv in dbg_services]

        # For these services, collect endpoint information to see if they are local or are running
        # in a container/vm/server elsewhere

        dgb_endpoints = [endpt for endpt in endpoints if endpt.service_id in dbg_ids and
                         endpt.interface.lower() == 'public']

        logging.info('OpenStack Controller: DBG Endpoints:\n{}'.format(pprint.PrettyPrinter().
                                                                       pformat(dgb_endpoints)))
        # Now create a list of tuples that have our service name and url

        servers = []

        # for endpt in dbgE

        raise NotImplementedError('TODO: Implement this')
