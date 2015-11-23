from ext_cloud.BaseCloud.BaseStats.BaseStats import BaseStatscls

class OpenStackStatscls(BaseStatscls):

	def __init__(self, *args, **kwargs):
		self.__args = args
		self.__kwargs = kwargs
                super(OpenStackStatscls, self).__init__()

	def list_metrics(self):
		metrics = []
		from ext_cloud.OpenStack.OpenStack import OpenStackcls
		openstack_obj = OpenStackcls(*self.__args,**self.__kwargs)
		lst_childrens = openstack_obj.Childrens
		for child in lst_childrens:
			child_metrics = child.list_metrics()
			metrics += child_metrics
			if hasattr(child, 'Childrens'):
				lst_childrens += child.Childrens
		return metrics

