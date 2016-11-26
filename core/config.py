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

import ruamel.yaml as yaml

from core.utils import get_uuid


class Config(object):
    """
    Wraps the configuration to read in
    """
    def __init__(self, **kwargs):
        """
        Create a configuration object

        TODO: Provide a full list of settable values and thier defaults

        :param kwargs: (dict) configuration parameters
        """
        # A few defaults
        self.name = 'SDNdbg.{}'.format(str(get_uuid()))
        self.seed_file = None
        self.logging_level = 'info'
        self.cache_client = False
        self.sites = []
        self.type = 'Global'
        self.config = self
        self.config_parent = None

        # TODO: Support a global list of username/passwords...

        # Continue with loading of the configuration file. If not present, try to load from
        # environment variables

        if 'config_file' in kwargs:
            self._config_data = self._load_file(kwargs['config_file'])

            if 'sites' not in self._config_data:
                raise KeyError("Unable to locate required key 'sites' in configuration file '{}'".
                               format(kwargs['config_file']))
        else:
            self._config_data = Config._load_env_vars()

        self.sites = self._load_site(self._config_data['sites'])

    @staticmethod
    def _load_env_vars():
        from site import Config as SiteConfig
        return {'sites': [SiteConfig.load_env_vars()]}

    def _load_file(self, filename):
        """
        Load the entire configuration from a user supplied YAML file

        :param filename: (string) Path to configuration file (YAML format)

        :return: (dict) YAML file converted into a dictionary
        """
        with open(filename, 'r') as f:
            config = yaml.load(f.read())

        self.logging_level = config.get('logging-level', self.logging_level)

        logging.debug('Configuration File: {} contains:\n{}'.format(filename,
                                                                    pprint.PrettyPrinter(indent=2).pformat(config)))
        self.name = config.get('name', self.name)
        self.seed_file = config.get('seed-file', self.seed_file)
        self.cache_client = config.get('cache-client', self.cache_client)

        return config

    def _load_site(self, site_configs):
        """
        Create a collection of Site objects based on the configuration provided

        :param site_configs:

        :return: (list) Site configuration objects
        """
        from site import Config as SiteConfig
        sites = []

        for site_config in site_configs:
            sites.append(SiteConfig.create(site_config, self))

        return sites

