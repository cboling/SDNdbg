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

import paramiko


class Client(object):
    """
    Simple SSH Client to execute 'ovs-vsctl' commands since we cannot rely upon
    OVSDB running on remote machines to query.
    """
    _available_tables = ['Open_vSwitch', 'Bridge', 'Port', 'Interface',
                         'Flow_Table', 'QoS', 'Queue', 'Mirror', 'Controller',
                         'Manager', 'Netflow', 'SSL', 'sFlow', 'IPFIX',
                         'Flow_Sample_Collector_Set']

    def __init__(self, address, username, password):
        self._address = address
        self._username = username
        self._password = password
        self._client = None

    def connect(self):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            logging.info("Attempting ssh connection: {}@{}, password: '{}'".format(self._username,
                                                                                   self._address,
                                                                                   self._password))
            ssh_client.connect(address=self._address, username=self._username, password=self._password)
            return ssh_client

        except paramiko.BadAuthenticationType as e:
            logging.warning('OpenStack.linux_bridges: SSH Bad Authentication Exception: {}@{}: {}'.
                            format(self._username, self._address, e.message))
        return ssh_client


        # " --timeout=secs --format=json"

        # Port Commands
        # These  commands  examine and manipulate Open vSwitch ports.  These com‐
        # mands treat a bonded port as a single entity.
        #
        # list-ports bridge
        # Lists all of the ports within bridge on standard output, one per
        # line.  The local port bridge is not included in the list.
        #
        #
        # Interface Commands
        # These  commands  examine  the  interfaces  attached  to an Open vSwitch
        # bridge.  These commands treat a bonded port as a collection of  two  or
        # more interfaces, rather than as a single port.
        #
        # list-ifaces bridge
        # Lists  all  of  the interfaces within bridge on standard output,
        # one per line.  The local port bridge  is  not  included  in  the
        # list.
        #
        #
        # OpenFlow Controller Connectivity
        # ovs-vswitchd can perform all configured bridging and switching locally,
        # or  it can be configured to communicate with one or more external Open‐
        # Flow controllers.  The switch is typically configured to connect  to  a
        # primary  controller  that  takes  charge  of the bridge's flow table to
        # implement a network policy.  In addition, the switch can be  configured
        # to listen to connections from service controllers.  Service controllers
        # are typically used for occasional support and  maintenance,  e.g.  with
        # ovs-ofctl.
        #
        # get-controller bridge
        # Prints the configured controller target.
        #
        #
        #
        # Manager Connectivity
        # These  commands  manipulate   the   manager_options   column   in   the
        # Open_vSwitch  table  and rows in the Managers table.  When ovsdb-server
        # is configured to use the manager_options column for  OVSDB  connections
        #     (as described in INSTALL.Linux and in the startup scripts provided with
        # Open vSwitch), this allows the administrator to use ovs-vsctl  to  con‐
        # figure database connections.
        #
        # get-manager
        # Prints the configured manager(s).
        #
        #
        #
        # Database Commands
        #     These commands query and modify the contents of ovsdb tables.  They are
        #     a slight abstraction of the ovsdb interface and as such they operate at
        #     a lower level than other ovs-vsctl commands.
        #
        # Identifying Tables, Records, and Columns
        #
        #     Each of these commands has a table parameter to identify a table within
        #     the  database.   Many of them also take a record parameter that identi‐
        #     fies a particular record within a table.  The record parameter  may  be
        #     the  UUID  for a record, and many tables offer additional ways to iden‐
        #     tify records.  Some commands also take column parameters that  identify
        #     a particular field within the records in a table.
        #
        #     The following tables are currently defined:
        #
        #     Open_vSwitch
        #         Global  configuration  for an ovs-vswitchd.  This table contains
        #         exactly one record, identified by specifying  .  as  the  record
        #         name.
        #
        #     Bridge Configuration  for a bridge within an Open vSwitch.  Records may
        #         be identified by bridge name.
        #
        #     Port   A bridge port.  Records may be identified by port name.
        #
        #     Interface
        #         A network device attached to a port.  Records may be  identified
        #         by name.
        #
        #     Flow_Table
        #         Configuration for a particular OpenFlow flow table.  Records may
        #         be identified by name.
        #
        #     QoS    Quality-of-service configuration for a  Port.   Records  may  be
        #         identified by port name.
        #
        #     Queue  Configuration for one queue within a QoS configuration.  Records
        #         may only be identified by UUID.
        #
        #     Mirror A port mirroring configuration attached to  a  bridge.   Records
        #         may be identified by mirror name.
        #
        #     Controller
        #         Configuration for an OpenFlow controller.  A controller attached
        #         to a particular bridge may be identified by the bridge's name.
        #
        #     Manager
        #         Configuration for an OVSDB connection.  Records may  be  identi‐
        #         fied by target (e.g. tcp:1.2.3.4).
        #
        #     NetFlow
        #         A  NetFlow  configuration  attached to a bridge.  Records may be
        #         identified by bridge name.
        #
        #     SSL    The global  SSL  configuration  for  ovs-vswitchd.   The  record
        #         attached to the Open_vSwitch table may be identified by specify‐
        #         ing . as the record name.
        #
        #     sFlow  An sFlow exporter configuration attached to a  bridge.   Records
        #         may be identified by bridge name.
        #
        #     IPFIX  An  IPFIX  exporter configuration attached to a bridge.  Records
        #         may be identified by bridge name.
        #
        #     Flow_Sample_Collector_Set
        #         An IPFIX exporter configuration attached to a  bridge  for  sam‐
        #         pling packets on a per-flow basis using OpenFlow sample actions.
        #
        #     AutoAttach
        #         Configuration for Auto Attach within a bridge.
