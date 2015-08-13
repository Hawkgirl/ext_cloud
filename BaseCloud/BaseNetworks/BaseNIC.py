from abc import ABCMeta, abstractmethod, abstractproperty

class BaseNICcls:
        __metaclass__ = ABCMeta

        @abstractproperty
        def name(self): pass

        @abstractproperty
        def id(self): pass

        @abstractproperty
        def state(self): pass

