from BaseCloud.BaseCloud import Cloudcls
from OpenStackBaseCloud import OpenStackBaseCloudcls

class OpenStackcls(OpenStackBaseCloudcls, Cloudcls):
	__identity = None
	__compute = None
	__networks = None
	__images = None
	__volumes = None
	__objectstore = None
	__templates = None

	def __init__(self,*args,**kwargs): 
		self._credentials = kwargs
	
	@property
	def identity(self): pass

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

        def validate_credentials(self): 
		self.networks.list_networks()
		return True
