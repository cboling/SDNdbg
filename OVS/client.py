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

import json
import logging
import pprint

import paramiko

class Client(object):
    """
    Simple SSH Client to execute 'ovs-vsctl' commands since we cannot rely upon
    OVSDB running on remote machines to query.
    """
    def __init__(self, address, username, password):
        self._address = address
        self._username = username
        self._password = password
        self.raw_table_info = {}
        self.table_info = {}

    @property
    def address(self):
        return self._address

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    def connect(self, address, username, password):
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            logging.info("Attempting ssh connection: {}@{}, password: '{}'".format(self.username,
                                                                                   self.address,
                                                                                   self.password))
            ssh_client.connect(address, username=username, password=password)
            return ssh_client

        except paramiko.BadAuthenticationType as e:
            logging.warning('OpenStack.linux_bridges: SSH Bad Authentication Exception: {}@{}: {}'.
                            format(username, address, e.message))
        return ssh_client

    @staticmethod
    def get_topology(address, username, password):
        """
        Updates the entire topology of the OVS database on a node
        """
        client = Client(address, username, password)
        client.get_tables()

    def get_tables(self):
        available_tables = ['Open_vSwitch', 'Bridge', 'Port', 'Interface',
                            'Flow_Table', 'QoS', 'Queue', 'Mirror', 'Controller',
                            'Manager', 'Netflow', 'SSL', 'sFlow', 'IPFIX',
                            'Flow_Sample_Collector_Set', 'AutoAttach']
        need_sudo = False

        try:
            connection = self.connect(self.address, self.username, self.password)
            command = 'ovs-vsctl --format=json --timeout=20 list'

            for table in available_tables:
                ssh_stdin, ssh_stdout, ssh_stderr = connection.exec_command(str('{}{} {}'.
                                                                                format('sudo ' if need_sudo else '',
                                                                                       command, table)))
                error = ssh_stderr.read()
                output = ssh_stdout.read()

                if error is not None and 'Permission denied' in error:
                    # Try with sudo

                    ssh_stdin, ssh_stdout, ssh_stderr = connection.exec_command(str('sudo {} {}'.
                                                                                    format(command, table)))
                    error = ssh_stderr.read()
                    output = ssh_stdout.read()
                    need_sudo = (error is None or 'Permission denied' not in error) and len(output) > 0

                logging.debug('Table: {}, STDOUT: {}'.format(table, pprint.PrettyPrinter(indent=2).pformat(output)))
                logging.error('Table: {}, STDERR: {}'.format(table, pprint.PrettyPrinter(indent=2).pformat(error)))

                json_data = json.loads(output)

                self.table_info[table] = []
                for dataset in json_data['data']:
                    self.table_info[table].append(zip(json_data['headings'], dataset))

                logging.debug('Table: {}, output: {}'.format(table, pprint.PrettyPrinter(indent=2).
                                                             pformat(self.table_info[table])))

        except Exception as e:
            logging.exception('Client.get_tables')

        logging.info('Table: {}, output: {}'.format(table, pprint.PrettyPrinter(indent=2).
                                                    pformat(self.table_info)))

        pass
