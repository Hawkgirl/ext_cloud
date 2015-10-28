from abc import ABCMeta, abstractmethod, abstractproperty

class BaseStatscls:
	__metaclass__ = ABCMeta

	@abstractmethod
        def list_metrics(self): pass
