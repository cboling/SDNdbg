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

from credentials import Credentials
from node import Node


class Controller(Node):
    """
    Base class for an NFV/VIM or SDN Contoller
    """
    def __init__(self, **kwargs):
        logging.info('core.Controller.__init__: {}'.format(pprint.PrettyPrinter().pformat(kwargs)))

        Node.__init__(self, **kwargs)

        # Save off site SSH credentials.  Should be useful for most all controller types
        # TODO: Do we want to support per-VIM/SDN sets of credentials?
        # TODO: How about global SSH user/passwords to try as well?

        self.ssh_credentials = None
        config = kwargs.get('config')
        while config is not None:
            if config.type.lower() == 'site':
                self.ssh_credentials = Credentials(config.ssh_username_and_passwords)
                break
            config = config.config_parent

    @staticmethod
    def create(parent, **kwargs):
        from openstack.controller import Controller as OpenStackController
        from onos.controller import Controller as ONOSController

        _supported_vims = {
            'openstack': OpenStackController.create,
            'onos': ONOSController.create
        }
        logging.info('core.Controller.create: {}'.format(pprint.PrettyPrinter().pformat(kwargs)))

        config = kwargs.get('config')
        create_method = _supported_vims.get(config.type.lower())

        if create_method is None:
            raise NotImplemented("Controller type '{}' is not supported".format(config.type))

        kwargs['parent'] = parent

        return create_method(**kwargs)
