from ext_cloud.BaseCloud.BaseResources.BaseResources import BaseResourcescls
from ext_cloud.OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls

class OpenStackResourcescls(OpenStackBaseCloudcls, BaseResourcescls):

	def __init__(self, *args, **kwargs):
		self.__args = args
		self.__kwargs = kwargs
                super(OpenStackResourcescls, self).__init__(credentials=kwargs)

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

	def list_zombie_resources(self):
		resources = []
		tenants_set = set()
		users_set = set()
		from ext_cloud.OpenStack.OpenStackIdentity.OpenStackIdentity import OpenStackIdentitycls
                tenants = OpenStackIdentitycls(**self._credentials).list_tenants()
		for tenant in tenants:
			tenants_set.add(tenant.id)	
                users = OpenStackIdentitycls(**self._credentials).list_users()
		for user in users:
			users_set.add(user.id)


		from ext_cloud.OpenStack.OpenStack import OpenStackcls
		openstack_obj = OpenStackcls(*self.__args,**self.__kwargs)
		lst_childrens = openstack_obj.Childrens
		for child in lst_childrens:
			if hasattr(child, 'user_id'):
				if not child.user_id in users_set:
					resources.append(child)
			if hasattr(child, 'tenant_id'):
				if not child.tenant_id in tenants_set:
					resources.append(child)

			if hasattr(child, 'Childrens'):
				lst_childrens += child.Childrens
		return resources

	# do not include users 
	def list_zombie_resources_by_tenants(self):
		resources = []
		tenants_set = set()
		from ext_cloud.OpenStack.OpenStackIdentity.OpenStackIdentity import OpenStackIdentitycls
                tenants = OpenStackIdentitycls(**self._credentials).list_tenants()
		for tenant in tenants:
			tenants_set.add(tenant.id)	

		from ext_cloud.OpenStack.OpenStack import OpenStackcls
		openstack_obj = OpenStackcls(*self.__args,**self.__kwargs)
		lst_childrens = openstack_obj.Childrens
		for child in lst_childrens:
			if hasattr(child, 'tenant_id'):
				if not child.tenant_id in tenants_set:
					resources.append(child)

			if hasattr(child, 'Childrens'):
				lst_childrens += child.Childrens
		return resources


