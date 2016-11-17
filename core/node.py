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


class Node:
    """
    The base class for a top level object that represents a device, port, computer, vm, container, ...
    """
    json = ''

    def __init__(self, json_data):
        self.json = json_data

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        return self.unique_id == other.unique_id

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
        Child objects
        :return: (list) of children
        """
        return []

    @property
    def edges(self):
        """
        Edges
        :return: (list) edges
        """
        return []

    @property
    def unique_id(self):
        """
        :return: (string) Globally Unique Name
        """
        raise NotImplementedError("Required 'unique_id' property not implemented")

    @property
    def name(self):
        """
        :return: (string) Human readable name for node
        """
        raise NotImplementedError("Required 'name' property not implemented")

    @property
    def to_json(self):
        """
        Output information to simple JSON format
        :return: (list) node 'data' elements
        """
        result = '{ "node" :{ "id": "%s"' % self.unique_id

        if self.parent is not None:
            result += ', "parent": "%s"' % self.parent.unique_id

        result += '} }'

        return result
