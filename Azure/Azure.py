from BaseCloud.BaseCloud import Cloudcls
from AzureCompute.AzureCompute import AzureComputecls
from AzureImages.AzureImages import AzureImagescls
from AzureBaseCloud import AzureBaseCloudcls


class Azurecls(AzureBaseCloudcls, Cloudcls):
    __identity = None
    __compute = None
    __networks = None
    __images = None
    __volumes = None
    __objectstore = None
    __templates = None
    __regions = None

    def __init__(self, *args, **kwargs):
        self._credentials['subscription_id'] = kwargs['subscription_id']
        self._credentials['certificate_path'] = kwargs['certificate_path']
        if 'region_name' not in kwargs:
            self._credentials['region_name'] = "East US"
        else:
            self._credentials['region_name'] = kwargs['region_name']

    @property
    def identity(self):
        pass

    @property
    def compute(self):
        if self.__compute is None:
            self.__compute = AzureComputecls(credentials=self._credentials)

        return self.__compute

    @property
    def networks(self):
        pass

    @property
    def images(self):
        if self.__images is None:
            self.__images = AzureImagescls(credentials=self._credentials)

        return self.__images

    @property
    def regions(self):
        from AzureRegions.AzureRegions import AzureRegionscls
        if self.__regions is None:
            self.__regions = AzureRegionscls(credentials=self._credentials)

        return self.__regions

    @property
    def volumes(self):
        if self.__volumes is None:
            from AzureVolumes.AzureVolumes import AzureVolumescls
            self.__volumes = AzureVolumescls(credentials=self._credentials)

        return self.__volumes

    @property
    def objectstore(self):
        pass

    @property
    def templates(self):
        pass

    def validate_credentials(self):
        pass
