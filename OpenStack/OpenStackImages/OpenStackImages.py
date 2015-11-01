from BaseCloud.BaseImages.BaseImages import BaseImagescls
from OpenStack.OpenStackImages.OpenStackImage import OpenStackImagecls
from OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls

class OpenStackImagescls(OpenStackBaseCloudcls, BaseImagescls):
        __glanceclient = None

        def __init__(self, *args, **kwargs):
		self._credentials = kwargs

	def list_metrics(self):
		metrics = []
		from BaseCloud.BaseStats.BaseMetrics import BaseMetricscls
		images = self.list_images()
		arch_dict = {}
		for image in images:
			if image.arch is not None:
				if arch_dict.has_key(image.arch): 
					arch_dict[image.arch] += 1
				else: arch_dict[image.arch] = 1

		metrics.append(BaseMetricscls('openstack.images.count', len(self.list_images())))
		for key in arch_dict:
			metrics.append(BaseMetricscls('openstack.images.'+ key, arch_dict[key]))
		
		return metrics	
		
        @property
        def __GlanceClient(self):
                return self.__glanceclient

        @__GlanceClient.getter
        def __GlanceClient(self):
                if self.__glanceclient is None:
			from OpenStack.utils.OpenStackClients import OpenStackClientsCls
                        self.__glanceclient = OpenStackClientsCls().get_glance_client(self._credentials)

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
