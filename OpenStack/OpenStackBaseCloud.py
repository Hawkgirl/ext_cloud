
#TODO derive it from BaseCloud
class OpenStackBaseCloudcls:
	_credentials = { }
	
	_name = None
        _id = None


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

	def list_metrics(self):
                metrics = []
                for child in self.Childrens:
                        metrics += child.list_metrics()
                return metrics

