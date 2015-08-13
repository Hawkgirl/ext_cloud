from abc import ABCMeta, abstractmethod, abstractproperty

class BaseSecurityGroupcls:
	__metaclass__ = ABCMeta

	@abstractproperty
	def name(self): pass

	@abstractproperty
	def id(self): pass

	@abstractproperty
	def description(self): pass

	@abstractproperty
	def rules(self): pass

	@abstractproperty
	def delete(self): pass

	@abstractproperty
	def add_rule(self, ip_protocol='tcp', from_port=None, to_port=None, cidr_block=None): pass

	@abstractproperty
	def delete_rule(self, ip_protocol='tcp', from_port=None, to_port=None, cidr_block=None): pass
