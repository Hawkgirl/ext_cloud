from abc import ABCMeta, abstractmethod, abstractproperty

class BaseSubnetcls:
        __metaclass__ = ABCMeta

	@property
	def resource_type(self): return 'subnet'

        @abstractproperty
        def name(self): pass

        @abstractproperty
        def id(self): pass

        @abstractproperty
        def state(self): pass

