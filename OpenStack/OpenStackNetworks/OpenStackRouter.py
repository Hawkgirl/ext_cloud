from BaseCloud.BaseNetworks.BaseRouter import BaseRoutercls
from OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls

class OpenStackRoutercls(OpenStackBaseCloudcls, BaseRoutercls):
	
	__openstack_router = None
	__neutronclient = None

	def __init__(self, *arg, **kwargs):
                self.__openstack_router = arg[0]

                super(OpenStackRoutercls, self).__init__(id=self.__openstack_router['id'], name=self.__openstack_router['name'], credentials=kwargs['credentials'])



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
        def state(self): return self.__openstack_router['status']

	def delete(self): pass

	def add_route(self, destination_cidr_block=None, gateway_id=None, instance_id=None, interface_id=None): pass

	def attach_nic(self, nic_id): pass
	def attach_subnet(self, subnet_id):
		self.__NeutronClient.add_interface_router(self.id, {'subnet_id':subnet_id})
