#!/usr/bin/env python
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

import argparse
import logging
import os
import sys
import time

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

    fileHandler = RotatingFileHandler("{0}/{1}.log".format(log_path, app_name), maxBytes=1048576, backupCount=10)
    fileHandler.setFormatter(logging.Formatter(FORMAT))
    logging.getLogger().addHandler(fileHandler)


def shutdown(wait_delay):
    """
    Halt any running threads
    """
    from core.sync import SyncThread

    logging.info('Signaling Shutdown')
    SyncThread.stop_all_threads(wait_delay)


def main():
    # Parse input

    parser = argparse.ArgumentParser(description=app_name)

    parser.add_argument('--config', '-c', action='store', default=None,
                        help='Configuration file to use (use environment variables otherwise)')

    parser.add_argument('--output', '-o', action='store', default=None,
                        help='Output file for JSON dump, default is stdout')

    args = parser.parse_args()

    #############################################################################################
    # Create out configuration based on either a CONFIG file (YAML) or environment variables

    config = Config(config_file=args.config)

    # TODO: Support debug level setting in 'config' file.

    logging.info('Collecting SDN/NFV Elements')

    # Create our Site wrapper objects
    # TODO: Support multiple sites.  Allow global seed file and per-site seed files
    # TODO: Need an outermost NODE to hold the sites. It should be each Site's parent

    sites = []

    try:
        for site_config in config.sites:
            from core.sync import SyncThread

            new_site = Site(parent=None, **site_config.__dict__)
            sites.append(new_site)

            # Start a thread up to discover the site contents

            new_site.sync_thread = SyncThread(new_site)
            new_site.sync_thread.start(signal_notify=True)

        # TODO Pause to allow all information to be gathered

        print('Currently entering forever-loop until we get all this working')
        while True:
            time.sleep(3)

        # TODO Dump information out

        if args.output is not None:
            sys.stdout = open(args.output, 'w')

            # json_data = site_elements.to_json
            # print json_data

    except KeyboardInterrupt:
        logging.info('^C from keyboard captured, shutting down gracefully')
        shutdown(5.0)

    except Exception as e:
        logging.exception('Unhandled Exception Encountered')
        shutdown(0.0)
        raise e

    finally:
        shutdown(10.0)

if __name__ == "__main__":
    main()
