from BaseCloud.BaseVolumes.BaseVolumes import BaseVolumescls
from OpenStack.OpenStackVolumes.OpenStackVolume import OpenStackVolumecls
from OpenStack.OpenStackVolumes.OpenStackSnapshot import OpenStackSnapshotcls
from cinderclient import client as CinderClient
from OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls

class OpenStackVolumescls(OpenStackBaseCloudcls, BaseVolumescls):
        __cinderclient = None

        def __init__(self, *args, **kwargs):
		self._credentials = kwargs

        @property
        def __CinderClient(self):
                return self._cinderclient

        @__CinderClient.getter
        def __CinderClient(self):
                if self.__cinderclient is None:
			self.__cinderclient = CinderClient.Client("1",self._credentials['username'], self._credentials['password'], self._credentials['tenant_name'], self._credentials['auth_url'])
                return self.__cinderclient

	def list_volumes(self):
		openstack_volumes = self.__CinderClient.volumes.list()
		volumes = []
		for openstack_volume in openstack_volumes:
			volume = OpenStackVolumecls(openstack_volume, credentials=self._credentials)
			volumes.append(volume)

		return volumes

        def create_volume(self, size=2, name = None): pass

        def attach_volume(self, volume_id=None, instance_id=None, device_path=None):pass

	def detach_volume(self, volume_id=None, instance_id=None): pass

	def list_snapshots(self):
		openstack_snapshots = self.__CinderClient.volume_snapshots.list()
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
