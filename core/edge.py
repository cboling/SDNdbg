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

from base import Base


class Edge(Base):
    """
    The base class for a top level object that represents a connection between two devices
    """

    def __init__(self, **kwargs):
        Base.__init__(self, **kwargs)

    def __eq__(self, other):
        if not isinstance(other, Edge):
            return False
        return self.id == other.id

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
    def to_json(self):
        """
        Output information to simple JSON format
        :return: (list) edge 'data' elements
        """
        return '{"edge":{"id": "%s","source": "%s","target": "%s"}}' % (self.unique_id,
                                                                        self.source,
                                                                        self.target)
