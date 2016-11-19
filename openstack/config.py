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
import urllib3.util as urlutil

from credentials import OpenStackCredentials


class Config(object):
    """
    Class used to wrap a set of openstack configuration information
    """

    def __init__(self, parent, input_data):
        self._parent = parent
        self._seed_file = input_data.get('seed-file', parent.seed_file)
        self._log_level = input_data.get('logging-level', parent.logging_level)

        self._name = input_data.get('name', 'OpenStack')
        self._auth_url = input_data.get('OS_AUTH_URL')
        self._username = input_data.get('OS_USERNAME')
        self._password = input_data.get('OS_PASSWORD')
        self._project = input_data.get('OS_PROJECT_NAME')
        self._region_name = input_data.get('OS_REGION_NAME')
        self._user_domain_name = input_data.get('OS_USER_DOMAIN_NAME')
        self._project_domain_name = input_data.get('OS_PROJECT_DOMAIN_NAME')
        self._certificate_path = input_data.get('OS_CA_PATH')

    @staticmethod
    def create(data):
        return Config(data)

    def to_credentials(self):
        return OpenStackCredentials(self.username,
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

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return 'OpenStack'

    @property
    def seed_file(self):
        return self._seed_file

    @property
    def logging_level(self):
        return self._log_level

    @property
    def auth_url(self):
        return self._auth_url

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def project(self):
        return self._project

    @property
    def region_name(self):
        return self._region_name

    @property
    def user_domain_name(self):
        return self._user_domain_name

    @property
    def project_domain_name(self):
        return self._project_domain_name

    @property
    def certificate_path(self):
        return self._certificate_path
