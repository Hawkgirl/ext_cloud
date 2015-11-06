from utils.OpenStackClients import OpenStackClientsCls
class OpenStackBaseCloudcls():
	_credentials = { }
	
	_name = None
        _id = None

	_novaclient = None
	_neutronclient = None

	def __init__(self, *arg, **kwargs):
                if kwargs.has_key('name'):
                        self._name = kwargs['name']
                if kwargs.has_key('id'):
                        self._id = kwargs['id']
                if kwargs.has_key('credentials'):
                        self._credentials = kwargs['credentials']

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

