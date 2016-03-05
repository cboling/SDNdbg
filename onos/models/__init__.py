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

DEFAULT_USERNAME = 'onos'  # Default ONOS username for REST GET operations
DEFAULT_PASSWORD = 'rocks'  # Default ONOS password for REST GET operations
DEFAULT_REST_PORT = 8181  # Default port for ONOS REST commands


def ulr_prefix(ip_address, port_number=DEFAULT_REST_PORT, version=1):
    """
    Create the base URL prefix for an ONOS REST interface
    :param ip_address:  IP Address or hostname for ONOS Controller
    :param port_number: Port number, default is 8181
    :param version:     API version number, default is 1

    :return: String to use as the initial portion of a REST API call to ONOS
    """
    return 'http://%s:%d/onos/v%d/' % (ip_address, port_number, version)
