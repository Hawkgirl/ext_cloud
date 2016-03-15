from ext_cloud.BaseCloud.BaseIdentity.BaseIdentity import BaseIdentitycls
from ext_cloud.OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls
from ext_cloud.OpenStack.utils.OpenStackClients import OpenStackClientsCls

class OpenStackIdentitycls(OpenStackBaseCloudcls, BaseIdentitycls):

        def __init__(self, *args, **kwargs):
		super(OpenStackIdentitycls, self).__init__(credentials = kwargs)

	def list_metrics(self):
                from ext_cloud.BaseCloud.BaseResources.BaseMetrics import BaseMetricscls
                metrics = []
		metrics.append(BaseMetricscls('openstack.tenants.count', len(self.list_tenants())))
		metrics.append(BaseMetricscls('openstack.users.count', len(self.list_users())))

		#alltenants metrics
                import datetime
		
                now = datetime.datetime.utcnow()
		usages = self._NovaClient.usage.list(now-datetime.timedelta(days=1), now, detailed=True)
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

		from dateutil.relativedelta import relativedelta
		one_month_back =  now - relativedelta(months=1)
		usages = self._NovaClient.usage.list(one_month_back, now, detailed=True)
		vms = total_memory_mb_usage = total_local_gb_usage = total_vcpus_usage = 0

		for usage in usages:
			total_vcpus_usage += usage.total_vcpus_usage
			total_memory_mb_usage += usage.total_memory_mb_usage
			total_local_gb_usage += usage.total_local_gb_usage
			vms += len(usage.server_usages)

		metrics.append(BaseMetricscls('openstack.alltentant1month.hours_cpu', total_vcpus_usage))
		metrics.append(BaseMetricscls('openstack.alltentant1month.hours_memory', total_memory_mb_usage))
		metrics.append(BaseMetricscls('openstack.alltentant1month.hours_disk', total_local_gb_usage))
		metrics.append(BaseMetricscls('openstack.alltentant1month.used_vm', vms))
		return metrics

	@property
        def Childrens(self):
                return  self.list_tenants()


	def list_users(self):
		from ext_cloud.OpenStack.OpenStackIdentity.OpenStackUser import OpenStackUsercls
		openstack_users = self._KeystoneClient.users.list()
		users = [ ]
		for openstack_user in openstack_users:
			user = OpenStackUsercls(openstack_user, credentials=self._credentials)
			users.append(user)
		return users

	def get_user_by_id(self, user_id):
		from ext_cloud.OpenStack.OpenStackIdentity.OpenStackUser import OpenStackUsercls
		from keystoneclient.openstack.common.apiclient.exceptions import NotFound
		try:
			openstack_user = self._KeystoneClient.users.get(user_id)
		except NotFound as e:
			# user got deleted
			return None

		user = OpenStackUsercls(openstack_user, credentials=self._credentials)
		return user

	def list_tenants(self): 
		from ext_cloud.OpenStack.OpenStackIdentity.OpenStackTenant import OpenStackTenantcls
		openstack_tenants = self._KeystoneClient.tenants.list()
		tenants = [ ]
		for openstack_tenant in openstack_tenants:
			tenant = OpenStackTenantcls(openstack_tenant, credentials=self._credentials)
			tenants.append(tenant)
		return tenants

	def get_tenant_by_id(self, tenant_id):
		from ext_cloud.OpenStack.OpenStackIdentity.OpenStackTenant import OpenStackTenantcls
		from keystoneclient.openstack.common.apiclient.exceptions import NotFound
		try:
			openstack_tenant = self._KeystoneClient.tenants.get(tenant_id)
		except NotFound as e:
			return None
		tenant = OpenStackTenantcls(openstack_tenant, credentials=self._credentials)
		return tenant

