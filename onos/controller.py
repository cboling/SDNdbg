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

from core.node import Node


class Controller(Node):
    """
    ONOS Controller Model

    A unique controller.  Multiple controllers in a culster will have the same cluster ID

    Fields / Attributes:
    uniqueId = (char):   A unique character string to identify the item.  This field is
                         combined with parent information to provide a unique path from the
                         highest level object to this item.  For the field itself, it
                         should be as short enough for display purposes but unique enough
                         not to clash with other items.  For instance, a GUID/UUID is always
                         unique.  A name like eth0 is not, so it may need to be prepended prepended
                         with it's parent unique ID. For instance, instead of 'eth0' you may want
                         to use <system-name>/eth0  or <system-name>/<bridge-name>/eth0.

    TODO: How do we set a 'cluster' id.
    TODO: Need a 'cluster master' boolean field
    TODO: Where & how to best store login credentials
    """

    def __init__(self, **kwargs):
        logging.info('onos.Controller.__init__: entry:\n{}'.format(pprint.PrettyPrinter().pformat(kwargs)))
        Node.__init__(self, **kwargs)

    @staticmethod
    def create(**kwargs):
        logging.info('onos.Controller.Create: entry:\n{}'.format(pprint.PrettyPrinter().pformat(kwargs)))
        return Controller(**kwargs)

    def connect(self):
        """
        Create credentials for accessing and ONOS Controller

        :return: (
        """
        return "TODO: Not yet implemented"

    def perform_sync(self):
        """
        A controller is made up of one or more machines running services that we care about.  There are
        a large number of OpenStack services, but we currently only care about a few.

        :return: True if synchronization was successful, False otherwise
        """
        if self.client is None:
            return False

        return True  # TODO: Not yet implemented

        # ipAddress = models.GenericIPAddressField()
        # tcpPort = models.IntegerField()  # TODO Place bounds 0-65535 possible?
        #
        # # TODO: Username/password is cluster-wide
        # # TODO: Each node in a cluster has a unique NodeId
        # username = models.CharField(max_length=100)
        # password = models.CharField(max_length=50)  # TODO Remember to use forms.PasswordInput() in the forms.py
        #
        # ACTIVE = 'A'  # Signifies that the instance is active and operating normally
        # INACTIVE = 'I'  # Signifies that the instance is inactive, which means either down or up, but not operational
        #
        # SUPPORTED_STATUS_IN_CLUSTER = (
        #     (ACTIVE, 'Active'),
        #     (INACTIVE, 'Inactive'),
        # )
        # __valid_controller_status = (ACTIVE, INACTIVE)
        #
        # status_in_cluster = models.CharField(max_length=2, choices=SUPPORTED_STATUS_IN_CLUSTER, default=ACTIVE)
        #
        # class Meta:
        #     app_label = 'onos'
        #     db_table = 'onos_controller'
        #
        # @classmethod
        # def create(cls, name, address, port, username, password, status=ACTIVE, parent=None):
        #     """
        #     TODO:    Fill this out...
        #     :param name:
        #     :param address:
        #     :param port:
        #     :param username:
        #     :param password:
        #     :param status:
        #     :param parent:
        #     :return:
        #     """
        #     logger.debug('Controller.create(%s, %s, %d, %s, %s, %s)' % (name, address, port, username,
        #                                                                 password, str(status)))
        #     return cls(name=name, address=address, port=port, username=username, password=password,
        #                status_in_cluster=status, parent=parent)
        #
        # def __str__(self):
        #     return 'ONOS Controller: %s (%s)' % (self.name, self.address)
        #
        # def is_cluster_status_valid(self):
        #     """ Is this a valid state for a controller to be in
        #     :return: (bool) True if valid, False otherwise.
        #     """
        #     return self.status_in_cluster in self.__valid_controller_status
