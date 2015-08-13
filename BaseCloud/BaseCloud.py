from abc import ABCMeta, abstractmethod, abstractproperty

class Cloudcls:
	__metaclass__ = ABCMeta

	@abstractproperty
	def identity(self): pass
	
	@abstractproperty
	def compute(self): pass

	@abstractproperty
	def networks(self): pass

	@abstractproperty
	def images(self): pass

	@abstractproperty
	def volumes(self): pass

	@abstractproperty
	def objectstore(self): pass

	@abstractproperty
	def templates(self): pass

	@abstractmethod
        def validate_credentials(self): pass


