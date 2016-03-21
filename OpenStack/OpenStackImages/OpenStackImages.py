from ext_cloud.BaseCloud.BaseImages.BaseImages import BaseImagescls
from ext_cloud.OpenStack.OpenStackImages.OpenStackImage import OpenStackImagecls
from ext_cloud.OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls


class OpenStackImagescls(OpenStackBaseCloudcls, BaseImagescls):
    def __init__(self, *args, **kwargs):
        super(OpenStackImagescls, self).__init__(credentials=kwargs)

    def list_metrics(self):
        metrics = []
        from ext_cloud.BaseCloud.BaseResources.BaseMetrics import BaseMetricscls
        images = self.list_images()
        arch_dict = {}
        for image in images:
            if image.arch is not None:
                if arch_dict.has_key(image.arch):
                    arch_dict[image.arch] += 1
                else:
                    arch_dict[image.arch] = 1

        metrics.append(BaseMetricscls('openstack.images.count', len(
            self.list_images())))
        for key in arch_dict:
            metrics.append(BaseMetricscls('openstack.images.' + key, arch_dict[
                key]))

        return metrics

    def list_images(self):
        openstack_images = self._GlanceClient.images.list()
        images = []
        for openstack_image in openstack_images:
            image = OpenStackImagecls(openstack_image,
                                      credentials=self._credentials)
            images.append(image)
        return images

    def create_image_from_instance(self):
        pass
