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
# Some various utilities

import logging
import netifaces as ni
import socket
import uuid

import libvirt

_log_levels = {
    'DEBUG'   : logging.DEBUG,
    'INFO'    : logging.INFO,
    'WARNING' : logging.WARNING,
    'WARN'    : logging.WARN,
    'ERROR'   : logging.ERROR,
    'CRITICAL': logging.CRITICAL
}


def get_uuid():
    """
    Simplified program to return UUID (format=1) but with node hard-coded to improve response
    and decrease file descriptors that may be left open

    :return: (UUID) New UUID
    """
    return uuid.uuid1(node=0xb8ca3ab44c0c)


def levelname_to_level(name):
    """
    Convert logging level string to logging level

    :param name: (string) Level to convert

    :return: Logging level
    """
    level = _log_levels.get(name.upper(), None)
    if level is None:
        raise ValueError("Invalid logging level '{}'".format(name))
    return level


def is_same_host(address_1, address_2):
    resolved_address_1 = socket.gethostbyname(address_1)
    resolved_address_2 = socket.gethostbyname(address_2)

    if resolved_address_1 is None or resolved_address_2 is None:
        return False

    return resolved_address_1 == resolved_address_2


def is_localhost(address):
    """
    Determine if an address is the address of a local interface.  Currently only
    IPv4 is supported

    :param address: IP address or hostname

    :return: (boolean) True if this is a local address
    """
    resolved_address = socket.gethostbyname(address)

    if resolved_address is None:
        return False

    if resolved_address == '127.0.0.1':
        return True

    interfaces = ni.interfaces()

    if interfaces is None:
        return False

    for interface in interfaces:
        ip_entries = ni.ifaddresses(interface).get(2, None)
        if ip_entries is not None:
            for ip_entry in ip_entries:
                if ip_entry is not None and 'addr' in ip_entry and ip_entry['addr'] == resolved_address:
                    return True

    return False


def libvirt_connection(username, password, address):
    """
    Open a read-only libVirt connection to the provided address.   Depending on how libVirt is
    configured in /etc/libvirt/libvirtd.conf, some connection methods may not be allowed. This will
    determine what types of connections may be supported.

    The format of the URIs differ depending if the address is local or remote, local URIs
    have the following format:

        driver:///system
        driver:///session
        driver+unix:///system
        driver+unix:///session

        where 'driver' may be one of the following:

            qemu    For managing qemu and KVM guests
            xen     For managing old-style (Xen 3.1 and older) Xen guests
            xenapi  For managing new-style Xen guests
            uml     For managing UML guests
            lxc     For managing Linux Containers
            vbox    For managing VirtualBox guests
            openvz  For managing OpenVZ containers
            esx     For managing VMware ESX guests
            one     For managing OpenNebula guests
            phyp    For managing Power Hypervisor guests

        Local URIs typically require the 'unix_sock_group', often 'libvird' and that the caller
        be a member of that group (see /etc/group and use 'usermod -aG <group> <user>' as needed)

    Remote URIs have the following format:
        driver[+transport]://[username@][hostname][:port]/[path][?extraparameters]

        where 'driver' is the same as above and transport is The name of one of the data
        transports. Possible values include tls, tcp, unix, ssh and ext. If omitted, it
        will default to tls if a hostname is provided, or unix if no hostname is provided.

        For transports, the following flags need to be set in /etc/libvirt/libvirtd.conf:

            tcp -> listen_tcp = 1
                   may want to set 'auth_tcp' to 'sasl' so TCP traffic is not in clear text

            tls -> listen_tls = 1

    :param username: username
    :param password: password
    :param address: IP address or hostname
    :return: libvirt connection object or None on failure
    """
    if address is None or is_localhost(address):
        uris = [
            'qemu:///system',  # UNIX localhost
        ]
    else:
        uris = [
            'qemu+ssh//{}@{}/system'.format(username, address),  # SSH connection
            'qemu+ssh//{}@{}/system'.format(username, address),  # TCP connection
            'qemu+tls//{}@{}/system'.format(username, address),  # TLS with certificate verification
            'qemu+tls//{}@{}/system?no_verify=1'.format(username, address),  # TLS without certificate verification
            'qemu+tcp//{}@{}/system'.format(username, address),  # TCP Connection
        ]

    for target in uris:
        logging.info('libvirt_connection: target: {}'.format(target))

        def request_cred(credentials, _user_data):
            # TODO: Have only tested username/password.  What about Certificates?
            for credential in credentials:
                if credential[0] == libvirt.VIR_CRED_AUTHNAME:
                    credential[4] = username
                elif credential[0] == libvirt.VIR_CRED_PASSPHRASE:
                    credential[4] = password
            return 0

        auth = [[libvirt.VIR_CRED_AUTHNAME, libvirt.VIR_CRED_PASSPHRASE], request_cred, None]

        try:
            connection = libvirt.openAuth(target, auth, flags=libvirt.VIR_CONNECT_RO)
            # connection = libvirt.openReadOnly(target)
            if connection is not None:
                return connection

        except libvirt.libvirtError as e:
            # logging.warning('LibvirtError: {}: {}'.format(target, e.message))
            pass

    return None
