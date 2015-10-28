from BaseCloud.BaseNetworks.BaseNIC import BaseNICcls
from OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls

class OpenStackNICcls(OpenStackBaseCloudcls, BaseNICcls):
	
	__openstack_nic = None

	def __init__(self, *arg, **kwargs):
                self.__openstack_nic = arg[0]

                super(OpenStackNICcls, self).__init__(id=self.__openstack_nic['id'], name=self.__openstack_nic['name'], credentials=kwargs['credentials'])


        @property
        def state(self): return self.__openstack_nic['status']

	@property
	def mac_address(self): return self.__openstack_nic['mac_address']

	@property
	def network_id(self): return self.__openstack_nic['network_id']

	@property
	def subnet_id(self): 
		if self.__openstack_nic.has_key('fixed_ips'):
			return self.__openstack_nic['fixed_ips'][0]['subnet_id']
		return None

	@property
	def ip_address(self):
		if self.__openstack_nic.has_key('fixed_ips'):
			return self.__openstack_nic['fixed_ips'][0]['ip_address']
		return None

