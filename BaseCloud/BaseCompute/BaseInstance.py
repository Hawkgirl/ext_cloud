from abc import ABCMeta, abstractmethod, abstractproperty

class BaseInstancecls:
	__metaclass__ = ABCMeta

	@abstractproperty
	def id(self): pass

	@abstractproperty
	def size(self): pass
	
	@abstractproperty
	def name(self): pass

	@abstractproperty
	def public_ip(self): pass

	@abstractproperty
	def state(self): pass

	@abstractproperty
        def image_id(self): pass
	
	@abstractproperty
        def image_name(self): pass

	@abstractproperty
        def arch(self): pass 

	@abstractproperty
        def network_id(self): pass

	@abstractproperty
        def subnet_id(self): pass

	@abstractproperty
        def private_ip(self): pass

	@abstractproperty
        def public_ip(self): pass

	@abstractproperty
        def keypair_name(self): pass

	@abstractproperty
        def dns_name(self): pass

	@abstractproperty
        def creation_time(self): pass

	@abstractproperty
        def os_type(self): pass

	@abstractmethod
	def start(self): pass

	@abstractmethod
	def stop(self): pass

	@abstractmethod
	def reboot(self): pass

	@abstractmethod
	def delete(self): pass

	@abstractmethod
	def addtag(self, name=None, value=None): pass

	@abstractmethod
	def gettags(self):  pass
