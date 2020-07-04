from ext_cloud.BaseCloud.BaseVolumes.BaseVolumes import BaseVolumescls
from ext_cloud.OpenStack.OpenStackVolumes.OpenStackVolume import OpenStackVolumecls, STATE_MAP
from ext_cloud.OpenStack.OpenStackVolumes.OpenStackSnapshot import OpenStackSnapshotcls
from ext_cloud.OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls
from functools import reduce


class OpenStackVolumescls(OpenStackBaseCloudcls, BaseVolumescls):

    def __init__(self, **kwargs):
        super(OpenStackVolumescls, self).__init__(credentials=kwargs)

    @property
    def Childrens(self):
        return self.list_volumes() + self.list_snapshots()

    def list_metrics_all(self, dic):
        from toolz import countby

        volumes = self.list_volumes()
        dic['openstack.volumes.count'] = len(volumes)

        group_by_state = countby(lambda x: x.status, volumes)
        dic['openstack.volumes.count_used_volumes'] =  group_by_state['in-use'] if 'in-use' in group_by_state else 0
        dic['openstack.volumes.count_free_volumes'] =  group_by_state['available'] if 'available' in group_by_state else 0
        dic['openstack.volumes.count_error_volumes'] =  group_by_state['error'] if 'error' in group_by_state else 0
        dic['openstack.volumes.count_creating'] =  group_by_state['creating'] if 'creating' in group_by_state else 0
        dic['openstack.volumes.count_error_deleting'] =  group_by_state['error_deleting'] if 'error_deleting' in group_by_state else 0


    def list_zombie_resources(self):
        zombies = []
        for child in self.Childrens:
            if child.is_zombie:
                zombies.append(child)

        return zombies

    def list_volumes(self):
        search_opts = {'all_tenants': 1}
        openstack_volumes = self._Clients.cinder.volumes.list(search_opts=search_opts)
        volumes = []
        for openstack_volume in openstack_volumes:
            volume = OpenStackVolumecls(openstack_volume, credentials=self._credentials)
            volumes.append(volume)

        return volumes

    def get_volumes_by_error_state(self):
        from ext_cloud.BaseCloud.BaseVolumes.BaseVolume import STATE
        return self.get_volumes_by_state(STATE.ERROR)

    def get_volumes_by_state(self, state):
        state_str = 'READY'
        for key in STATE_MAP:
            if state == STATE_MAP[key]:
                state_str = key
                break

        search_opts = {'all_tenants': 1, 'status': state_str}
        openstack_volumes = self._Clients.cinder.volumes.list(
            search_opts=search_opts)
        volumes = []
        for openstack_volume in openstack_volumes:
            volume = OpenStackVolumecls(openstack_volume, credentials=self._credentials)
            volumes.append(volume)

        return volumes

    def create_volume(self, size=2, name=None):
        pass

    def attach_volume(self, volume_id=None, instance_id=None, device_path=None):
        pass

    def detach_volume(self, volume_id=None, instance_id=None):
        pass

    def list_snapshots(self):
        search_opts = {'all_tenants': 1}
        openstack_snapshots = self._Clients.cinder.volume_snapshots.list(search_opts=search_opts)
        snapshots = []
        for openstack_snapshot in openstack_snapshots:
            snapshot = OpenStackSnapshotcls(openstack_snapshot, credentials=self._credentials)
            snapshots.append(snapshot)

        return snapshots

    def delete_volume_by_id(self, volume_id):
        pass

    def create_snapshot(self, volume_id, name=None, description=None):
        pass

    def get_volumes_by_tag(self, tag_name, tag_value):
        pass

    def delete_snapshot_by_id(self, snapshot_id):
        pass
