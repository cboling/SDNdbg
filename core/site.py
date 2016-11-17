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
from core.node import Node


class Site(Node):
    """
    An OpenStack 'Site' represents a collection of OpenStack controllers that share a
    common geo-location.
    """
    my_controllers = None

    def __init__(self, config):
        Node.__init__(self, '')

        self.site_name = 'Site: {}'.format(config.name)
        self.config = config

    @property
    def parent(self):
        """
        Parent objects
        :return: parent
        """
        return None

    @property
    def children(self):
        """
        Child objects.  For a site, this is a list of all VIM Controllers
        :return: (list) of children
        """
        return self.controllers

    @property
    def unique_id(self):
        """
        :return: (string) Globally Unique Name
        """
        return self.name

    @property
    def name(self):
        """
        :return: (string) Human readable name for node
        """
        return self.site_name

    @property
    def controllers(self):
        """
        This property provides all known controllers in the network.  Currently provided
        by the configuration file

        :return: (list) server objects
        """
        from openstack.controller import Controller

        if self.my_controllers is None:
            self.my_controllers = Controller.controllers(self, self.config)

        return self.my_controllers
