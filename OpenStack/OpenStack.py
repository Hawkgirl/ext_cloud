from BaseCloud.BaseCloud import Cloudcls
from boto import ec2
from OpenStackCompute.OpenStackCompute import OpenStackComputecls
from OpenStackImages.OpenStackImages import OpenStackImagescls
from OpenStackNetworks.OpenStackNetworks import OpenStackNetworkscls
from OpenStackVolumes.OpenStackVolumes import OpenStackVolumescls
from OpenStackTemplates.OpenStackTemplates import OpenStackTemplatescls
from OpenStackObjectStore.OpenStackObjectStore import OpenStackObjectStorecls
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
			self.__compute = OpenStackComputecls(**self._credentials)

		return self.__compute

	@property
	def networks(self): 
		if self.__networks is None:
			self.__networks = OpenStackNetworkscls(**self._credentials)

		return self.__networks

	@property
	def images(self):
		if self.__images is None:
			self.__images = OpenStackImagescls(**self._credentials)

		return self.__images

	@property
	def volumes(self): 
		if self.__volumes is None:
                        self.__volumes = OpenStackVolumescls(**self._credentials)

                return self.__volumes

	@property
	def templates(self): 
		if self.__templates is None:
                        self.__templates = OpenStackTemplatescls(**self._credentials)

                return self.__templates


	@property
	def objectstore(self): 
		if self.__objectstore is None:
                        self.__objectstore = OpenStackObjectStorecls(**self._credentials)

                return self.__objectstore

        def validate_credentials(self): 
		self.networks.list_networks()
		return True
