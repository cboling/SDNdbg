# Copyright (c) 2015 - present.  Boling Consulting Solutions, BCSW.net
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and

from __future__ import unicode_literals

import ast
import logging
import pprint

from .client import Client

DEFAULT_SYSFS_MOUNT_POINT = '/sys'
_sysfs_mount_point = DEFAULT_SYSFS_MOUNT_POINT


def set_sysfs_mount_point(point):
    # TODO: Support alternate mount points within config file
    _sysfs_mount_point = point


def get_sysfs_mount_point():
    return _sysfs_mount_point


def get_sys_class_net_interface_devices(connection, cmd_prefix=""):
    # Walk the /sys/class/net structure and create a dictionary with each device we care about
    return _get_device_list(connection, cmd_prefix)


def _get_device_list(connection, cmd_prefix=""):
    """
    Get a list of network devices from /sys/class/net

    :param connection: SSH client connection

    :return: (list of dict) List of device dictionaries based of /sys/class/net/<device> contents
    """
    ignore = ['lo', 'ovs-system']
    command = cmd_prefix + '/bin/ls ' + _sysfs_mount_point + '/class/net'

    devices = {}
    device_path = {}

    try:
        output, error = Client.exec_command(connection, command)

        for line in output.split(str('\n')):
            for dev in str.split(line):
                if dev not in ignore:
                    device_path[dev] = str('{}/class/net/{}'.format(_sysfs_mount_point, dev))

    except Exception as e:
        logging.exception('Client._get_sys_class_net_interface_devices')

    # Walk each device subdirectory a dictionary of information for the device

    for name, sys_path in device_path.items():
        if sys_path == str(_sysfs_mount_point + '/class/net/bonding_masters'):
            devices[name] = _get_bonding_master_detail(connection, sys_path, cmd_prefix)
        else:
            devices[name] = _get_device_detail(connection, sys_path, cmd_prefix)

        devices[name][str('name')] = name
        #
        # TODO: Add driver detail and peer information if we can !!!
        # TODO: Also dump to the screen some ethtool output to see what is usefull

        if sys_path != str(_sysfs_mount_point + '/class/net/bonding_masters'):
            devices[name]['driver'] = _driver_info(connection, name, cmd_prefix=cmd_prefix)
            if devices[name]['driver'].get('supports-statistics', False):
                stats = _driver_stats(connection, name, cmd_prefix=cmd_prefix)

                if 'statistics' in devices[name]:
                    devices[name]['statistics'].update(stats)
                else:
                    devices[name]['statistics'] = stats

    logging.debug('_get_device_list: output: {}'.format(pprint.PrettyPrinter(indent=2).pformat(devices)))

    return devices


def _get_bonding_master_detail(connection, sys_path, cmd_prefix=""):
    """
    The /sys/class/net/bonding_masters (Sysfs) file contains information on
    :param connection:
    :param sys_path:
    :param cmd_prefix:
    :return:
    """
    command = cmd_prefix + 'cat {}'.format(sys_path)
    master = {}

    try:
        # do ->  cat /sys/class/net/bonding_masters
        #         bond0 fabric
        output, error = Client.exec_command(connection, command)

        for master_line in output.split(str('\n')):
            for bonding_device in master_line.split():
                master[bonding_device] = {}

                # Pull configuration from /proc/net/bonding/<bonding_device>

                # do ->  cat cat /proc/net/bonding/<device>
                #        Ethernet Channel Bonding Driver: v3.7.1 (April 27, 2011)
                #
                #        Bonding Mode: load balancing (round-robin)
                #        MII Status: down
                #        MII Polling Interval (ms): 0
                #        Up Delay (ms): 0
                #        Down Delay (ms): 0
                # or
                #       Ethernet Channel Bonding Driver: 2.6.1 (October 29, 2004)
                #       Bonding Mode: load balancing (round-robin)
                #       Currently Active Slave: eth0
                #       MII Status: up
                #       MII Polling Interval (ms): 1000
                #       Up Delay (ms): 0
                #       Down Delay (ms): 0
                #
                #       Slave Interface: eth1
                #       MII Status: up
                #       Link Failure Count: 1
                #
                #       Slave Interface: eth0
                #       MII Status: up
                #       Link Failure Count: 1
                #
                command = cmd_prefix + 'cat /proc/net/bonding/' + bonding_device

                output, error = Client.exec_command(connection, command)

                slave_name = None

                for device_line in output.split(str('\n')):
                    if len(device_line.strip()) == 0:
                        slave_name = None
                        continue

                    fields = device_line.split(':')

                    if len(fields) == 2:
                        if fields[0].strip().lower() == 'slave interface':
                            slave_name = fields[0].strip()
                            master[bonding_device][slave_name] = {}
                            master[bonding_device][slave_name][fields[0].strip()] = fields[1].strip()

                        elif slave_name is not None:
                            master[bonding_device][slave_name][fields[0].strip()] = fields[1].strip()
                        else:
                            master[bonding_device][fields[0].strip()] = fields[1].strip()

    except Exception as e:
        logging.exception('Client._get_bonding_master_detail')

    logging.debug('_get_bonding_master_detail: detail:\n{}'.format(pprint.PrettyPrinter(indent=2).pformat(master)))

    return master


def _get_device_detail(connection, sys_path, cmd_prefix=""):
    """
    Walk the /sys/class/net/<device> file structure and convert it into a usable dictionary.

    :param connection:
    :param sys_path:
    :param cmd_prefix:
    :return:
    """
    command = cmd_prefix + 'find {} -type f -print -exec cat {{}} \; -exec echo \;'.format(sys_path + '/')
    ignore_errors = ['invalid argument', 'operation not supported', 'permission denied']

    device = {}

    try:
        # do ->  find /sys/calls/net/<dev>/ -type f -print -exec cat {} \;   will output something like
        #
        #    ...
        #       /sys/class/net/qvo5faab8ab-96/queues/tx-0/byte_queue_limits/hold_time
        #       1000
        #       /sys/class/net/qvo5faab8ab-96/queues/tx-0/byte_queue_limits/inflight
        #       0
        #       /sys/class/net/qvo5faab8ab-96/tx_queue_len
        #       1000
        #       /sys/class/net/qvo5faab8ab-96/uevent
        #       INTERFACE=qvo5faab8ab-96
        #       IFINDEX=38
        #       /sys/class/net/qvo5faab8ab-96/statistics/rx_fifo_errors
        #       0
        #    ...
        output, error = Client.exec_command(connection, command, ignore_errors)
        item_name = None

        for line in output.split(str('\n')):
            # Is it a filename
            if len(line) == 0:
                continue  # Extra echo in command insures all 'cat' commands end with at least one \n

            elif line.startswith(sys_path):
                item_name = line[len(sys_path) + 1:]

            elif item_name is not None:
                # It is the contents of a file, add it as an item, watching to see if it is more than
                # just one line

                if item_name in device:
                    if not isinstance(device[item_name], list):
                        device[item_name] = [device[item_name]]
                    device[item_name].append(line)
                else:
                    device[item_name] = line

        def tryeval(val):
            # TODO: Add list recursion support
            try:
                val = ast.literal_eval(val)
            except (ValueError, SyntaxError):
                pass
            return val

        def build_nested_dict_helper(key, container, val):
            segments = key.split(str('/'))
            head = segments[0]
            tail = segments[1:]
            if not tail:
                container[head] = val
            else:
                if head not in container:
                    container[head] = {}
                build_nested_dict_helper(str('/').join(tail), container[head], val)

        def build_nested_dict(paths):
            container = {}
            for key, val in paths.items():
                build_nested_dict_helper(key, container, tryeval(val))
            return container

        device = build_nested_dict(device)

    except Exception as e:
        logging.exception('Client._get_device_detail')

    logging.debug('_get_device_detail: detail:\n{}'.format(pprint.PrettyPrinter(indent=2).pformat(device)))

    return device


def _driver_info(connection, device, cmd_prefix=""):  # TODO Deprecated
    driver_command = cmd_prefix + 'ethtool -i {}'.format(device)

    # Use ethtool t get more information on the interface
    # For each **dev** _device_ above, it will execute the following command to extract out
    # the driver involved:
    #
    # ```
    # driver=$(ethtool -i $dev | awk '/driver:/ {print $2}' 2> /dev/null)
    # ```
    # The output for a sample number of devices above (ignoring the __awk__ filter) are:
    #
    # ```
    # root@onos-sfc:/home/cboling/neutron-diag# ethtool -i br-ext
    # driver: openvswitch
    # version:
    # firmware-version:
    # bus-info:
    # supports-statistics: no
    # supports-test: no
    # supports-eeprom-access: no
    # supports-register-dump: no
    # supports-priv-flags: no
    #
    detail = {}

    try:
        output, error = Client.exec_command(connection, driver_command)
        logging.debug('Driver detail for {}: {}'.format(device, output))

        for line in output.split(str('\n')):
            # Is it a filename
            if len(line.strip()) == 0:
                continue

            fields = line.split(str(':'))

            if len(fields) == 2:
                if fields[1].strip().lower() == 'yes':
                    fields[1] = True
                elif fields[1].strip().lower() == 'no':
                    fields[1] = False
                else:
                    fields[1] = fields[1].strip()

            detail[fields[0].strip()] = fields[1]

    except Exception as e:
        logging.exception('Client._driver_info')

    logging.debug('_driver_info: output: {}'.format(pprint.PrettyPrinter(indent=2).pformat(detail)))

    return detail


def _driver_stats(connection, device, cmd_prefix=""):  # TODO Deprecated
    stats_command = cmd_prefix + 'ethtool -S {}'.format(device)

    # Use ethtool t get more information on the interface
    # For each **dev** _device_ above, it will execute the following command to extract out
    # the driver involved:
    #
    # ```
    # driver=$(ethtool -i $dev | awk '/driver:/ {print $2}' 2> /dev/null)
    # ```
    # The output for a sample number of devices above (ignoring the __awk__ filter) are:
    #
    # ```
    # root@onos-sfc:/home/cboling/neutron-diag# ethtool -i br-ext
    # driver: openvswitch
    # version:
    # firmware-version:
    # bus-info:
    # supports-statistics: no           if the -i output 'support-statistics' == yes
    # supports-test: no
    # supports-eeprom-access: no
    # supports-register-dump: no
    # supports-priv-flags: no
    #
    # ifIndex command just puts out one line with ifIndex
    #
    #  -S output for veth looks like
    #    NIC statistics:
    #        peer_ifindex: 33
    #
    # Sometimes for NICs, we might get:
    #    NIC statistics:
    #        rx_packets: 0
    #        tx_packets: 0
    #        rx_bytes: 0
    #        tx_bytes: 0
    #        rx_pkts_nic: 0
    stats = {}

    try:
        def tryeval(val):
            try:
                val = ast.literal_eval(val)
            except (ValueError, SyntaxError):
                pass
            return val

        output, error = Client.exec_command(connection, stats_command)
        logging.debug('Statistics detail for {}: {}'.format(device, output))

        for line in output.split(str('\n')):
            # Is it a filename
            if len(line.strip()) == 0:
                continue

            fields = line.split(str(':'))

            stats[fields[0].strip()] = tryeval(fields[1].strip())

    except Exception as e:
        logging.exception('Client._driver_stats')

    logging.debug('_driver_stats: output: {}'.format(pprint.PrettyPrinter(indent=2).pformat(stats)))

    return stats
