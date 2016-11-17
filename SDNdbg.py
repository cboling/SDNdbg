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
# !/usr/bin/env python
import argparse
import logging
import os
import sys

from core.config import Config
from core.site import Site

app_name = 'SDNdbg'
FORMAT = '%(asctime)-15s %(levelname)s:{app}:%(message)s'.format(app=app_name)
logging.basicConfig(level=logging.INFO, format=FORMAT)

home_directory = os.environ.get('HOME', '/tmp')
log_directory = os.environ.get('LOG_DIR', '{home}/logs'.format(home=home_directory))
log_path = "{log_dir}/{app}".format(log_dir=log_directory, app=app_name)


def make_sure_path_exists(path):
    import errno
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            return False
    return True


if make_sure_path_exists(log_path):
    from logging.handlers import RotatingFileHandler

    fileHandler = RotatingFileHandler("{0}/{1}.log".format(log_path, app_name), maxBytes=1048576, backupCount=5)
    fileHandler.setFormatter(logging.Formatter(FORMAT))
    logging.getLogger().addHandler(fileHandler)


def main():
    # Parse input

    parser = argparse.ArgumentParser(description=app_name)

    parser.add_argument('--config', '-c', action='store', default=None,
                        help='Configuration file to use (use environment variables otherwise)')

    args = parser.parse_args()

    #############################################################################################
    # Create out configuration based on either a CONFIG file (YAML) or environment variables

    config = Config(config_file=args.config)

    # TODO: Support debug level setting in 'config' file.

    logging.info('Collecting SDN/NFV Elements')

    # Load up the site (could be multiple controllers...)
    site_elements = Site(config)

    # TODO: Set up a state machine for the 'nodes' and 'edges' and transition with states such as
    #
    #  Initial, discovery, refreshing, synchronized, deleting, deleted, ...
    #
    ########################################################################
    # TODO: Move the SDN controllers into the Site (core) class

    # TODO: Support more than one SDN Controller
    # onos_elements = Controller(config.sdn_controllers[0])

    #######################################################################

    if args.output is not None:
        sys.stdout = open(args.output, 'w')

    json_data = site_elements.to_json

    print json_data


if __name__ == "__main__":
    main()
