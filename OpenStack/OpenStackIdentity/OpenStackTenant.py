from BaseCloud.BaseIdentity.BaseTenant import BaseTenantcls
from OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls
from OpenStack.utils.OpenStackClients import OpenStackClientsCls

class OpenStackTenantcls(OpenStackBaseCloudcls, BaseTenantcls):

        __openstack_tenant = None
	__keystoneclient = None
	__novaclient = None

	def __init__(self, *arg, **kwargs):
                self.__openstack_tenant = arg[0]
                super(OpenStackTenantcls, self).__init__(id=self.__openstack_tenant.id, name=self.__openstack_tenant.name, credentials=kwargs['credentials'])


	@property
        def __NovaClient(self):
                return self.__novaclient

        @__NovaClient.getter
        def __NovaClient(self):
                if self.__novaclient is None:
                        self.__novaclient = OpenStackClientsCls().get_nova_client(self._credentials)
                return self.__novaclient

	@property
        def __KeystoneClient(self):
                return self.__keystoneclient

        @__KeystoneClient.getter
        def __KeystoneClient(self):
                if self.__keystoneclient is None:
                        self.__keystoneclient = OpenStackClientsCls().get_keystone_client(self._credentials)
                return self.__keystoneclient


        @property
        def status(self):
                return 'enabled' if self.__openstack_tenant.enabled is True else 'disabled'

	@property
	def usage(self):
		from BaseCloud.BaseStats.BaseResourceUsage import BaseResourceUsagecls
		import datetime
	        now = datetime.datetime.now()
		epoch = datetime.datetime(year=1970, month=1, day=1)
        	tenant_usage = self.__NovaClient.usage.get(self.id, epoch, now)

		if not hasattr(tenant_usage, 'total_vcpus_usage'):
			return None
		usage_dict = {}
		usage_dict['hours_cpu'] = tenant_usage.total_vcpus_usage
		usage_dict['hours_disk'] = tenant_usage.total_local_gb_usage
		usage_dict['hours_memory'] = tenant_usage.total_memory_mb_usage

		deleted_vms = used_vms = 0
		for vm in tenant_usage.server_usages:
			if vm['state'] == 'terminated': deleted_vms += 1
			else: used_vms += 1
		usage_dict['deleted_vms'] = deleted_vms
		usage_dict['used_vms'] = used_vms

		return BaseResourceUsagecls(**usage_dict)

	def list_metrics(self):
		resource_usage = self.usage
		if resource_usage is None: return []
		
		from BaseCloud.BaseStats.BaseMetrics import BaseMetricscls
                metrics = []
                metric_str = 'openstack.tenant.' + self.name + '.' 
		for varible in dir(resource_usage):
                        if not varible.startswith("_") and isinstance(getattr(resource_usage.__class__, varible), property):
                                value = getattr(resource_usage, varible)
                                if value is None: continue
				metrics.append(BaseMetricscls(metric_str + varible, value))
                return metrics

