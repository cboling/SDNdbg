"""
Copyright (c) 2015 - present.  Boling Consulting Solutions, BCSW.net

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
import threading
import time

_allThreads = []


class SyncThread(object):
    """
    Class used to provide a simple synchronization thread
    """

    def __init__(self, root):
        self._root = root
        self._thread = None
        self._tick_delay = 5.0
        self._running = False
        self._condition = threading.Condition()
        self._last_run_time = time.time()
        self._run_limit = 10
        self._consecutive_runs = self._run_limit
        self._throttle_secs = 3
        self._run_window = 1.0

    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, value):
        if self._running != value:
            self._running = value
            if not value:
                self.notify()  # Hit condition variable

    @property
    def condition(self):
        return self._condition

    def notify(self):
        with self._condition:
            self._condition.notify_all()

    def throttle(self):
        # Limit number of times running within a given time window
        if self._consecutive_runs >= self._run_limit:
            time.sleep(self._throttle_secs)
            self._consecutive_runs = 0

        # Count number of times ran in the same second
        if time.time() - self._last_run_time < self._run_window:
            self._consecutive_runs += 1

    def wait(self):
        self.throttle()

        with self._condition:
            self._condition.wait(self._tick_delay)
            self._last_run_time = time.time()

    @staticmethod
    def stop_all_threads(wait_delay=0):
        all_threads = list(_allThreads)

        for item in all_threads:
            item.stop(wait_delay)

    @staticmethod
    def _thread_main(root):
        root.sync_message = ['Synchronization starting']
        root.sync_thread.running = True

        while root.sync_thread.running:
            root.sync_thread.wait()

            if root.sync_thread.running:
                root.sync()

        logging.info('Sync:Thread: {} thread exiting'.format(root.name))

    def start(self, signal_notify=True):
        """
        Start up a background thread to keep site synchronized

        :param signal_notify: (boolean) Call the 'notify' method immediately instead of waiting for
                                        and initial tick_interval before first running the thread
        """
        if not self.running:
            logging.info('Starting up synchronization thread for {}'.format(self._root.name))
            self._thread = threading.Thread(name=self._root.name, target=SyncThread._thread_main,
                                            kwargs={'root': self._root})
            if signal_notify:
                self._consecutive_runs = 0

            self._thread.start()
            _allThreads.append(self)

            if signal_notify:
                self.notify()

    def stop(self, wait_delay=0):
        """
        Start up a background thread to keep site synchronized

        :param: wait_delay (integer) Milliseconds to wait for graceful exit. 0 = no delay
        """
        if self.running:
            self.running = False

            _allThreads.remove(self)

            logging.info('Halting up synchronization thread for {}, delay: {}'.format(self._root.name,
                                                                                      wait_delay))
            if wait_delay > 0 and self._thread is not None:
                self._thread.join(wait_delay)

            self._thread = None
