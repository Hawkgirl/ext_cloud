from ext_cloud.BaseCloud.BaseIdentity.BaseProject import BaseProjectcls
from ext_cloud.OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls


class OpenStackProjectcls(OpenStackBaseCloudcls, BaseProjectcls):

    __openstack_project = None

    def __init__(self, *arg, **kwargs):
        self.__openstack_project = arg[0]
        super(OpenStackProjectcls, self).__init__(id=self.__openstack_project.id,
                                                 name=self.__openstack_project.name, credentials=kwargs['credentials'])

    @property
    def status(self):
        return 'enabled' if self.__openstack_project.enabled is True else 'disabled'

    @property
    def usage(self):


        from ext_cloud.OpenStack.utils.ConfFileParser import is_novausage_enabled
        if( is_novausage_enabled() == False ):
            return None

        from ext_cloud.BaseCloud.BaseResources.BaseResourceUsage import BaseResourceUsagecls
        import datetime
        now = datetime.datetime.now()
        epoch = datetime.datetime(year=1970, month=1, day=1)
        project_usage = self._Clients.nova.usage.get(self.oid, epoch, now)

        if not hasattr(project_usage, 'total_vcpus_usage'):
            return None
        usage_dict = {}
        usage_dict['hours_cpu'] = project_usage.total_vcpus_usage
        usage_dict['hours_disk'] = project_usage.total_local_gb_usage
        usage_dict['hours_memory'] = project_usage.total_memory_mb_usage

        deleted_vms = used_vms = 0
        for vm in project_usage.server_usages:
            if vm['state'] == 'terminated':
                deleted_vms += 1
            else:
                used_vms += 1
        usage_dict['deleted_vms'] = deleted_vms
        usage_dict['used_vms'] = used_vms

        return BaseResourceUsagecls(**usage_dict)

    def list_metrics_all(self, dic):
        pass
