from ext_cloud.BaseCloud.BaseVolumes.BaseVolumes import BaseVolumescls
from ext_cloud.OpenStack.OpenStackVolumes.OpenStackVolume import OpenStackVolumecls
from ext_cloud.OpenStack.OpenStackVolumes.OpenStackSnapshot import OpenStackSnapshotcls
from ext_cloud.OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls

class OpenStackVolumescls(OpenStackBaseCloudcls, BaseVolumescls):

        def __init__(self, *args, **kwargs):
		super(OpenStackVolumescls, self).__init__(credentials = kwargs)

	def list_metrics(self):
		metrics = []
		from ext_cloud.BaseCloud.BaseStats.BaseMetrics import BaseMetricscls
		metrics.append(BaseMetricscls('openstack.volumes.count', self.count_total_volumes))
		metrics.append(BaseMetricscls('openstack.volumes.count_error_volumes', self.count_error_volumes))
		metrics.append(BaseMetricscls('openstack.volumes.count_used_volumes', self.count_used_volumes))
		metrics.append(BaseMetricscls('openstack.volumes.count_free_volumes', self.count_free_volumes))
	
		return metrics

	@property
	def count_total_volumes(self): return len(self.list_volumes())

	@property
	def count_used_volumes(self): return reduce(lambda x,y: x+1 if y.is_attached else x , self.list_volumes(),0)

	@property
	def count_free_volumes(self): 
		return reduce(lambda x,y: x+1 if (not y.is_attached) and (y.status == 'available') else x , self.list_volumes(),0)

	@property
	def count_error_volumes(self): return reduce(lambda x,y: x+1 if y.status == 'error' else x , self.list_volumes(),0)

	def list_volumes(self):
		search_opts = {'all_tenants': 1}
		openstack_volumes = self._CinderClient.volumes.list( search_opts = search_opts)
		volumes = []
		for openstack_volume in openstack_volumes:
			volume = OpenStackVolumecls(openstack_volume, credentials=self._credentials)
			volumes.append(volume)

		return volumes

        def create_volume(self, size=2, name = None): pass

        def attach_volume(self, volume_id=None, instance_id=None, device_path=None):pass

	def detach_volume(self, volume_id=None, instance_id=None): pass

	def list_snapshots(self):
		openstack_snapshots = self._CinderClient.volume_snapshots.list()
		snapshots = []
		for openstack_snapshot in openstack_snapshots:
			snapshot = OpenStackSnapshotcls(openstack_snapshot, credentials=self._credentials)
			snapshots.append(snapshot)

		return snapshots

        def create_volume(self, size=2, name = None): 
                pass

        def delete_volume_by_id(self, volume_id): 
		pass

        def create_snapshot(self, volume_id, name=None, description=None): 
                pass

	def get_volumes_by_tag(self, tag_name, tag_value): 
                pass

	def delete_snapshot_by_id(self, snapshot_id): 
		pass
