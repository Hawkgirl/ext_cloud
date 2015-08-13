from abc import ABCMeta, abstractmethod, abstractproperty

class BaseZonecls:
	__metaclass__ = ABCMeta

	@abstractproperty
	def id(self): pass

	@abstractproperty
	def name(self): pass
