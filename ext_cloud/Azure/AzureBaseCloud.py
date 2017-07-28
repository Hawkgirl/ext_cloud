class AzureBaseCloudcls:
    _credentials = {}

    _name = None
    _id = None
    _azure_ref = None

    def __init__(self, *arg, **kwargs):
        if 'name' in kwargs:
            self._name = kwargs['name']
        if 'id' in kwargs:
            self._id = kwargs['id']
        if 'credentials' in kwargs:
            self._credentials = kwargs['credentials']

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    def __repr__(self):
        ret = ""
        for varible in dir(self):
            if not varible.startswith("_") and isinstance(getattr(self.__class__, varible), property):
                value = getattr(self, varible)
                if value is None:
                    value = "None"
                if not isinstance(value, str):
                    value = str(value)
                ret = ret + varible + ":" + value + "  "
        return ret