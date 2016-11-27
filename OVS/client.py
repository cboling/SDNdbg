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
import time
import uuid

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
                            'Flow_Sample_Collector_Set']
        need_sudo = False

        try:
            connection = self.connect(self.address, self.username, self.password)
            command = 'ovs-vsctl --format=json --timeout=20 list'

            all_tables_start_time = time.clock()
            delta_times = {}

            for table in available_tables:
                delta_start = time.clock()

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
                    need_sudo = (error is None or 'permission denied' not in error.lower()) and len(output) > 0

                logging.debug('Table: {}, STDOUT: {}'.format(table, pprint.PrettyPrinter(indent=2).pformat(output)))
                logging.debug('Table: {}, STDERR: {}'.format(table, pprint.PrettyPrinter(indent=2).pformat(error)))

                delta_times[table.lower()] = time.clock() - delta_start

                try:
                    self.table_info[table.lower()] = self._table_json_to_dict(json.loads(output))

                    logging.debug('Table: {}, output: {}'.format(table, pprint.PrettyPrinter(indent=2).
                                                                 pformat(self.table_info[table.lower()])))
                except ValueError as e:
                    logging.exception('Value error converting OVS table {}'.format(table))

        except Exception as e:
            logging.exception('Client.get_tables')

        all_tables_delta_time = time.clock() - all_tables_start_time
        logging.info('OVS Table parsing took {} seconds.  Individual table delta times follow:\n{}'.
                     format(all_tables_delta_time, pprint.PrettyPrinter(indent=2).pformat(delta_times)))

        logging.info('output: {}'.format(pprint.PrettyPrinter(indent=2).pformat(self.table_info)))

    def _table_json_to_dict(self, json_data):
        # Get as tuples

        list_of_tuples = [zip(json_data['headings'], dataset) for dataset in json_data['data']]

        def to_self(val):
            return val

        def to_dict(val):
            """
            Convert to a dictionary.  The input 'val' is a list that contains zero or more
            lists composed of two values. T
            """
            result = {}
            for item in val:
                assert (len(item) == 2)
                assert (not isinstance(item[1], list))
                k = item[0]
                val_type = item[1][0] if isinstance(item[1], list) else 'literal'
                v = item[1][1] if isinstance(item[1], list) else item[1]
                result[k] = convert_it(val_type, v)

            return result

        def to_set(val):
            result = set()
            for item in val:
                val_type = val[0][0] if isinstance(val[0], list) else 'literal'
                v = val[0][1] if isinstance(val[0], list) else item
                result.add(convert_it(val_type, v))

            return result

        def to_uuid(val):
            return uuid.UUID(val)

        def convert_it(val_type, val):
            convert_method = {
                'literal': to_self,
                'map'    : to_dict,
                'set'    : to_set,
                'uuid'   : to_uuid
            }
            return convert_method.get(val_type, to_self)(val)

        # Now convert to list of dicts with conversions as needed

        info = []
        for tbl in list_of_tuples:
            data = {}
            for tpl in tbl:
                key = tpl[0]
                value_type = tpl[1][0].lower() if isinstance(tpl[1], list) else 'literal'
                value = tpl[1][1] if isinstance(tpl[1], list) else tpl[1]
                data[key] = convert_it(value_type, value)

            info.append(data)
        return info
