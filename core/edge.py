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


class Edge:
    """
    The base class for a top level object that represents a connection between two devices
    """
    json = ''

    def __init__(self, json_data):
        self.json = json_data

    def __eq__(self, other):
        if not isinstance(other, Edge):
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
    def unique_id(self):
        """
        :return: (string) Globally Unique Name
        """
        raise NotImplementedError("Required 'unique_id' property not implemented")

    @property
    def source(self):
        """
        :return: (string) Source Node ID
        """
        raise NotImplementedError("Required 'source' property not implemented")

    @property
    def target(self):
        """
        :return: (string) Target Node Id
        """
        raise NotImplementedError("Required 'target' property not implemented")

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
        :return: (list) edge 'data' elements
        """
        return '{"edge":{"id": "%s","source": "%s","target": "%s"}}' % (self.unique_id,
                                                                        self.source,
                                                                        self.target)
