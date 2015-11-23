from utils.OpenStackClients import OpenStackClientsCls
class OpenStackBaseCloudcls():
	_credentials = None
	
	_name = None
        _id = None

	_keystoneclient = None
	_novaclient = None
	_neutronclient = None
	_cinderclient = None
	_glanceclient = None

	def __init__(self, *arg, **kwargs):
                if kwargs.has_key('name'):
                        self._name = kwargs['name']
                if kwargs.has_key('id'):
                        self._id = kwargs['id']
                if kwargs.has_key('credentials'):
			import collections
                        self._credentials = collections.defaultdict(lambda:None, kwargs['credentials'])

	@property
        def name(self): return self._name

        @property
        def id(self): return self._id

	def __repr__(self):
                ret = ""
                for varible in dir(self):
                        if not varible.startswith("_") and isinstance(getattr(self.__class__, varible), property):
                                value = getattr(self, varible)
                                if value is None: value = "None"
                                if not isinstance(value, str): value = str(value)
                                ret = ret + varible +":" +  value + "  "
                return ret

	def list_metrics(self): return []


	@property
        def _KeystoneClient(self):
                return self._keystoneclient

        @_KeystoneClient.getter
        def _KeystoneClient(self):
                if self._keystoneclient is None:
                        self._keystoneclient = OpenStackClientsCls().get_keystone_client(self._credentials)
                return self._keystoneclient

	@property
        def _NovaClient(self):
                return self._novaclient

        @_NovaClient.getter
        def _NovaClient(self):
                if self._novaclient is None:
                        self._novaclient = OpenStackClientsCls().get_nova_client(self._credentials)
                return self._novaclient

	@property
        def _NeutronClient(self):
                return self._neutronclient

        @_NeutronClient.getter
        def _NeutronClient(self):
                if self._neutronclient is None:
                        self._neutronclient = OpenStackClientsCls().get_neutron_client(self._credentials)
                return self._neutronclient


	@property
        def _CinderClient(self):
                return self._cinderclient

        @_CinderClient.getter
        def _CinderClient(self):
                if self._cinderclient is None:
                        self._cinderclient = OpenStackClientsCls().get_cinder_client(self._credentials)
                return self._cinderclient

	@property
        def _GlanceClient(self):
                return self._glanceclient

        @_GlanceClient.getter
        def _GlanceClient(self):
                if self._glanceclient is None:
                       self._glanceclient = OpenStackClientsCls().get_glance_client(self._credentials)

                return self._glanceclient

