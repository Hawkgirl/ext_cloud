from BaseCloud.BaseNetworks.BaseNetworks import BaseNetworkscls 
from OpenStack.OpenStackNetworks.OpenStackNetwork import OpenStackNetworkcls
from OpenStack.OpenStackNetworks.OpenStackSubnet import OpenStackSubnetcls
from OpenStack.OpenStackNetworks.OpenStackNIC import OpenStackNICcls
from OpenStack.OpenStackNetworks.OpenStackRouter import OpenStackRoutercls
from neutronclient.v2_0 import client as NeutronClient
from OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls
from keystoneclient.v2_0 import client as KeystoneClient

class OpenStackNetworkscls(OpenStackBaseCloudcls, BaseNetworkscls):
	__neutronclient = None

	def __init__(self, *args, **kwargs):
		self._credentials = kwargs

 	@property
        def __NeutronClient(self):
                return self.__neutronclient

        @__NeutronClient.getter
        def __NeutronClient(self):
                if self.__neutronclient is None:
			if self._credentials.has_key('token'):
				keystone = KeystoneClient.Client(auth_url=self._credentials['auth_url'],token=self._credentials['token'], tenant_name=self._credentials['tenant_name'], region_name=self._credentials['region_name'])
				endpoint = keystone.service_catalog.url_for(service_type='network', endpoint_type='publicURL')
			 	self.__neutronclient = NeutronClient.Client(token=self._credentials['token'], endpoint_url = endpoint)
			else:
			 self.__neutronclient = NeutronClient.Client(username=self._credentials['username'], password=self._credentials['password'], tenant_name=self._credentials['tenant_name'], auth_url=self._credentials['auth_url'], region_name=self._credentials['region_name'])
                return self.__neutronclient

        def get_network_by_id(self, network_id): 
		openstack_networks = self.get_all_networks()
		for openstack_network in openstack_networks:
			if openstack_network.id == network_id:
				return openstack_network

		return None
		
        def get_networks_by_name(self, network_name):
		networks = self.get_all_networks()
		nets = []
		for network in networks:
			if network.name == network_name:
				nets.append(network)
		return nets 

        def get_networks_by_tag(self, tag_name, tag_value): pass

	def get_all_networks(self):
		openstack_networks_dic = self.__NeutronClient.list_networks()
		openstack_networks = openstack_networks_dic['networks']
		networks = []
		for openstack_network in openstack_networks:
			network = OpenStackNetworkcls(openstack_network, credentials=self._credentials)
			networks.append(network)

		return networks

        def create_network(self, name=None,cidr_block=None):
		params= { 'network': { 'name': name} }
		openstack_network_dic = self.__NeutronClient.create_network(params)
		openstack_network = openstack_network_dic['network']
		network = OpenStackNetworkcls(openstack_network, credentials=self._credentials)
		return network

	def get_all_subnets(self):
		subnet_dict = self.__NeutronClient.list_subnets()
		openstack_subnets = subnet_dict['subnets']
		subnets = []
		for openstack_subnet in openstack_subnets:
			subnet = OpenStackSubnetcls(openstack_subnet, credentials=self._credentials)
			subnets.append(subnet)
		return subnets
		

        def get_subnet_by_id(self, subnet_id):
		subnets = self.get_all_subnets()
		for subnet in subnets:
			if subnet.id == subnet_id:
				return subnet
		return None
        def get_subnets_by_name(self, subnet_name):pass

        def get_subnets_by_tag(self, tag_name, tag_value):pass

	def get_all_nics(self):
		nic_dict = self.__NeutronClient.list_ports()
		openstack_nics = nic_dict['ports']
		nics = []
		for openstack_nic in openstack_nics:
			nic = OpenStackNICcls(openstack_nic, credentials=self._credentials)
			nics.append(nic)

		return nics

	def get_all_routers(self):
		router_dict  = self.__NeutronClient.list_routers()
		openstack_routers = router_dict['routers']
		routers = []
		for router in openstack_routers:
			router = OpenStackRoutercls(router, credentials=self._credentials)
			routers.append(router)
	
		return routers
