
class OpenStackClientsCls:
	def get_neutron_client(self, credentials=None): 
		from keystoneclient.v2_0 import client as KeystoneClient
		from neutronclient.v2_0 import client as NeutronClient

		if not credentials.has_key('region_name'):
				credentials['region_name'] = None

                if credentials.has_key('token'):
                                keystone = KeystoneClient.Client(auth_url=credentials['auth_url'],token=credentials['token'], tenant_name=credentials['tenant_name'], region_name=credentials['region_name'])
                                endpoint = keystone.service_catalog.url_for(service_type='network', endpoint_type='publicURL')
                                neutronclient = NeutronClient.Client(token=credentials['token'], endpoint_url = endpoint)
				return neutronclient

		neutronclient = NeutronClient.Client(username=credentials['username'], password=credentials['password'], tenant_name=credentials['tenant_name'], auth_url=credentials['auth_url'], region_name = credentials['region_name'])

                return neutronclient

	def get_nova_client(self, credentials):
		from novaclient.client import Client as NovaClient

		if credentials.has_key('token'):
                                novaclient = NovaClient('2', credentials['username'], credentials['token'], credentials['tenant_name'], credentials['auth_url'], 'compute', auth_token=credentials['token'], region_name=credentials['region_name'])

				return novaclient

		if not credentials.has_key('region_name'):
				credentials['region_name'] = None
		novaclient = NovaClient('2', credentials['username'], credentials['password'], credentials['tenant_name'], credentials['auth_url'], 'compute', region_name=credentials['region_name'])


                return novaclient

	def get_keystone_client(self, credentails):
		from keystoneclient.v2_0 import client as KeystoneClient
		return KeystoneClient.Client(**credentials)
