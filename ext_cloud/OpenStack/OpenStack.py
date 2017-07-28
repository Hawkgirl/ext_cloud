from ext_cloud.BaseCloud.BaseCloud import BaseCloudcls
from OpenStackBaseCloud import OpenStackBaseCloudcls


class OpenStackcls(OpenStackBaseCloudcls, BaseCloudcls):
    __identity = None
    __compute = None
    __networks = None
    __images = None
    __volumes = None
    __objectstore = None
    __templates = None
    __resources = None
    __childrens = None
    __services = None
    __regions = None

    def __init__(self, *args, **kwargs):
        if 'username' in kwargs:
            self._credentials = kwargs
            return None
        import os
        # load credentials from environment varible
        if os.environ.get('OS_USERNAME') is not None:
            dic = {}
            dic['username'] = os.environ.get('OS_USERNAME')
            dic['password'] = os.environ.get('OS_PASSWORD')
            dic['tenant_name'] = os.environ.get('OS_TENANT_NAME')
            dic['auth_url'] = os.environ.get('OS_AUTH_URL')
            dic['cacert'] = os.environ.get('OS_CACERT')
            self._credentials = dic

            return None
        # load credentials from config file
        if os.path.exists('/etc/ext_cloud/ext_cloud.conf'):
            from utils.ConfFileParser import config_file_dic
            dic = config_file_dic()
            self._credentials = dic

            return None
        else:
            raise Exception("Credentails not exported in environment varibles and /etc/ext_cloud/ext_cloud.conf file")

    @property
    def identity(self):
        if self.__identity is None:
            from OpenStackIdentity.OpenStackIdentity import OpenStackIdentitycls
            self.__identity = OpenStackIdentitycls(**self._credentials)

        return self.__identity

    @property
    def compute(self):
        if self.__compute is None:
            from OpenStackCompute.OpenStackCompute import OpenStackComputecls
            self.__compute = OpenStackComputecls(**self._credentials)

        return self.__compute

    @property
    def networks(self):
        if self.__networks is None:
            from OpenStackNetworks.OpenStackNetworks import OpenStackNetworkscls
            self.__networks = OpenStackNetworkscls(**self._credentials)

        return self.__networks

    @property
    def images(self):
        if self.__images is None:
            from OpenStackImages.OpenStackImages import OpenStackImagescls
            self.__images = OpenStackImagescls(**self._credentials)

        return self.__images

    @property
    def volumes(self):
        if self.__volumes is None:
            from OpenStackVolumes.OpenStackVolumes import OpenStackVolumescls
            self.__volumes = OpenStackVolumescls(**self._credentials)

        return self.__volumes

    @property
    def templates(self):
        if self.__templates is None:
            from OpenStackTemplates.OpenStackTemplates import OpenStackTemplatescls
            self.__templates = OpenStackTemplatescls(**self._credentials)

        return self.__templates

    @property
    def objectstore(self):
        if self.__objectstore is None:
            from OpenStackObjectStore.OpenStackObjectStore import OpenStackObjectStorecls
            self.__objectstore = OpenStackObjectStorecls(**self._credentials)

        return self.__objectstore

    @property
    def resources(self):
        if self.__resources is None:
            from OpenStackResources.OpenStackResources import OpenStackResourcescls
            self.__resources = OpenStackResourcescls(**self._credentials)

        return self.__resources

    @property
    def regions(self):
        if self.__regions is None:
            from OpenStackRegions.OpenStackRegions import OpenStackRegionscls
            self.__regions = OpenStackRegionscls(credentials=self._credentials)

        return self.__regions

    @property
    def services(self):
        if self.__services is None:
            from OpenStackServices.OpenStackServices import OpenStackServicescls
            self.__services = OpenStackServicescls(**self._credentials)

        return self.__services

    @property
    def Childrens(self):
        if self.__childrens is None:
            self.__childrens = [self.identity, self.compute, self.networks,
                                self.services, self.regions, self.volumes, self.images]

        return self.__childrens

    def validate_credentials(self):
        self.networks.list_networks()
        return True