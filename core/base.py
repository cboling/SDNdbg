import datetime
from uuid import uuid4


class Base(object):
    """
    Base class for node & edge objects

    This class provides a set of common properties and methods implemented by most all other
    orchestrator objects (site, user, vnf, ...).
    """
    states = ['initial', 'discovery', 'in_sync', 'updating', 'deleting', 'deleted']

    transitions = [
        # TODO
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

        self._name = kwargs.get('name')
        self._id = kwargs.pop('id', str(uuid4()))

    def __str__(self):
        return '{} [{}]'.format(self.name, self.id)

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
        Unique name of this object

        :return: (string) Name
        """
        return self._name

        # TODO: Move more common items from node/edge to here
