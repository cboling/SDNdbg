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

import paramiko


class Client(object):
    """
    Simple SSH Client to execute 'brctl show' commands since a remotely accessible API is not available
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
            ssh_client = None

        return ssh_client

    @staticmethod
    def get_topology(address, username, password):
        """
        Updates the entire topology of the OVS database on a node
        """
        client = Client(address, username, password)
        return client._get_tables() if client is not None else None

    def _get_tables(self):
        available_tables = ['bridge', 'interface', 'namespace']

        get_funcs = {
            'bridge': Client._get_bridge_table,
            'interface': Client._get_interface_table,
            'namespace': Client._get_namespace_table
        }
        connection = None
        try:
            connection = self.connect(self.address, self.username, self.password)

            if connection is not None:
                for table in available_tables:
                    self.table_info[table] = get_funcs.get(table)(connection)
            else:
                logging.error('Linux.client: Could not open a connection to {}'.format(self.address))

        finally:
            if connection is not None:
                connection.close()

        logging.info('_get_tables: Contents follow:\n{}'.
                     format(pprint.PrettyPrinter(indent=2).pformat(self.table_info)))

        return self.table_info

    @staticmethod
    def exec_command(connection, command, ignore_errors=None):

        command = str('sudo {}'.format(command))

        ssh_stdin, ssh_stdout, ssh_stderr = connection.exec_command(command)
        error = str(ssh_stderr.read())
        output = str(ssh_stdout.read())

        logging.debug("Command: '{}', STDOUT: {}".format(command, output))

        if len(error) > 0 and (ignore_errors is None or
                                   not any(ignore in error.lower() for ignore in ignore_errors)):
            logging.warning("Command: '{}', STDERR: {}".format(command, error))

        return output, error

    @staticmethod
    def _get_bridge_table(connection):
        # TODO Move to separate file
        command = str('brctl show')
        bridge_info = []
        try:
            output, error = Client.exec_command(connection, command)
            whitespace = str(' \t\n\r')
            line_input = None

            for line in output.split(str('\n')):

                # Output could contain any of the following
                #      7 fields for header (don't care)
                # 3 or 4 fields for new bridge line
                #      1 fields for bridge line continuation
                #      (all others we do not care about)

                fields = str.split(line)

                if len(fields) == 4 or len(fields) == 3:
                    # Save completed partial from before
                    if line_input is not None:
                        bridge_info.append(line_input)

                    line_input = {
                        'name'       : fields[0].strip(whitespace),
                        'id'         : fields[1].strip(whitespace),
                        'stp-enabled': False if fields[2].strip(whitespace).lower() == 'no' else True,
                        'interfaces' : [fields[3].strip(whitespace)] if len(fields) > 3 else []
                    }
                elif len(fields) == 1:
                    # Continuation line for interfaces
                    line_input['interfaces'].append(fields[0].strip(whitespace))

                else:
                    if line_input is not None:
                        bridge_info.append(line_input)
                        line_input = None

        except Exception as e:
            logging.exception('Client.get_bridge_table')

        logging.info('output: {}'.format(pprint.PrettyPrinter(indent=2).pformat(bridge_info)))

        return bridge_info

    @staticmethod
    def _get_interface_table(connection):
        from sys_class_net import get_sys_class_net_interface_devices

        # First get a list of all network devices we care about, first the global network namespace

        devices = get_sys_class_net_interface_devices(connection)

        return devices

    @staticmethod
    def _get_namespace_table(connection):
        """
        Get a list of network namespaces and their contents

        TODO: Move to separate file
        """
        from sys_class_net import get_sys_class_net_interface_devices

        namespaces = {}

        try:
            # First a list of namespaces

            command = 'ip netns list'
            output, error = Client.exec_command(connection, command)

            for line in output.split(str('\n')):
                for ns in str.split(line):
                    prefix = 'ip netns exec {} '.format(ns)
                    namespaces[ns] = get_sys_class_net_interface_devices(connection, cmd_prefix=prefix)

        except Exception as e:
            logging.exception('Client._get_namespace_table')

        logging.debug('_get_namespace_table: output: {}'.format(pprint.PrettyPrinter(indent=2).pformat(namespaces)))

        return namespaces
