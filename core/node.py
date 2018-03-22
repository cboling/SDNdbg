"""
Copyright (c) 2015 - present.  Boling Consulting Solutions, BCSW.net

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

from base import Base


class Node(Base):
    """
    The base class for a top level object that represents a device, port, computer, vm, container, ...
    """

    def __init__(self, **kwargs):
        Base.__init__(self, **kwargs)

    @property
    def edges(self):
        """
        Edges
        :return: (list) edges
        """
        return []

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
