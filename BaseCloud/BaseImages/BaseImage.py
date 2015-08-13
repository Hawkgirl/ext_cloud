from abc import ABCMeta, abstractmethod, abstractproperty

class BaseImagecls:
        __metaclass__ = ABCMeta

        @abstractproperty
        def name(self): pass

        @abstractproperty
        def id(self): pass

        @abstractproperty
        def size(self): pass

        @abstractproperty
        def state(self): pass

