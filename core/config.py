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
import ruamel.yaml as yaml


class Config(object):
    """
    Wraps the configuration to read in
    """

    def __init__(self, config_file=None):
        self._name = 'Site'
        self._seed_file = None
        self._config_data = self._load_file(config_file) if config_file is not None else self._load_env_vars()

    def _load_file(self, filename):
        with open(filename, 'r') as f:
            config = yaml.load(f.read())

        logging.info('Configuration File: {} contains:\n{}'.format(filename,
                                                                   pprint.PrettyPrinter(indent=2).pformat(config)))

        if 'site' not in config:
            raise KeyError("Unable to locate required key 'site' in configuration file '{}'".format(filename))

        site = config['site']
        self._name = site.get('name', 'Site')
        self._seed_file = site.get('seed-file', None)
        self._vims = Config._load_vims(site.get('vims', []))
        self._sdn = Config._load_sdns(site.get('sdn-controllers', []))
        self._ssh = Config._load_ssh(site.get('ssh-credentials', []))

    def _load_env_vars(self):
        """
        Load up our configuration based on common environment variables.

        Obviously can only handle a single Openstack and onos controller
        """
        self._vims = Config._load_vims([{'OS_AUTH_URL': os.environ.get('OS_AUTH_URL'),
                                         'OS_USERNAME': os.environ.get('OS_USERNAME'),
                                         'OS_PASSWORD': os.environ.get('OS_PASSWORD'),
                                         'OS_CA_PATH': os.environ.get('OS_CA_PATH'),
                                         'OS_PROJECT_DOMAIN_NAME': os.environ.get('OS_PROJECT_DOMAIN_NAME'),
                                         'OS_PROJECT_NAME': os.environ.get('OS_PROJECT_NAME',
                                                                           os.environ.get('OS_TENANT_NAME')),
                                         'OS_REGION_NAME': os.environ.get('OS_REGION_NAME'),
                                         'OS_USER_DOMAIN_NAME': os.environ.get('OS_USER_DOMAIN_NAME'),
                                         'name': 'OpenStack',
                                         'type': 'OpenStack'}])

        self._ssh = Config._load_ssh([{'username': os.environ.get('OS_USERNAME'),
                                       'password': os.environ.get('OS_PASSWORD')}])

        sdn = []
        cnt = 1
        while os.environ.get('OC{}'.format(cnt)) is not None:
            item = {'type': 'ONOS',
                    'name': '{}-{}'.format(os.environ.get('ONOS_CELL'), cnt),
                    'username': os.environ.get('ONOS_USER'),
                    'password': os.environ.get('ONOS_WEB_PASS'),
                    'address': os.environ.get('OC{}'.format(cnt)),
                    'port': 8181}
            sdn.append(item)
            cnt += 1

        self._sdn = Config._load_sdns(sdn)

    @staticmethod
    def _load_vims(vim_configs):
        from openstack.config import Config as OpenStackConfig

        vim_loader = {
            'openstack': OpenStackConfig.create
        }
        vims = []

        for config in vim_configs:
            vims.append(vim_loader[config.get('type', 'unknown').lower()](config))

        return vims

    @staticmethod
    def _load_sdns(sdn_configs):
        from onos.config import Config as OnosConfig

        sdn_loader = {
            'onos': OnosConfig.create
        }
        sdn = []

        for config in sdn_configs:
            sdn.append(sdn_loader[config.get('type', 'unknown').lower()](config))

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

    @seed_file.setter
    def seed_file(self, value):
        self._seed_file = value
