from abc import ABCMeta, abstractmethod, abstractproperty

class BaseUsercls:
        __metaclass__ = ABCMeta

        @abstractproperty
        def name(self): pass

        @abstractproperty
        def id(self): pass

        @abstractproperty
        def email_id(self): pass

        @abstractproperty
        def status(self): pass

