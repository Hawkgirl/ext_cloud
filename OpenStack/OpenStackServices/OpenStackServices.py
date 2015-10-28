from BaseCloud.BaseServices.BaseServices import BaseServicescls 
from OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls

class OpenStackServicescls(OpenStackBaseCloudcls, BaseServicescls):
	__novaclient = None
	def __init__(self, *args, **kwargs):
		self._credentials = kwargs

	@property
        def Childrens(self):
                return [] 

	def list_metrics(self):
		return []

 	@property
        def __NovaClient(self):
                return self.__novaclient

        @__NovaClient.getter
        def __NovaClient(self):
                if self.__novaclient is None:
			from OpenStack.utils.OpenStackClients import OpenStackClientsCls
                        self.__novaclient = OpenStackClientsCls().get_nova_client(self._credentials)
                return self.__novaclient
	
	def list_services(self):
		services = []
		services += self.list_compute_services()
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
		pass
