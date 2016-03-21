from abc import ABCMeta, abstractmethod, abstractproperty


class BaseBucketcls:
    __metaclass__ = ABCMeta

    @abstractproperty
    def name(self): pass

    @abstractproperty
    def id(self): pass

    @abstractproperty
    def get_all_keys(self): pass

    @abstractproperty
    def delete(self): pass
