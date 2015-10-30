from BaseCloud.BaseNetworks.BaseNetworks import BaseNetworkscls 
from OpenStack.OpenStackNetworks.OpenStackNetwork import OpenStackNetworkcls
from OpenStack.OpenStackNetworks.OpenStackSubnet import OpenStackSubnetcls
from OpenStack.OpenStackNetworks.OpenStackNIC import OpenStackNICcls
from OpenStack.OpenStackNetworks.OpenStackFloatingIp import OpenStackFloatingIpcls
from OpenStack.OpenStackNetworks.OpenStackRouter import OpenStackRoutercls
from neutronclient.v2_0 import client as NeutronClient
from OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls
from keystoneclient.v2_0 import client as KeystoneClient

class OpenStackNetworkscls(OpenStackBaseCloudcls, BaseNetworkscls):
	__neutronclient = None

	def __init__(self, *args, **kwargs):
		self._credentials = kwargs

	@property
        def Childrens(self):
		return self.list_networks()

	def list_metrics(self):
		metrics = []
		from BaseCloud.BaseStats.BaseMetrics import BaseMetricscls
		metrics.append(BaseMetricscls('openstack.networks.count', len(self.list_networks())))
		metrics.append(BaseMetricscls('openstack.networks.subnets.count', len(self.list_subnets())))
		return metrics

 	@property
        def __NeutronClient(self):
                return self.__neutronclient

        @__NeutronClient.getter
        def __NeutronClient(self):
                if self.__neutronclient is None:
			from OpenStack.utils.OpenStackClients import OpenStackClientsCls
			self.__neutronclient = OpenStackClientsCls().get_neutron_client(self._credentials)
                return self.__neutronclient

        def get_network_by_id(self, network_id): 
		openstack_networks = self.list_networks()
		for openstack_network in openstack_networks:
			if openstack_network.id == network_id:
				return openstack_network

		return None
		
        def get_networks_by_name(self, network_name):
		networks = self.list_networks()
		nets = []
		for network in networks:
			if network.name == network_name:
				nets.append(network)
		return nets 

        def get_networks_by_tag(self, tag_name, tag_value): pass

	def list_networks(self):
		return [  OpenStackNetworkcls(openstack_network, credentials=self._credentials) for openstack_network in self.__NeutronClient.list_networks()['networks'] ]

	def list_external_networks(self):
		return [network for network in self.list_networks() if network.is_external_network]

        def create_network(self, name=None,cidr_block=None):
		params= { 'network': { 'name': name} }
		openstack_network_dic = self.__NeutronClient.create_network(params)
		openstack_network = openstack_network_dic['network']
		network = OpenStackNetworkcls(openstack_network, credentials=self._credentials)
		return network

	def list_subnets(self):
		return [ OpenStackSubnetcls(openstack_subnet, credentials=self._credentials) for openstack_subnet in self.__NeutronClient.list_subnets()['subnets']]
		
	def list_external_subnets(self):
		return [subnet for network  in self.list_external_networks() for subnet in network.list_subnets()]

        def get_subnet_by_id(self, subnet_id):
		subnets = self.list_subnets()
		for subnet in subnets:
			if subnet.id == subnet_id:
				return subnet
		return None
        def get_subnets_by_name(self, subnet_name):pass

        def get_subnets_by_tag(self, tag_name, tag_value):pass

	def list_nics(self):
		return [OpenStackNICcls(openstack_nic, credentials=self._credentials) for openstack_nic in self.__NeutronClient.list_ports()['ports']]

	def list_routers(self):
		return [ OpenStackRoutercls(router, credentials=self._credentials) for router in  self.__NeutronClient.list_routers()['routers']]

	def list_floating_ips(self):
		return [ OpenStackFloatingIpcls(openstack_floating_ip, credentials=self._credentials) for openstack_floating_ip in self.__NeutronClient.list_floatingips()['floatingips']]

	def count_total_floating_ips(self):
		count = 0
		for subnet in self.list_external_subnets():
			count += subnet.count_total_ips
		return count
