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
from credentials import OnosCredentials


class Config(object):
    """
    Class used to wrap a set of openstack configuration information
    """

    def __init__(self, parent, input_data):
        self._parent = parent
        self._seed_file = input_data.get('seed-file', parent.seed_file)
        self._log_level = input_data.get('logging-level', parent.logging_level)

        self._name = input_data.get('name', 'ONOS')
        self._address = input_data.get('address')
        self._username = input_data.get('username', 'onos')
        self._password = input_data.get('password', 'rocks')
        self._port = input_data.get('port')

    @staticmethod
    def create(data):
        return Config(data)

    def to_credentials(self):
        return OnosCredentials(self.username,
                               self.password,
                               self.address,
                               self.port)

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return 'ONOS'

    @property
    def seed_file(self):
        return self._seed_file

    @property
    def logging_level(self):
        return self._log_level

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def address(self):
        return self._address

    @property
    def port(self):
        return self._port
