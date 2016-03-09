from abc import ABCMeta, abstractmethod, abstractproperty

from enum import Enum
class STATE(Enum):
        UNKNOWN = 0,
        READY = 1,
        ATTACHED = 2,
        ERROR = 3

class BaseVolumecls:
        __metaclass__ = ABCMeta

        @abstractproperty
        def name(self): pass

        @abstractproperty
        def id(self): pass

        @abstractproperty
        def size(self): pass

        @abstractproperty
        def state(self): pass

