from ext_cloud.BaseCloud.BaseCompute.BaseHypervisor import BaseHypervisorcls
from ext_cloud.OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls


class OpenStackHypervisorcls(OpenStackBaseCloudcls, BaseHypervisorcls):

    __openstack_hypervisor = None

    def __init__(self, *arg, **kwargs):
        self.__openstack_hypervisor = arg[0]
        super(OpenStackHypervisorcls, self).__init__(id=self.__openstack_hypervisor.id,
                                                     name=self.__openstack_hypervisor.hypervisor_hostname, credentials=kwargs['credentials'])

    @property
    def state(self):
        return self.__openstack_hypervisor.state

    @property
    def status(self):
        return self.__openstack_hypervisor.status

    @property
    def arch(self):
        cpu_arch = None
        try:
            import ast
            cpu_dict = ast.literal_eval(self.__openstack_hypervisor.cpu_info)
            cpu_arch = cpu_dict['arch']
        except BaseException:
            pass
        return cpu_arch

    @property
    def host_name(self):
        return self.__openstack_hypervisor.hypervisor_hostname

    @property
    def short_host_name(self):
        return self.host_name.split('.', 1)[0]

    @property
    def cpus(self):
        from ext_cloud.OpenStack.utils.ConfFileParser import config_file_dic
        dic = config_file_dic()
        # load cpu multiplication factor from ext_cloud.config file
        # default is 16
        if dic is None:
           return self.__openstack_hypervisor.vcpus * 16

        if 'cpu_allocation_ratio' in dic:
            return self.__openstack_hypervisor.vcpus * int(dic['cpu_allocation_ratio'])
        else:
            return self.__openstack_hypervisor.vcpus * 16

    @property
    def hypervisor_type(self):
        return self.__openstack_hypervisor.hypervisor_type

    @property
    def vcpus_used(self):
        return self.__openstack_hypervisor.vcpus_used

    @property
    def vpcus_used_percentage(self):
        return round((self.vcpus_used / float(self.cpus) * 100), 2)

    @property
    def disk_gb(self):
        return self.__openstack_hypervisor.local_gb

    @property
    def disk_used_gb(self):
        return self.__openstack_hypervisor.local_gb_used

    @property
    def free_disk_gb(self):
        return self.__openstack_hypervisor.free_disk_gb

    @property
    def memory_mb(self):
        from ext_cloud.OpenStack.utils.ConfFileParser import config_file_dic
        dic = config_file_dic()
        # load memory multiplication factor from ext_cloud.config file
        # default is 1.5
        if dic is None:
            return self.__openstack_hypervisor.memory_mb * 1.5
        if 'ram_allocation_ratio' in dic:
            return self.__openstack_hypervisor.memory_mb * int(dic['ram_allocation_ratio'])
        else:
            return self.__openstack_hypervisor.memory_mb * 1.5

    @property
    def memory_mb_api(self):
        return self.__openstack_hypervisor.memory_mb

    @property
    def proc_units(self):
       return self.__openstack_hypervisor.proc_units

    @property
    def proc_units_reserved(self):
       return self.__openstack_hypervisor.proc_units_reserved

    @property
    def proc_units_used(self):
       return self.__openstack_hypervisor.proc_units_used

    @property
    def memory_used_mb(self):
        return self.__openstack_hypervisor.memory_mb_used

    @property
    def memory_free_mb(self):
        return self.__openstack_hypervisor.free_ram_mb

    @property
    def memory_used_percentage(self):
        return round((self.memory_used_mb / float(self.memory_mb) * 100), 2)

    @property
    def running_vms(self):
        return self.__openstack_hypervisor.running_vms

    @property
    def host_ip(self):
        return self.__openstack_hypervisor.host_ip

    def list_metrics_all(self, dic):
        if self.hypervisor_type == 'ironic':
            # Baremetal node.need to return other metrics
            return 

        metric_property = ('proc_units', 'proc_units_used', 'disk_gb', 'disk_used_gb', 'free_disk_gb',
                           'memory_mb', 'memory_used_mb', 'memory_free_mb' )

        metric_str = 'openstack.compute.' + self.short_host_name + '.'
        for metric in metric_property:
            full_metric_str = metric_str + metric
            dic[full_metric_str] =  getattr(self, metric)
  
        # percentage metric
        dic[metric_str + 'cpus_used_percentage'] = round(((float(self.proc_units_used)+float(self.proc_units_reserved))/float(self.proc_units)*100), 1)
        dic[metric_str + 'memory_used_percentage'] = round(((float(self.memory_used_mb))/float(self.memory_mb_api)*100), 1)
        dic[metric_str + 'disk_used_percentage'] =  round(((float(self.disk_used_gb))/float(self.disk_gb)*100), 1)
        # state metric
        full_metric_str = metric_str + 'statedown'
        value = 1 if self.state == 'down' else 0
        dic[full_metric_str] = value
        # status
        full_metric_str = metric_str + 'statusdisabled'
        value = 1 if self.status == 'disabled' else 0
        dic[full_metric_str] = value
        # arch metric
        if self.arch is not None:
            full_metric_str = metric_str + 'arch.' + self.arch
            dic[full_metric_str] =  1

        if self.hypervisor_type is not None:
            full_metric_str = metric_str + 'type.' + self.hypervisor_type
            dic[full_metric_str] =  1

