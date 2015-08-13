from BaseCloud.BaseNetworks.BaseSubnet import BaseSubnetcls
from neutronclient.v2_0 import client as NeutronClient
from OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls
from OpenStack.OpenStackNetworks.OpenStackNIC import OpenStackNICcls
from keystoneclient.v2_0 import client as KeystoneClient

class OpenStackSubnetcls(OpenStackBaseCloudcls, BaseSubnetcls):
	
	__openstack_subnet = None
	__neutronclient = None

	def __init__(self, *arg, **kwargs):
                self.__openstack_subnet = arg[0]

                super(OpenStackSubnetcls, self).__init__(id=self.__openstack_subnet['id'], name=self.__openstack_subnet['name'], credentials=kwargs['credentials'])


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
                        	self.__neutronclient = NeutronClient.Client(username=self._credentials['username'], password=self._credentials['password'], tenant_name=self._credentials['tenant_name'], auth_url=self._credentials['auth_url'], region_name = self._credentials['region_name'])
                return self.__neutronclient
        @property
        def state(self): pass

	@property
	def cidr_block(self): return self.__openstack_subnet['cidr']

	@property
	def network_id(self): return self.__openstack_subnet['network_id']

	@property
	def zone(self): pass 

	
	def attach_nic(self, name=None, ip_address=None):
		if ip_address is None:
			fixed_ips = [{'subnet_id': self.id }]
		else:
			fixed_ips = [{ 'ip_address': ip_address, 'subnet_id': self.id }]
                params = {'port' : {
                                        'name': name,
                                        'network_id': self.network_id,
                                        'fixed_ips': fixed_ips
                                    }
                        }

                nic_dict = self.__NeutronClient.create_port(params)
                openstack_nic = nic_dict['port']
                nic = OpenStackNICcls(openstack_nic, credentials=self._credentials)
                return nic

