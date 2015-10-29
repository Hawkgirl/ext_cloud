from BaseCloud.BaseIdentity.BaseIdentity import BaseIdentitycls
from keystoneclient.v2_0 import client as KeystoneClient
from OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls
from OpenStack.utils.OpenStackClients import OpenStackClientsCls

class OpenStackIdentitycls(OpenStackBaseCloudcls, BaseIdentitycls):
        __keystoneclient = None
	__novaclient = None

        def __init__(self, *args, **kwargs):
		self._credentials = kwargs


	@property
        def __NovaClient(self):
                return self.__novaclient

        @__NovaClient.getter
        def __NovaClient(self):
                if self.__novaclient is None:
                        self.__novaclient = OpenStackClientsCls().get_nova_client(self._credentials)
                return self.__novaclient

	def list_metrics(self):
                from BaseCloud.BaseStats.BaseMetrics import BaseMetricscls
                metrics = []
		metrics.append(BaseMetricscls('openstack.tenants.count', len(self.list_tenants())))
		metrics.append(BaseMetricscls('openstack.users.count', len(self.list_users())))

		#alltenants metrics
                import datetime
                now = datetime.datetime.now()
		usages = self.__NovaClient.usage.list(now-datetime.timedelta(days=1), now, detailed=True)
		vms = total_memory_mb_usage = total_local_gb_usage = total_vcpus_usage = 0

		for usage in usages:
			total_vcpus_usage += usage.total_vcpus_usage
			total_memory_mb_usage += usage.total_memory_mb_usage
			total_local_gb_usage += usage.total_local_gb_usage
			vms += len(usage.server_usages)

		metrics.append(BaseMetricscls('openstack.alltentant1day.hours_cpu', total_vcpus_usage))
		metrics.append(BaseMetricscls('openstack.alltentant1day.hours_memory', total_memory_mb_usage))
		metrics.append(BaseMetricscls('openstack.alltentant1day.hours_disk', total_local_gb_usage))
		metrics.append(BaseMetricscls('openstack.alltentant1day.used_vm', vms))
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
