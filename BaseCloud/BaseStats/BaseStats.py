from abc import ABCMeta, abstractmethod, abstractproperty

class BaseStatscls:
	__metaclass__ = ABCMeta

	@abstractmethod
        def get_metrics(self): pass
