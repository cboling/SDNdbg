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
import logging
import pprint
import uuid

import ruamel.yaml as yaml


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

        self._name = 'SDNdbg.{}'.format(str(uuid.UUID()))
        self._seed_file = None
        self._log_level = 'info'
        self._sites = []

        # Continue with loading of the configuration file. If not present, try to load from
        # environment variables

        if 'config_file' in kwargs:
            self._config_data = self._load_file(kwargs['config_file'])
        else:
            self._config_data = Config._load_env_vars()

        if 'sites' not in self._config_data:
            raise KeyError("Unable to locate required key 'sites' in configuration file '{}'".format(filename))

        self._sites = Config._load_site(self._config_data['sites'])

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

        self._log_level = config.get('logging-level', self._log_level)

        logging.info('Configuration File: {} contains:\n{}'.format(filename,
                                                                   pprint.PrettyPrinter(indent=2).pformat(config)))
        self._name = config.get('name', self._name)
        self._seed_file = config.get('seed-file', self._seed_file)

        return config

    @staticmethod
    def _load_site(site_configs):
        """
        Create a collection of Site objects based on the configuration provided

        :param site_configs:

        :return: (list) Site configuration objects
        """
        from site import Config as SiteConfig
        sites = []

        for site in site_configs:
            sites.append(SiteConfig.create(site))

        return sites

    @property
    def get_sites(self):
        """
        Configuration data of all sites

        :return: (list) Site configuration objects
        """
        return self._sites
