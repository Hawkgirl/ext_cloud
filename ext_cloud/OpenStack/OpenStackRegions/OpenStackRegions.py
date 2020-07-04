from ext_cloud.BaseCloud.BaseRegions.BaseRegions import BaseRegionscls
from ext_cloud.OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls


class OpenStackRegionscls(OpenStackBaseCloudcls, BaseRegionscls):

    def __init__(self, **kwargs):
        self._credentials = kwargs['credentials']
        self.__childrens = None
        super(OpenStackRegionscls, self).__init__(credentials=kwargs['credentials'])

    @property
    def Childrens(self):
        return []

    def list_regions(self):
        from ext_cloud.OpenStack.OpenStackRegions.OpenStackRegion import OpenStackRegioncls

        endpoints = self._Clients.keystone.endpoints.list()
        regions = set()
        for endpoint in endpoints:
            if endpoint.region not in regions:
                regions.add(endpoint.region)

        openstack_regions = []
        for region in regions:
            region = OpenStackRegioncls(region, credentials=self._credentials)
            openstack_regions.append(region)

        return openstack_regions

    def get_region_by_id(self, instance_id):
        pass

    def get_region_by_name(self, instance_name):
        pass

        
    def list_metrics_all(self, dic):
        from ext_cloud.BaseCloud.BaseResources.BaseMetrics import BaseMetricscls
        regions = self.list_regions()
        dic['openstack.regions.count'] =  len(regions)
        for region in regions:
            region.list_metrics_all(dic)
