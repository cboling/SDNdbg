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

from core.credentials import Credentials


class OnosCredentials(Credentials):
    """
    ONOS Controller Credentials Class

    Provides some simple wrappers around what is needed to access ONOS
    """

    def __init__(self, username, password, address, port):
        Credentials.__init__(self, collections.OrderedDict({username: password}))

        self.address = address
        self.port = port

    @property
    def type(self):
        return 'ONOS'

    @property
    def auth(self):
        """
        Return an auth tuple for the requests library

        :return: (tuple) Username/password
        """
        auth = (self.username, self.password)
        return auth
