
class OpenStackClientsCls:

    _token = None
    _keystoneclient = None
    _novaclient = None
    _neutronclient = None
    _cinderclient = None
    _glanceclient = None

    def __init__(self, *arg, **kwargs):
        self._credentials=kwargs
	if 'region_name' not in self._credentials:
		self._credentials['region_name'] = None

    @property
    def token(self):
		return self._token
    @token.getter
    def token(self):
        if self._token is None:
        	from keystoneclient.v2_0 import client as KeystoneClient
	        self._keystoneclient = KeystoneClient.Client(**self._credentials)
		self._token = self._keystoneclient.auth_token
	return self._token

    @property
    def keystone(self):
        return self._keystoneclient

    @keystone.getter
    def keystone(self):
        if self._keystoneclient is None:
		from keystoneclient.v2_0 import client as KeystoneClient
                self._keystoneclient = KeystoneClient.Client(**self._credentials)
        return self._keystoneclient

    @property
    def neutron(self):
        return self._neutronclient

    @neutron.getter
    def neutron(self):
	if self._neutronclient is None:
        	from neutronclient.v2_0 import client as NeutronClient

            	endpoint = self.keystone.service_catalog.url_for(service_type='network', endpoint_type='publicURL')
            	self._neutronclient = NeutronClient.Client(token=self.token, endpoint_url=endpoint, ca_cert=self._credentials['cacert'])

        return self._neutronclient

    @property
    def nova(self):
        return self._novaclient

    @neutron.getter
    def nova(self):
	if self._novaclient is None:
        	from novaclient.client import Client as NovaClient

            	self._novaclient = NovaClient('2', self._credentials['username'], self.token, self._credentials['tenant_name'], self._credentials['auth_url'], 'compute', auth_token=self.token, region_name=self._credentials['region_name'])

        return self._novaclient


    @property
    def cinder(self):
        return self._cinderclient

    @cinder.getter
    def cinder(self):
	if self._cinderclient is None:
        	from cinderclient import client as CinderClient
        	self._cinderclient = CinderClient.Client("2", self._credentials['username'], self._credentials['password'], self._credentials['tenant_name'], self._credentials['auth_url'], cacert=self._credentials['cacert'])
	
	return self._cinderclient

    @property
    def glance(self):
        return self._glanceclient

    @glance.getter
    def glance(self):
	if self._glanceclient is None:
        	from glanceclient import client as GlanceClient
	        endpoint = self.keystone.service_catalog.url_for(service_type='image', endpoint_type='publicURL')
		self._glanceclient  = GlanceClient.Client('2', endpoint=endpoint, token=self.token, cacert=self._credentials['cacert'])

	return self._glanceclient
