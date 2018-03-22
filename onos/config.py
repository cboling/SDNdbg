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
from os import path

from core.utils import get_uuid, levelname_to_level
from credentials import OnosCredentials


class Config(object):
    """
    Class used to wrap a set of ONOS configuration information
    """

    def __init__(self, config_data, parent):
        self.type = 'ONOS'
        self.config = self
        self.config_parent = parent

        self.name = config_data.get('name', '{}.ONOS.{}'.format(parent.name, str(get_uuid())))
        self.seed_file = config_data.get('seed-file', parent.seed_file)
        self.logging_level = config_data.get('logging-level', parent.logging_level)
        self.cache_client = config_data.get('cache-client', parent.cache_client)

        base_module_name = __name__[:-len(path.splitext(path.basename(__file__))[0]) - 1]
        logging.getLogger(base_module_name).setLevel(levelname_to_level(self.logging_level))

        self.address = config_data.get('address')
        self.username = config_data.get('username', 'onos')
        self.password = config_data.get('password', 'rocks')
        self.port = config_data.get('port')

    @staticmethod
    def create(config_data, parent):
        """
        Create an ONOS SDN Controller(s) configuration object

        :param config_data: (dict) Site Configuration dictionary
        :param parent: (Base) Higher level object that contains this site.  This parameter allows some
                              default values such as logging-level to default to same level as the parent
                              config if not explicitly overridden.
        :return: (Config) Site configuration object for the provided data
        """
        return Config(config_data, parent)

    def to_credentials(self):
        return OnosCredentials(self.username,
                               self.password,
                               self.address,
                               self.port)

