from abc import ABCMeta, abstractmethod, abstractproperty


class BaseSnapshotcls:
    __metaclass__ = ABCMeta

    @property
    def resource_type(self):
        return 'snapshot'

    @abstractproperty
    def name(self):
        pass

    @abstractproperty
    def id(self):
        pass

    @abstractproperty
    def size(self):
        pass

    @abstractproperty
    def state(self):
        pass
