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

import collections
import os.path

import novaclient.client as nova_client
from keystoneauth1 import session
from keystoneauth1.identity import v2, v3
from keystoneclient.v2_0 import client as keystone_client_v2
from keystoneclient.v3 import client as keystone_client_v3

from core.credentials import Credentials as CoreCredentials


class Credentials(CoreCredentials):
    """
    OpenStack Credentials Class

    Provides some simple wrappers around all the various OpenStack Identity and Client APIs
    """
    _supported_keystone_versions = ['v2.0', 'v3']

    def __init__(self,
                 username,
                 password,
                 auth_url,
                 project_name,
                 user_domain_name=None,
                 project_domain_name=None,
                 ca_path=None):
        CoreCredentials.__init__(self, collections.OrderedDict({username: password}))

        self.auth_url = auth_url
        self.project_name = project_name
        self.user_domain_name = user_domain_name
        self.project_domain_name = project_domain_name
        self.ca_path = ca_path

        # Decode the version

        self.version = None

        for version in self._supported_keystone_versions:
            if auth_url[-len(version):].lower() == version:
                self.version = version
                break

        if self.version is None:
            raise ValueError('{}: Unknown or unsupported Keystone version'.
                             format(auth_url))
        # Is SSL being used
        self.is_ssl = auth_url[:5].lower() == 'https'

        if self.is_ssl:
            if self.ca_path is None:
                raise ValueError('A path to a certificates file is required if SSL is in use')
            elif not os.path.exists(self.ca_path):
                raise IOError("Certificate file '{}' does not exist".format(self.ca_path))

    def _v2_credentials(self):
        return {
            'username': self.username,
            'password': self.password,
            'auth_url': self.auth_url,
            'tenant_name': self.project_name
        }

    def _v3_credentials(self):
        return {
            'username': self.username,
            'password': self.password,
            'auth_url': self.auth_url,
            'project_name': self.project_name,
            'user_domain_name': self.user_domain_name,
            'project_domain_name': self.project_domain_name
        }

    @property
    def type(self):
        return 'OpenStack'

    @property
    def credentials(self):
        """
        Return OpenStack openstack_credentials for use with keystone v2/v3 identity API

        :return: (dict) Credentials
        """
        credentials = {
            'v2.0': self._v2_credentials,
            'v3': self._v3_credentials
        }
        return credentials[self.version]()

    @property
    def authorization(self):
        """
        Return OpenStack keystone client authorization/identity
        """
        auth = {
            'v2.0': v2.Password,
            'v3': v3.Password
        }
        return auth[self.version](**self.credentials)

    @property
    def session(self):
        """
        Return a keystone session object for this set of openstack_credentials
        """
        return session.Session(auth=self.authorization, verify=self.ca_path) if self.is_ssl \
            else session.Session(auth=self.authorization)

    @property
    def keystone_client(self):
        """
        Return a keystone client for this set of openstack_credentials
        """
        client = {
            'v2.0': keystone_client_v2.Client,
            'v3': keystone_client_v3.Client
        }
        return client[self.version](session=self.session)

    @property
    def nova_client(self):
        """
        Return a nova client for this set of openstack_credentials
        """
        version = '2'
        return nova_client.Client(version, session=self.session)
