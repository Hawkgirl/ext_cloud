
class OpenStackClientsCls:

    def get_neutron_client(self, credentials=None):
        from keystoneclient.v2_0 import client as KeystoneClient
        from neutronclient.v2_0 import client as NeutronClient

        if 'region_name' not in credentials:
            credentials['region_name'] = None

        if 'token' in credentials:
            keystone = KeystoneClient.Client(auth_url=credentials['auth_url'], token=credentials['token'], tenant_name=credentials['tenant_name'], region_name=credentials['region_name'])
            endpoint = keystone.service_catalog.url_for(service_type='network', endpoint_type='publicURL')
            neutronclient = NeutronClient.Client(token=credentials['token'], endpoint_url=endpoint)
            return neutronclient

        neutronclient = NeutronClient.Client(username=credentials['username'], password=credentials['password'], tenant_name=credentials['tenant_name'], auth_url=credentials['auth_url'], region_name=credentials['region_name'], ca_cert=credentials['cacert'])

        return neutronclient

    def get_nova_client(self, credentials):
        from novaclient.client import Client as NovaClient

        if 'token' in credentials:
            novaclient = NovaClient('2', credentials['username'], credentials['token'], credentials['tenant_name'], credentials['auth_url'], 'compute', auth_token=credentials['token'], region_name=credentials['region_name'])

            return novaclient

        novaclient = NovaClient('2', credentials['username'], credentials['password'], credentials['tenant_name'], credentials['auth_url'], 'compute', region_name=credentials['region_name'])

        return novaclient

    def get_keystone_client(self, credentials):
        from keystoneclient.v2_0 import client as KeystoneClient
        return KeystoneClient.Client(**credentials)

    def get_cinder_client(self, credentials):
        from cinderclient import client as CinderClient
        return CinderClient.Client("2", credentials['username'], credentials['password'], credentials['tenant_name'], credentials['auth_url'], cacert=credentials['cacert'])

    def get_glance_client(self, credentials):
        from glanceclient import client as GlanceClient
        from keystoneclient.v2_0 import client as KeystoneClient
        keystoneclient = KeystoneClient.Client(**credentials)
	import pdb
	pdb.set_trace()
        token = keystoneclient.auth_token
        endpoint = keystoneclient.service_catalog.url_for(service_type='image', endpoint_type='publicURL')
        return GlanceClient.Client('2', endpoint=endpoint, token=token, cacert=credentials['cacert'])
