from BaseCloud.BaseStats.BaseStats import BaseStatscls

class OpenStackStatscls(BaseStatscls):

	def __init__(self, *args, **kwargs):
		self.__args = args
		self.__kwargs = kwargs
                super(OpenStackStatscls, self).__init__()

	def get_metrics(self):
		metrics = []
		from OpenStack.OpenStack import OpenStackcls
		openstack_obj = OpenStackcls(*self.__args,**self.__kwargs)
		for child in openstack_obj.Childrens:
			child_metrics = child.get_metrics()
			metrics += child_metrics
		return metrics

