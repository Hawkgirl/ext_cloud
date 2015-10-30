from BaseCloud.BaseNetworks.BaseNetwork import BaseNetworkcls
from OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls
from OpenStack.OpenStackNetworks.OpenStackSubnet import OpenStackSubnetcls
from neutronclient.v2_0 import client as NeutronClient
from keystoneclient.v2_0 import client as KeystoneClient

class OpenStackNetworkcls(OpenStackBaseCloudcls, BaseNetworkcls):
	
	__openstack_network = None
	__neutronclient = None

	def __init__(self, *arg, **kwargs):
                self.__openstack_network = arg[0]
		
                super(OpenStackNetworkcls, self).__init__(id=self.__openstack_network['id'], name= self.__openstack_network['name'], credentials=kwargs['credentials'])

        @property
        def state(self): return self.__openstack_network['status']

	@property
	def is_external_network(self): return self.__openstack_network['router:external']

	@property
        def __NeutronClient(self):
                return self.__neutronclient

        @__NeutronClient.getter
        def __NeutronClient(self):
                if self.__neutronclient is None:
                        from OpenStack.utils.OpenStackClients import OpenStackClientsCls
                        self.__neutronclient = OpenStackClientsCls().get_neutron_client(self._credentials)
                return self.__neutronclient

	def list_subnets(self):
		return [  OpenStackSubnetcls(openstack_subnet, credentials=self._credentials) for openstack_subnet in self.__NeutronClient.list_subnets(network_id=self.id)['subnets'] ]

        def get_subnet_by_id(self, subnet_id):
		return [  OpenStackSubnetcls(openstack_subnet, credentials=self._credentials) for openstack_subnet in self.__NeutronClient.list_subnets(id=subnet_id)['subnets'] ]

        def get_subnets_by_name(self, subnet_name):
		return [  OpenStackSubnetcls(openstack_subnet, credentials=self._credentials) for openstack_subnet in self.__NeutronClient.list_subnets(name=subnet_name)['subnets'] ]

        def get_subnets_by_tag(self, tag_name, tag_value):pass

        def create_subnet(self, name=None, cidr_block=None, enable_dhcp=False, dns_nameservers=None):
		if dns_nameservers is None:
			dns_nameservers = ['8.8.8.8']
		if cidr_block is None:
			cidr_block = '10.0.0.0/24'
		params = { 
				'subnet' : { 
						'network_id' : self.id, 
						'ip_version' : 4, 
						'enable_dhcp' : enable_dhcp,
						'dns_nameservers' : dns_nameservers,
						'name' : name, 
						'cidr' : cidr_block } }
		subnet_dict = self.__NeutronClient.create_subnet(params)
		openstack_subnet = subnet_dict['subnet']
		subnet = OpenStackSubnetcls(openstack_subnet, credentials=self._credentials)
		return subnet

