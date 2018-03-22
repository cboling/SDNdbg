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

import datetime
import logging
import random
from uuid import UUID

from transitions import Machine

from utils import get_uuid

# Some constants
DEFAULT_UPDATE_INTERVAL_SECS = 60  # When in sync, default 'update with VIM' delta in seconds


class Base(object):
    """
    Base class for node & edge objects

    This class provides a set of common properties and methods implemented by most all other
    orchestrator objects (site, user, vnf, ...).

    An object of a class derived from 'Base' will exist in one of 5 states. The definition of each
    state is defined below:

    OUT_OF_SYNC This is the initial state of an object an when it is first created and after connectivity
                to the server/system supporting the object has been lost.  Once connectivity is achieved,
                the object will be queried and its state information is saved.  If it provides any child nodes,
                then these are discovered during this time.

                Should connectivity be lossed to an object and this state re-entered, the object will be
                periodically polled and once connectivity re-established, any children will be validated and
                new/missing ones updated.  Note that if a child is found to be missing, it will be signaled to
                enter the 'deleting' state.

                Discovery of any children will result in the creation of an proper object to wrap that child and
                discovery will occur for that child at a later time.

                If communications is successful and the object is properly updated, it will enter the IN_SYNC state.
                If communications should fail, the object will remain in the OUT_OF_SYNC state and be polled again
                at a future point in time.

    IN_SYNC     This state is for an object that has been successfully discovered. Once a database is supported,
                this would be an ideal state to save off any information into.

    UPDATING    This state is called periodically, or upon request to perform an update of any state and child
                information.  While it performs many of the steps of the OUT_OF_SYNC state, this state should
                help allow an outside observer to know that the object was previously IN_SYNC, but it is just
                going through normal and expected status updates.

    DELETED     This state is entered when it can no long be located or has been manually deleted by an operator.

    """
    _states = ['out_of_sync', 'in_sync', 'updating', 'deleted']

    _transitions = [
        {'trigger': 'tick', 'source': 'out_of_sync', 'dest': 'updating'},

        {'trigger': 'success', 'source': 'updating', 'dest': 'in_sync'},
        {'trigger': 'failure', 'source': 'updating', 'dest': 'out_of_sync'},
        {'trigger': 'missing', 'source': 'updating', 'dest': 'deleting'},

        {'trigger': 'tick', 'source': 'in_sync', 'dest': 'updating', 'conditions': ['sync_enabled', 'update_ok']},

        # Do wildcard 'delete' trigger last so it covers all previous states
        {'trigger': 'delete', 'source': '*', 'dest': 'deleted'},
    ]

    # TODO: Support a 'modified' trigger
    #
    #       A 'modified' trigger should be use to flag that the object is Out-of-sync (if not already) and
    #       should tie in with the 'modified' boolean flag. Other options may also exist on how to handle
    #       modifications. Needs to be thread safe

    def __init__(self, **kwargs):
        """
        Initialize common settings.  The following are properties common to most all objects
        """
        # Set 'database' container first as needed to validate name uniqueness

        now = datetime.datetime.utcnow()
        self._create_time = now
        self._last_update_time = None
        self._config = kwargs.pop('config', None)

        self._last_synced_time = None
        self._last_unsynced_time = now
        self._i_am_synced = False
        self._sync_thread = None
        self._update_interval = kwargs.pop('update_interval', DEFAULT_UPDATE_INTERVAL_SECS)
        self._update_message = ['Initial discovery has not yet occured']
        self._no_sync = kwargs.pop('no_sync', False)
        self._cache_client = kwargs.pop('cache_client', False)

        self._name = kwargs.pop('name')
        self._id = UUID(kwargs.pop('id', str(get_uuid())))

        self._parent = kwargs.get('parent', None)  # Do not 'pop'
        self._children = kwargs.pop('children', [])

        self._enabled = kwargs.get('enabled', True)
        self._delete_pending = False
        self._modified = False

        self._metadata = kwargs.pop('metadata', {})

        self._client = None

        # Validate parameters

        if self.name is None or len(self.name) == 0:
            raise ValueError('Invalid/missing unique name not provided')

        if self.parent is not None and not isinstance(self.parent, Base):
            raise ValueError("Parent of {} must be derived from 'Base', type is '{}".format(self.name,
                                                                                            type(self.parent)))
        if not isinstance(self.children, list):
            raise ValueError("Children of {} must be supplied as a list or 'None', type is '{}".
                             format(self.name, type(self.children)))
        cnt = 1
        for child in self.children:
            if not isinstance(child, Base):
                raise ValueError("Child #{} of {} must be derived from 'Base', type is '{}".
                                 format(cnt, self.name, type(child)))
            cnt += 1

        # Set up state machine to manage states

        self._machine = Machine(model=self, states=Base._states,
                                transitions=Base._transitions,
                                initial='out_of_sync',
                                queued=True,
                                name='{} [{}]'.format(self.__class__.__name__, self.name))

    def __str__(self):
        return '{} [{}]'.format(self.name, self.id)

    def __repr__(self):
        return '%s.(%r)' % (self.__class__, self.__dict__)

    def __eq__(self, other):
        return isinstance(other, Base) and self.id == other.id

    @property
    def id(self):
        """
        Unique orchestrator ID of this object
        :return: UUID
        """
        return self._id

    @property
    def name(self):
        """
        Name of this object

        :return: (string) Name
        """
        return self._name

    @property
    def parent(self):
        """
        Parent objects
        :return: parent
        """
        return self._parent

    @property
    def children(self):
        """
        Child objects
        :return: (list) of children
        """
        return self._children

    @property
    def config(self):
        """
        Configuration object
        :return: (Config) Configuration, None if item was fully discovered
        """
        return self._config

    @property
    def enabled(self):
        """
        Flag indicating that this object is enabled

        :return: (boolean) True if enabled
        """
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        if self.enabled != value:
            self._enabled = value
            self.modified = True

    @property
    def delete_pending(self):
        """
        Flag indicating that this object is in the process of being deleted (if true)

        :return: (boolean) True if object deletion has been requested
        """
        return self._delete_pending

    @delete_pending.setter
    def delete_pending(self, value):
        if value:
            raise ValueError('Delete Pending for an object can only be set to True')

        if self._delete_pending != value:
            self._delete_pending = value
            if value:
                self.delete()

            self.modified = True

    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, value):
        self._metadata = value

    @property
    def cache_client(self):
        return self._cache_client

    @cache_client.setter
    def cache_client(self, value):
        self._cache_client = value

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, value):
        self._client = value

    @property
    def modified(self):
        """
        Flag indicating that this object has modified since last 'saved' to a back database store

        :return: (boolean) True if modified
        """
        return self._modified

    @modified.setter
    def modified(self, value):
        """
        Flag indicating that this object has modified since last 'saved' to a back database store

        :param value: (boolean) Flag indicating if this object has been modified
        """
        if self.modified != value:
            logging.debug('Setting modified to {}'.format(value))
            self._modified = value

            if self._no_sync:
                pass  # Save to database

            elif value:
                # Clear synchronized flag.  Will be saved to database once we synchronize (and we have a database)
                self.i_am_synced = False
                self.notify_sync_thread()

            elif self.i_am_synced:
                pass  # Save to database

    def notify_sync_thread(self):
        # Walk ancestors to find sync thread and signal it to run
        if self.sync_thread is not None:
            self.sync_thread.notify()

        elif self.parent is not None:
            self.parent.notify_sync_thread()

    @property
    def no_sync(self):
        """
        Flag indicating that this object should not be synchronized

        :return: (boolean) True if synchronization is disabled
        """
        return self._no_sync

    @no_sync.setter
    def no_sync(self, value):
        """
        Flag indicating that this object is not synchronized with its respective driver

        :param value: (boolean) True if synchronization is disabled
        """
        if self._no_sync != value:
            logging.info('Setting no_sync to {}'.format(value))
            self._no_sync = value

    def sync_enabled(self):
        """
        Is synchronization enabled for this object
        :return: True if enabled
        """
        return not self.no_sync

    @property
    def sync_time(self):
        """
        UTC Time when this object was last marked as synchronized

        :return: (DateTime)
        """
        return self._last_synced_time

    @property
    def discontinuity_time(self):
        """
        UTC Time when this object was last marked as not synchronized

        :return: (DateTime)
        """
        return self._last_unsynced_time

    @property
    def create_time(self):
        """
        UTC Time when this object was first created

        :return: (DateTime)
        """
        return self._create_time

    @property
    def last_update_time(self):
        """
        The last time the update_status method was called to update with the VIM and a
        successful update was performed

        :return: (DateTime) UTC last successful update time
        """
        return self._last_update_time

    @property
    def status_update_interval(self):
        """
        When in sync, default 'update with VIM' delta in seconds

        :return: (Int) delta seconds between updates
        """
        return self._update_interval

    @status_update_interval.setter
    def status_update_interval(self, value):
        """
        Delta seconds between VIM update when the object is 'in-sync'

        :param value: (Int) delta seconds between updats
        """
        if value <= 0:
            raise ValueError('Update delta must be > 0 seconds')

        self._update_interval = value

    def update_ok(self):
        """
        Is this object (in the In-Sync state) ready to do a status poll.  The time
        to do a poll on a particular item is dependent upon the last time it was
        updated.

        :return: True if it is time to do a status poll
        """
        # TODO: Need to support an update 'immediately' capability

        if self.last_update_time is None:
            return True

        # Skew all update intervals by up to +20% each check to lessen the chance of
        # all updates firing at once/clump together

        delta_time = datetime.datetime.utcnow() - self.last_update_time
        delta_time += datetime.timedelta(seconds=random.randint(0, 20))

        return delta_time >= datetime.timedelta(seconds=self.status_update_interval)

    @property
    def sync_message(self):
        """
        Synchronization status message of current synchronization status / error

        :return: (string)
        """
        return self._update_message if self._update_message is not None else []

    @sync_message.setter
    def sync_message(self, value):
        """
        Synchronization status message of current synchronization status / error
        """
        self._update_message = value

    @property
    def to_json(self):
        """
        Output information to simple JSON format
        :return: (list) edge 'data' elements
        """
        raise NotImplementedError("Required 'to_json' property not implemented")

    @property
    def sync_thread(self):
        """
        The Sync Thread controls synchronization from a ROOT object down to all children
        who do not have sync thread of their own

        :return: Sync thread for this object (if root)
        """
        return self._sync_thread

    @sync_thread.setter
    def sync_thread(self, thread_val):
        if self._sync_thread is not None and thread_val is not None:
            raise ValueError('You cannot switch sync threads without first disassociating with the previous thread')

        self._sync_thread = thread_val

    @property
    def i_am_synced(self):
        return self._i_am_synced

    @i_am_synced.setter
    def i_am_synced(self, value):
        """
        Flag indicating that this object is synchronized with its respective driver

        :param value: (boolean) True if synchronized
        """
        if self._i_am_synced != value:
            logging.info('Setting _i_am_synced to {}'.format(value))
            self._i_am_synced = value

            if value:
                self._last_synced_time = datetime.datetime.utcnow()
            else:
                self._last_unsynced_time = datetime.datetime.utcnow()

            self.modified = False

    def connect(self):
        """
        Each derived class should override this method and provide a method that attempts
        to connect to the proper server, library, or stub that can retrieve information
        on this object.  If no 'real' connection is required, just return anything but 'None'

        When the object's sync_object method is called, it can make use of this object by
        accessing the 'client' property.

        If the 'cache_client' property is False (default) the 'client' property is set back
        to 'None' on exiting of the 'updating' state

        :return: Client connection object/stub
        """
        raise NotImplementedError("Required 'connect' method not implemented")

    def perform_sync(self):
        """
        Each derived class should override this method as needed and make use of the 'client'
        property (created during 'connect') to update the object.

        You should discover any child nodes/links during this time and update as appropriate

        :return: True if synchronization was successful, False otherwise
        """
        return True

    def sync_object(self):
        """
        Perform common tasks for synchronizing in the OUT_OF_SYNC and UPDATING sates
        :return:
        """
        logging.info('sync_object: entry. {}'.format(self.name))

        if self.client is None:
            self.client = self.connect()

        # Attempt the synchronization

        success = self.perform_sync() if self.client is not None else False

        if success:
            self._last_synced_time = datetime.datetime.utcnow()
            self.success()
        else:
            self.failure()

    def on_enter_out_of_sync(self):
        """
        This method is called upon entering the out_of_sync step.
        """
        logging.info('on_enter_out_of_sync: entry. {}'.format(self.name))

        # Attempt a lookup.  If not found, need to create

        def stub_am_i_connected():  # Really, do I know enough to do anything
            return False

        if not stub_am_i_connected():
            self.sync_object()

    def on_enter_updating(self):
        """
        Entering the UPDATING state. Try and sync with the actual object
        """
        logging.info('on_enter_updating: entry. {}'.format(self.name))
        self.sync_object()

    def on_exit_updating(self):
        """
        Leaving the UPDATING state. Drop client if we do not cache it
        """
        logging.info('on_exit_updating: entry. {}'.format(self.name))

        if not self.cache_client:
            self.client = None

    def on_enter_deleted(self):
        """
        Entering the DELETED state.  Drop any client connections and signal all decedent
        children to delete as well.
        """
        logging.info('on_enter_deleted: entry. {}'.format(self.name))
        self.client = None

        # Force all child objects into the deleted state as well

        for child in self.children:
            child.delete_pending = True

    def sync(self):
        """
        Synchronize this object with the underlying VIM
        """
        logging.info('Sync: {} entry: no sync: {}, deleted: {}'.format(self, self.no_sync, self.is_deleted))

        if self.no_sync or self.is_deleted() or self.delete_pending:
            return

        try:
            self.tick()

        except Exception as e:
            message = "Unhandled Exception while attempting to sync '{}': {}".format(self, e.message)
            logging.exception(message)
            messages = self.sync_message
            messages.append(message)
            self.sync_message = messages

        # If this object is in the in-sync state, send a tick() to all children UNLESS they
        # have their own sync thread

        if self.is_in_sync():
            logging.info('Sync: {}, {} children'.format(self, len(self._children)))

            for child in self.children:
                # Do not recurse into children that are marked as a root for synchronization by
                # another sync thread

                if child.sync_thread is None and not self.delete_pending:
                    try:
                        child.sync()

                    except Exception as e:
                        message = "Unhandled Exception while attempting to sync '{}': {}".format(self, e.message)
                        logging.error(message)
                        messages = self.sync_message
                        messages.append(message)
                        self.sync_message = messages
