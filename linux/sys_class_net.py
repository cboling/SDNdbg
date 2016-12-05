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

import ast
import logging
import pprint

from client import Client


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
    command = cmd_prefix + '/bin/ls /sys/class/net'

    devices = {}
    device_path = {}

    try:
        output, error = Client.exec_command(connection, command)

        for line in output.split(str('\n')):
            for dev in str.split(line):
                if dev not in ignore:
                    device_path[dev] = str('/sys/class/net/{}'.format(dev))

    except Exception as e:
        logging.exception('Client._get_sys_class_net_interface_devices')

    # Walk each device subdirectory a dictionary of information for the device

    for name, sys_path in device_path.items():
        devices[name] = _get_device_detail(connection, sys_path, cmd_prefix)
        devices[name][str('name')] = name
        #
        # TODO: Add driver detail and peer information if we can !!!

    logging.debug('_get_device_list: output: {}'.format(pprint.PrettyPrinter(indent=2).pformat(devices)))

    return devices


def _get_device_detail(connection, sys_path, cmd_prefix=""):
    """
    Walk the /sys/class/net/<device> file structure and convert it into a usable dictionary.

    :param connection:
    :param sys_path:
    :param cmd_prefix:
    :return:
    """
    command = cmd_prefix + 'find {} -type f -print -exec cat {{}} \; -exec echo \;'.format(sys_path + '/')
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
        output, error = Client.exec_command(connection, command)
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
        return device

    except Exception as e:
        logging.exception('Client._get_device_detail')

    logging.debug('_get_device_detail: detail:\n{}'.format(pprint.PrettyPrinter(indent=2).pformat(device)))


def _driver_info(connection, device):  # TODO Deprecated
    driver_info_command = 'ethtool -i {}'.format(device)
    ifIndex_command = 'cat /sys/class/net/{}/ifIndex'.format(device)
    stats_command = 'ethtool -S {}'.format(device)

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
    # ifIndex command just puts out one line with ifIndex
    #
    #  -S output for veth looks like
    #       NIC statistics:
    #           peer_ifindex: 33
    #
    #
    #   In the above output, there are zero or more lines output.  Can probably figure it out by
    #   lookiing for /sys/class/net/... to know if it is a filename or useful statistic
    detail = {}
    try:
        output, error = Client.exec_command(connection, driver_info_command)

        logging.info('detail: {}'.format(output))

        # The script then looks for, and processes only the _veth_, _openvswitch_, and _bridge_
        # driver types.  Each driver type device is saved off as in the **node** file.
        # TODO: look into driver type 'bonding' to see how we may want to represent this

    except Exception as e:
        logging.exception('Client._get_sys_class_net_interface_devices')

    logging.info('_get_device_detail: output: {}'.format(pprint.PrettyPrinter(indent=2).pformat(detail)))

    return detail
