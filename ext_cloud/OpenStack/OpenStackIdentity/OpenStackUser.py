from ext_cloud.BaseCloud.BaseIdentity.BaseUser import BaseUsercls
from ext_cloud.OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls


class OpenStackUsercls(OpenStackBaseCloudcls, BaseUsercls):

    __openstack_user = None

    def __init__(self, *arg, **kwargs):
        self.__openstack_user = arg[0]
        super(OpenStackUsercls, self).__init__(id=self.__openstack_user.id, name=self.__openstack_user.name, credentials=kwargs['credentials'])

    @property
    def status(self):
        return 'enabled' if self.__openstack_user.enabled is True else 'disabled'

    @property
    def email_id(self):
        return self.__openstack_user.email if hasattr(self.__openstack_user, 'email') else None
 
    def list_metrics_all(self, dic):
        pass
