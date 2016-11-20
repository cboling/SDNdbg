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
import collections
import logging
import os
import pprint

from core.node import Node
from core.utils import get_uuid


class Config(object):
    """
    Wraps Site specific configuration
    """

    def __init__(self, config_data, parent):
        self.name = config_data.get('name', '{}.Site.{}'.format(parent.name, str(get_uuid())))
        self.seed_file = config_data.get('seed-file', parent.seed_file)
        self.logging_level = config_data.get('logging-level', parent.logging_level)
        self.cache_client = config_data.get('cache-client', parent.cache_client)

        self.vims = self._load_vims(config_data.get('vims', []))
        self.sdn_controllers = self._load_sdns(config_data.get('sdn-controllers', []))
        self.ssh_username_and_passwords = Config._load_ssh(config_data.get('ssh-credentials', []))

    @staticmethod
    def create(config_data, parent):
        """
        Create a site object configuration object.  This call will recurse into any defined VIMS or
        SDN controller configs and parse those configs as well.

        :param config_data: (dict) Site Configuration dictionary
        :param parent: (Base) Higher level object that contains this site.  This parameter allows some
                              default values such as logging-level to default to same level as the parent
                              config if not explicitly overridden.
        :return: (Config) Site configuration object for the provided data
        """
        return Config(config_data, parent)

    @staticmethod
    def load_env_vars():
        """
        Load up our configuration based on common environment variables.

        Obviously can only handle a single Openstack and onos controller

        :return: (dict) Site configuration dictionary constructed from environment variables
        """
        # TODO: Move to openstack directory

        openstack_config = {
            'OS_AUTH_URL'           : os.environ.get('OS_AUTH_URL'),
            'OS_USERNAME'           : os.environ.get('OS_USERNAME'),
            'OS_PASSWORD'           : os.environ.get('OS_PASSWORD'),
            'OS_CA_PATH'            : os.environ.get('OS_CA_PATH'),
            'OS_PROJECT_DOMAIN_NAME': os.environ.get('OS_PROJECT_DOMAIN_NAME'),
            'OS_PROJECT_NAME'       : os.environ.get('OS_PROJECT_NAME',
                                                     os.environ.get('OS_TENANT_NAME')),
            'OS_REGION_NAME'        : os.environ.get('OS_REGION_NAME'),
            'OS_USER_DOMAIN_NAME'   : os.environ.get('OS_USER_DOMAIN_NAME'),
            'name'                  : 'OpenStack',
            'type'                  : 'OpenStack'
        }
        ssh = [
            {'username': os.environ.get('OS_USERNAME'),
             'password': os.environ.get('OS_PASSWORD')}
        ]
        # TODO: Move to ONOS directory
        sdn = []
        cnt = 1
        while os.environ.get('OC{}'.format(cnt)) is not None:
            item = {'type'    : 'ONOS',
                    'name'    : '{}-{}'.format(os.environ.get('ONOS_CELL'), cnt),
                    'username': os.environ.get('ONOS_USER'),
                    'password': os.environ.get('ONOS_WEB_PASS'),
                    'address' : os.environ.get('OC{}'.format(cnt)),
                    'port'    : 8181}
            sdn.append(item)
            cnt += 1

        config = {
            'name'           : os.environ.get('USER'),
            'sdn-controllers': sdn,
            'vims'           : [openstack_config],
            'ssh-credentials': ssh
        }
        return config

    def _load_vims(self, vim_configs):
        from openstack.config import Config as OpenStackConfig

        vim_loader = {
            'openstack': OpenStackConfig.create
        }
        vims = []

        for config in vim_configs:
            vims.append(vim_loader[config.get('type', 'unknown').lower()](config, self))

        return vims

    def _load_sdns(self, sdn_configs):
        from onos.config import Config as OnosConfig

        sdn_loader = {
            'onos': OnosConfig.create
        }
        sdn = []

        for config in sdn_configs:
            sdn.append(sdn_loader[config.get('type', 'unknown').lower()](config, self))

        return sdn

    @staticmethod
    def _load_ssh(ssh_configs):
        # TODO: Also support per machine/address credentials, not just a bunch to try
        ssh_username_and_passwords = collections.OrderedDict()

        for up_dict in ssh_configs:
            if 'username' in up_dict:
                ssh_username_and_passwords.update({up_dict['username']: up_dict.get('password', '')})

        return ssh_username_and_passwords


class Site(Node):
    """
    An OpenStack 'Site' represents a collection of OpenStack controllers that share a
    common geo-location.
    """

    def __init__(self, **kwargs):
        logging.info('Site.__init__: args:\n{}'.format(pprint.PrettyPrinter().pformat(kwargs)))

        # No VIMs/NFV infrastructure or SDN controllers yet.  Will populate during discovery
        # TODO: Do we want to keep these separate, or just all in the children base property/list

        self._vims = []
        self._sdn_controllers = []

        Node.__init__(self, **kwargs)

    @property
    def unique_id(self):
        """
        :return: (string) Globally Unique Name
        """
        return self.name

    @property
    def nfv_controllers(self):
        """
        This property provides all known VIM/NFV controllers in the network

        :return: (list) NFV Controller objects
        """
        return self._vims

    @property
    def sdn_controllers(self):
        """
        This property provides all known SDN controllers in the network

        :return: (list) SDN Controller objects
        """
        return self._sdn_controllers

    def connect(self):
        """

        :return:
        """
