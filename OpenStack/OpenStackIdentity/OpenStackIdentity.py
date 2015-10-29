from BaseCloud.BaseIdentity.BaseIdentity import BaseIdentitycls
from keystoneclient.v2_0 import client as KeystoneClient
from OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls

class OpenStackIdentitycls(OpenStackBaseCloudcls, BaseIdentitycls):
        __keystoneclient = None

        def __init__(self, *args, **kwargs):
		self._credentials = kwargs

	def list_metrics(self):
                from BaseCloud.BaseStats.BaseMetrics import BaseMetricscls
                metrics = []
		metrics.append(BaseMetricscls('openstack.tenants.count', len(self.list_tenants())))
		metrics.append(BaseMetricscls('openstack.users.count', len(self.list_users())))
		return metrics

	@property
        def Childrens(self):
                return  self.list_tenants()


	@property
        def __KeystoneClient(self):
                return self.__keystoneclient

        @__KeystoneClient.getter
        def __KeystoneClient(self):
                if self.__keystoneclient is None:
                        self.__keystoneclient = KeystoneClient.Client(**self._credentials)
                return self.__keystoneclient

	def list_users(self):
		from OpenStack.OpenStackIdentity.OpenStackUser import OpenStackUsercls
		openstack_users = self.__KeystoneClient.users.list()
		users = [ ]
		for openstack_user in openstack_users:
			user = OpenStackUsercls(openstack_user, credentials=self._credentials)
			users.append(user)
		return users

	def list_tenants(self): 
		from OpenStack.OpenStackIdentity.OpenStackTenant import OpenStackTenantcls
		openstack_tenants = self.__KeystoneClient.tenants.list()
		tenants = [ ]
		for openstack_tenant in openstack_tenants:
			tenant = OpenStackTenantcls(openstack_tenant, credentials=self._credentials)
			tenants.append(tenant)
		return tenants
