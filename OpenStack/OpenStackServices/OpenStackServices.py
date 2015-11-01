from BaseCloud.BaseServices.BaseServices import BaseServicescls 
from OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls

class OpenStackServicescls(OpenStackBaseCloudcls, BaseServicescls):
	__novaclient = None
	__neutronclient = None
	__cinderclient = None

	def __init__(self, *args, **kwargs):
		self._credentials = kwargs

	@property
        def Childrens(self):
                return [] 

	def list_metrics(self):
		metrics = []
		metrics += self.__list_metrics(self.list_compute_services())
		metrics += self.__list_metrics(self.list_network_services())
		metrics += self.__list_metrics(self.list_volume_services())
		return metrics
	def __list_metrics(self, services):
		if len(services) is 0: return []
		from BaseCloud.BaseStats.BaseMetrics import BaseMetricscls
                metrics = []
		metric_str = 'openstack.' + services[0].group + '.services.'
		enabled = disabled = up = down = 0
		for service in services:
			
			if service.state == 'up': up += 1
			elif service.state == 'down': down += 1
			else: pass
	
			if service.status == 'enabled': enabled += 1
			elif service.status == 'disabled': disabled += 1
			else: pass
		metrics.append(BaseMetricscls(metric_str + 'up', up))
		metrics.append(BaseMetricscls(metric_str + 'down', down))
		metrics.append(BaseMetricscls(metric_str + 'enabled', enabled))
		metrics.append(BaseMetricscls(metric_str + 'disabled', disabled))
			
		return metrics

 	@property
        def __NovaClient(self):
                return self.__novaclient

        @__NovaClient.getter
        def __NovaClient(self):
                if self.__novaclient is None:
			from OpenStack.utils.OpenStackClients import OpenStackClientsCls
                        self.__novaclient = OpenStackClientsCls().get_nova_client(self._credentials)
                return self.__novaclient
	
	@property
        def __NeutronClient(self):
                return self.__neutronclient

        @__NeutronClient.getter
        def __NeutronClient(self):
                if self.__neutronclient is None:
                        from OpenStack.utils.OpenStackClients import OpenStackClientsCls
                        self.__neutronclient = OpenStackClientsCls().get_neutron_client(self._credentials)
                return self.__neutronclient

	@property
        def __CinderClient(self):
                return self.__cinderclient

        @__CinderClient.getter
        def __CinderClient(self):
                if self.__cinderclient is None:
                        from OpenStack.utils.OpenStackClients import OpenStackClientsCls
                        self.__cinderclient = OpenStackClientsCls().get_cinder_client(self._credentials)
                return self.__cinderclient


	def list_services(self):
		services = []
		services += self.list_compute_services()
		services += self.list_network_services()
		return services

	def list_compute_services(self):
		services = []
		nova_services = self.__NovaClient.services.list()
		for nova_service in nova_services:
			kwargs = {}
			kwargs['id']= nova_service.id
			kwargs['name'] = nova_service.binary
			kwargs['group'] = 'nova'
			kwargs['state'] = nova_service.state
			kwargs['status'] = nova_service.status
			kwargs['host'] = nova_service.host
			from OpenStack.OpenStackServices.OpenStackService import OpenStackServicecls
			service = OpenStackServicecls(**kwargs)
			services.append(service)
			
		return services

	def list_network_services(self):
		services = []
		neutron_services = self.__NeutronClient.list_agents()['agents']
		for service in neutron_services:
			kwargs = {}
                        kwargs['id']= service['id']
                        kwargs['name'] = service['binary']
                        kwargs['group'] = 'network'
                        kwargs['state'] = 'up' if service['alive'] is True else 'down'
                        kwargs['status'] = 'enabled' if service['admin_state_up'] is True else 'disabled'
                        kwargs['host'] = service['host']
                        from OpenStack.OpenStackServices.OpenStackService import OpenStackServicecls
                        service = OpenStackServicecls(**kwargs)
                        services.append(service)

                return services

	def list_volume_services(self):
		services = []
		volume_services = self.__CinderClient.services.list()
		for service in volume_services:
                        kwargs = {}
                        kwargs['id']= service.binary
                        kwargs['name'] = service.binary
                        kwargs['group'] = 'volumes'
                        kwargs['state'] = service.state
                        kwargs['status'] = service.status
                        kwargs['host'] = service.host
                        from OpenStack.OpenStackServices.OpenStackService import OpenStackServicecls
                        service = OpenStackServicecls(**kwargs)
                        services.append(service)

                return services
