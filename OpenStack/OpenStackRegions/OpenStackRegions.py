from BaseCloud.BaseRegions.BaseRegions import BaseRegionscls 
from OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls
from keystoneclient.v2_0 import client as KeystoneClient

class OpenStackRegionscls(OpenStackBaseCloudcls, BaseRegionscls):

	def __init__(self, *args, **kwargs):
		self._credentials = kwargs['credentials']
		self.__childrens = None

	@property
        def Childrens(self): return []

        def list_regions(self): 
			from OpenStack.OpenStackRegions.OpenStackRegion import OpenStackRegioncls
			keystoneclient = KeystoneClient.Client(**self._credentials)

			endpoints = keystoneclient.endpoints.list()
			regions = set()
			for endpoint in endpoints:
				if not endpoint.region in regions:
					regions.add(endpoint.region)

			openstack_regions = []
			for region in regions:
				region = OpenStackRegioncls(region, credentials=self._credentials)
				openstack_regions.append(region)

			return openstack_regions 

	def get_region_by_id(self, instance_id): pass

        def get_region_by_name(self, instance_name): pass

	def list_metrics(self):
		from BaseCloud.BaseStats.BaseMetrics import BaseMetricscls
                metrics = []
		regions = self.list_regions()
		metrics.append(BaseMetricscls('openstack.regions.count', len(regions)))
		zone_count = 0
		for region in regions:
			zone_count += len(region.list_zones())
		metrics.append(BaseMetricscls('openstack.regions.zones.count', zone_count))
		return metrics

