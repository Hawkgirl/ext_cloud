from abc import ABCMeta, abstractproperty


class BaseGatewaycls:
    __metaclass__ = ABCMeta

    @abstractproperty
    def name(self):
        pass

    @abstractproperty
    def id(self):
        pass

    @abstractproperty
    def state(self):
        pass
