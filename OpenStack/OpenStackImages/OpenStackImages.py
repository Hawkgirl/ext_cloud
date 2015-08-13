from BaseCloud.BaseImages.BaseImages import BaseImagescls
from OpenStack.OpenStackImages.OpenStackImage import OpenStackImagecls
from glanceclient import client as GlanceClient
from keystoneclient.v2_0 import client as KeystoneClient
from OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls

class OpenStackImagescls(OpenStackBaseCloudcls, BaseImagescls):
        __glanceclient = None

        def __init__(self, *args, **kwargs):
		self._credentials = kwargs

        @property
        def __GlanceClient(self):
                return self.__glanceclient

        @__GlanceClient.getter
        def __GlanceClient(self):
                if self.__glanceclient is None:
			keystoneclient = KeystoneClient.Client(**self._credentials)
                        token = keystoneclient.auth_token
                        endpoint = keystoneclient.service_catalog.url_for(service_type='image',
                                                        endpoint_type='publicURL')
                        self.__glanceclient = GlanceClient.Client('1', endpoint=endpoint, token=token)

                return self.__glanceclient
	
	def list_images(self):
		openstack_images = self.__GlanceClient.images.list()
		images = [ ]
		for openstack_image in openstack_images:
			image = OpenStackImagecls(openstack_image, credentials=self._credentials)
			images.append(image)
		return images

        def create_image_from_instance(self):
                pass
