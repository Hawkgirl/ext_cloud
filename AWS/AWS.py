from BaseCloud.BaseCloud import Cloudcls
from boto import ec2
from AWSCompute.AWSCompute import AWSComputecls
from AWSImages.AWSImages import AWSImagescls
from AWSNetworks.AWSNetworks import AWSNetworkscls
from AWSVolumes.AWSVolumes import AWSVolumescls
from AWSObjectStore.AWSObjectStore import AWSObjectStorecls
from AWSTemplates.AWSTemplates import AWSTemplatescls
from AWSBaseCloud import AWSBaseCloudcls


class AWScls(AWSBaseCloudcls, Cloudcls):
    __identity = None
    __compute = None
    __networks = None
    __images = None
    __volumes = None
    __objectstore = None
    __templates = None
    __regions = None

    def __init__(self, *args, **kwargs):
        self._credentials['username'] = kwargs['username']
        self._credentials['password'] = kwargs['password']
        self._credentials['region_name'] = kwargs['region_name']

    @property
    def identity(self): pass

    @property
    def compute(self):
        if self.__compute is None:
            self.__compute = AWSComputecls(username=self._credentials['username'], password=self._credentials[
                                           'password'], region_name=self._credentials['region_name'])

        return self.__compute

    @property
    def networks(self):
        if self.__networks is None:
            self.__networks = AWSNetworkscls(username=self._credentials['username'], password=self._credentials[
                                             'password'], region_name=self._credentials['region_name'])

        return self.__networks

    @property
    def images(self):
        if self.__images is None:
            self.__images = AWSImagescls(username=self._credentials['username'], password=self._credentials[
                                         'password'], region_name=self._credentials['region_name'])

        return self.__images

    @property
    def regions(self):
        if self.__regions is None:
            from AWSRegions.AWSRegions import AWSRegionscls
            self.__regions = AWSRegionscls(credentials=self._credentials)

        return self.__regions

    @property
    def volumes(self):
        if self.__volumes is None:
            self.__volumes = AWSVolumescls(username=self._credentials['username'], password=self._credentials[
                                           'password'], region_name=self._credentials['region_name'])

        return self.__volumes

    @property
    def objectstore(self):
        if self.__objectstore is None:
            self.__objectstore = AWSObjectStorecls(username=self._credentials['username'], password=self._credentials[
                                                   'password'], region_name=self._credentials['region_name'])

        return self.__objectstore

    @property
    def templates(self):
        if self.__templates is None:
            self.__templates = AWSTemplatescls(username=self._credentials['username'], password=self._credentials[
                                               'password'], region_name=self._credentials['region_name'])

        return self.__templates

    def validate_credentials(self):
        self.networks.list_networks()
        return True
