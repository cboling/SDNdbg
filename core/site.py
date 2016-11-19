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
import os
import uuid

from core.node import Node


class Config(object):
    """
    Wraps Site specific configuration
    """

    def __init__(self, site, parent):
        self._parent = parent

        self._name = site.get('name', 'Site.{}'.format(str(uuid.UUID())))
        self._seed_file = site.get('seed-file', parent.seed_file)
        self._log_level = site.get('logging-level', parent.logging_level)

        self._vims = self._load_vims(site.get('vims', []))
        self._sdn = self._load_sdns(site.get('sdn-controllers', []))
        self._ssh = Config._load_ssh(site.get('ssh-credentials', []))

    @staticmethod
    def create(parent, config_data):
        """
        Create a site object based on the provided configuration

        :param config_data: (dict) Site Configuration dictionary
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
            vims.append(vim_loader[config.get('type', 'unknown').lower()](self, config))

        return vims

    def _load_sdns(self, sdn_configs):
        from onos.config import Config as OnosConfig

        sdn_loader = {
            'onos': OnosConfig.create
        }
        sdn = []

        for config in sdn_configs:
            sdn.append(sdn_loader[config.get('type', 'unknown').lower()](self, config))

        return sdn

    @staticmethod
    def _load_ssh(ssh_configs):
        # TODO: Also support per machine/address credentials, not just a bunch to try
        ssh_username_and_passwords = collections.OrderedDict()

        for up_dict in ssh_configs:
            if 'username' in up_dict:
                ssh_username_and_passwords.update({up_dict['username']: up_dict.get('password', '')})

        return ssh_username_and_passwords

    @property
    def name(self):
        return self._name

    @property
    def vims(self):
        return self._vims

    @property
    def sdn_controllers(self):
        return self._sdn

    @property
    def ssh_username_and_passwords(self):
        return self._ssh

    @property
    def seed_file(self):
        return self._seed_file

    @property
    def logging_level(self):
        return self._log_level


class Site(Node):
    """
    An OpenStack 'Site' represents a collection of OpenStack controllers that share a
    common geo-location.
    """
    def __init__(self, config):
        Node.__init__(self, '')

        self.site_name = 'Site: {}'.format(config.name)
        self.config = config

    @staticmethod
    def default_site():
        return Site()

    @property
    def parent(self):
        """
        Parent objects
        :return: parent
        """
        return None

    @property
    def children(self):
        """
        Child objects.  For a site, this is a list of all VIM Controllers
        :return: (list) of children
        """
        return self.controllers

    @property
    def unique_id(self):
        """
        :return: (string) Globally Unique Name
        """
        return self.name

    @property
    def name(self):
        """
        :return: (string) Human readable name for node
        """
        return self.site_name

    @property
    def controllers(self):
        """
        This property provides all known controllers in the network.  Currently provided
        by the configuration file

        :return: (list) server objects
        """
        from openstack.controller import Controller

        if self.my_controllers is None:
            self.my_controllers = Controller.controllers(self, self.config)

        return self.my_controllers
