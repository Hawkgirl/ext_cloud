from ext_cloud.BaseCloud.BaseVolumes.BaseVolume import BaseVolumecls
from ext_cloud.OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls

class OpenStackVolumecls(OpenStackBaseCloudcls, BaseVolumecls):

        __openstack_volume = None

	def __init__(self, *arg, **kwargs):
                self.__openstack_volume = arg[0]

                super(OpenStackVolumecls, self).__init__(id=self.__openstack_volume.id, name=self.__openstack_volume.name, credentials=kwargs['credentials'])

        @property
        def status(self): return self.__openstack_volume.status

	@property
        def description(self): return self.__openstack_volume.description

	@property
        def size(self): return self.__openstack_volume.size
	
	@property
	def state(self): pass

	@property
	def user_id(self): return self.__openstack_volume.user_id
	
	@property
	def attached_to(self): return None if len(self.__openstack_volume.attachments) == 0 else self.__openstack_volume.attachments[0]['server_id']

	@property
	def is_attached(self): return False if self.attached_to is None else True
