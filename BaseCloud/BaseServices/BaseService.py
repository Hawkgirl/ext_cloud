from abc import ABCMeta, abstractmethod, abstractproperty


class BaseServicecls:
    __metaclass__ = ABCMeta

    @abstractproperty
    def id(self):
        pass

    @abstractproperty
    def name(self):
        pass

    @abstractproperty
    def state(self):
        pass

    @abstractproperty
    def status(self):
        pass

    @abstractproperty
    def port(self):
        pass

    @abstractproperty
    def host(self):
        pass
