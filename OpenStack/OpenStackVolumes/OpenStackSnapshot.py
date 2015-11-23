from ext_cloud.BaseCloud.BaseVolumes.BaseSnapshot import BaseSnapshotcls
from ext_cloud.OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls

class OpenStackSnapshotcls(OpenStackBaseCloudcls, BaseSnapshotcls):

        __openstack_snapshot = None

	def __init__(self, *arg, **kwargs):
                self.__openstack_snapshot = arg[0]
		#TODO
		name = None

                super(AWSInstancecls, self).__init__(id=self.__openstack_snapshot.id, name=name, credentials=kwargs['credentials'])
        @property
        def size(self): pass 

        @property
        def state(self): return self.__openstack_snapshot.status
