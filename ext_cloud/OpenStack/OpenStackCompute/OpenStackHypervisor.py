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
       return float(self.__openstack_hypervisor.proc_units)

    @property
    def proc_units_reserved(self):
       return float(self.__openstack_hypervisor.proc_units_reserved)

    @property
    def proc_units_used(self):
       return float(self.__openstack_hypervisor.proc_units_used)

    @property
    def memory_used_mb(self):
        return int(self.__openstack_hypervisor.memory_mb_used)

    @property
    def memory_free_mb(self):
        return int(self.__openstack_hypervisor.free_ram_mb)

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

        toplevel_str = 'openstack.toplevel.computes.'
        metric_str = 'openstack.compute.' + self.short_host_name + '.'

        dic[metric_str+'proc_units'] = self.proc_units
        if toplevel_str+'sum_proc_units' in dic:
            dic[toplevel_str+'sum_proc_units'] += self.proc_units
        else:
            dic[toplevel_str+'sum_proc_units']  = self.proc_units


        dic[metric_str+'proc_units_used'] = self.proc_units_used
        if toplevel_str+'sum_proc_units_used' in dic:
            dic[toplevel_str+'sum_proc_units_used'] += round(self.proc_units_used,1)
        else:
            dic[toplevel_str+'sum_proc_units_used']  = round(self.proc_units_used, 1)

        dic[metric_str+'memory_mb'] = self.memory_mb
        if toplevel_str+'sum_memory_mb' in dic:
            dic[toplevel_str+'sum_memory_mb'] += self.memory_mb
        else:
            dic[toplevel_str+'sum_memory_mb']  = self.memory_mb
  
        dic[metric_str+'memory_used_mb'] = self.memory_used_mb
        if toplevel_str+'sum_memory_used_mb' in dic:
            dic[toplevel_str+'sum_memory_used_mb'] += self.memory_used_mb
        else:
            dic[toplevel_str+'sum_memory_used_mb']  = self.memory_used_mb

        # percentage metric
        dic[metric_str + 'cpus_used_percentage'] = round(((self.proc_units_used+self.proc_units_reserved)/self.proc_units)*100, 1)
        dic[metric_str + 'memory_used_percentage'] = round(((self.memory_used_mb/self.memory_mb_api)*100), 1)
        dic[toplevel_str + 'sum_cpus_used_percentage'] = round(((dic[toplevel_str+'sum_proc_units_used']*100)/dic[toplevel_str+'sum_proc_units']), 1)
        dic[toplevel_str + 'sum_memory_used_percentage'] = round(((dic[toplevel_str+'sum_memory_used_mb']*100)/dic[toplevel_str+'sum_memory_mb']), 1)
        # state metric
        full_metric_str = metric_str + 'statedown'
        value = 1 if self.state == 'down' else 0
        dic[full_metric_str] = value
        if self.state == 'down':
            if toplevel_str+'sum_compute_statedown' in dic:
                dic[toplevel_str+'sum_compute_statedown'] += 1
            else:
                dic[toplevel_str+'sum_compute_statedown']  =  1
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

