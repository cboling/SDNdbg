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

import urllib3.util as urlutil

from core.utils import get_uuid, levelname_to_level
from credentials import Credentials


class Config(object):
    """
    Class used to wrap a set of OpenStack configuration information
    """

    def __init__(self, config_data, parent):
        self.type = 'OpenStack'
        self.config = self
        self.config_parent = parent

        self.name = config_data.get('name', '{}OpenStack.{}'.format(parent.name, str(get_uuid())))
        self.seed_file = config_data.get('seed-file', parent.seed_file)
        self.logging_level = config_data.get('logging-level', parent.logging_level)
        self.cache_client = config_data.get('cache-client', parent.cache_client)

        base_module_name = __name__[:-len(path.splitext(path.basename(__file__))[0]) - 1]
        logging.getLogger(base_module_name).setLevel(levelname_to_level(self.logging_level))

        self.auth_url = config_data.get('OS_AUTH_URL')
        self.username = config_data.get('OS_USERNAME')
        self.password = config_data.get('OS_PASSWORD')
        self.project = config_data.get('OS_PROJECT_NAME')
        self.region_name = config_data.get('OS_REGION_NAME')
        self.user_domain_name = config_data.get('OS_USER_DOMAIN_NAME')
        self.project_domain_name = config_data.get('OS_PROJECT_DOMAIN_NAME')
        self.certificate_path = config_data.get('OS_CA_PATH')

    @staticmethod
    def create(config_data, parent):
        """
        Create an OpenStack configuration object

        :param config_data: (dict) Site Configuration dictionary
        :param parent: (Base) Higher level object that contains this site.  This parameter allows some
                              default values such as logging-level to default to same level as the parent
                              config if not explicitly overridden.
        :return: (Config) Site configuration object for the provided data
        """
        return Config(config_data, parent)

    def to_credentials(self):
        return Credentials(self.username,
                           self.password,
                           self.auth_url,
                           self.project,
                           user_domain_name=self.user_domain_name,
                           project_domain_name=self.project_domain_name,
                           ca_path=self.certificate_path)

    def get_address(self):
        return urlutil.parse_url(self.auth_url).host

    def get_port(self):
        return urlutil.parse_url(self.auth_url).port
