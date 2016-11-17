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


class Node(ModelBase):
    """
    The Node class models a node in the network graph.

    The node may be a physical interface, computer, bridge, port, ...
    """
    # Each variable below represents a database field in this model
    name = StrippedCharField(max_length=2552, default='',
                             help_text='Human readable name for the node')
    description = StrippedCharField(max_length=1024, blank=True, null=True)

    class Meta:
        app_label = "collector"
        db_table = "collector_node"

    def __str__(self):
        return self.name

