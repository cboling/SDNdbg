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
import collections
import logging
import paramiko
import subprocess

_cached_creds = {}


class Credentials:
    """
    This is just a simple class to represent login credentials
    """

    def __init__(self, ssh_names):
        """
        Store basic (username/password) credentials

        :param ssh_names: (OrderedDict) Ordered dictionary of user (key) password (value) pairs
        """
        if not isinstance(ssh_names, collections.OrderedDict):
            raise ValueError('Core credentials input should be an OrderedDictionary. Received: {}',
                             type(ssh_names))

        self._names = collections.OrderedDict() if ssh_names is None else ssh_names

    @property
    def username(self):
        # Return the first entry and the first part of the pair
        return self._names.items()[0][0]

    @property
    def password(self):
        return self._names.items()[0][1]

    def get_ssh_credentials(self, url=None):
        """
        Get the set of SSH credentials, optionally optimized based on previously saved values for a given URl

        :param url: (string) URL to use in looking into cached credentials for a previously saved match that was
                             successful in a previous attempt
        :return: (dict/OrderedDict) Username(key) password(value) pairs to try
        """
        creds = _cached_creds.get(url, self._names) if url is not None else self._names
        return creds if creds is not None else {self.username: self.password}

    def save_ssh_creds(self, url, username, password):
        creds = collections.OrderedDict()
        creds[username] = password
        creds.update(self._names)
        _cached_creds[url] = creds

    def ssh_subprocess(self, address, command):
        """
        Execute the given command on the remote host, trying all possible username/passwords until success

        :param address: (string) address to open connect to
        :param command: (string) command

        :return: Result or None or error
        """
        items = self.get_ssh_credentials(address)

        for username, password in items.iteritems():
            host = "{}@{}".format(username, address)
            try:
                p = subprocess.Popen(["ssh", "%s" % host, command],
                                     shell=False,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
                result = p.stdout.readlines()

                if result is not None:
                    self.save_ssh_creds(address, username, password)
                    return result

            except Exception as e:
                logging.info("ssh_subprocess[{}: command '{}' failed: {}".format(host, command, e.message))

        return None

    def ssh_client(self, address, function):
        """
        Get an SSH Client connection to the following URL

        :param address: (string) address to open connection to
        :param function: (function) function to call with client that performs the needed operations
        """
        items = self.get_ssh_credentials(address)

        for username, password in items.iteritems():

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            try:
                logging.info("Attempting ssh connection: {}@{}, password: '{}'".format(username, address, password))

                ssh.connect(address, username=username, password=password)
                function(ssh)
                break

            except paramiko.BadAuthenticationType as e:
                logging.warning('OpenStack.linux_bridges: SSH Bad Authentication Exception: {}@{}: {}'.
                                format(username, address, e.message))
