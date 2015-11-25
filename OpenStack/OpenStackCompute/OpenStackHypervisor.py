from ext_cloud.BaseCloud.BaseCompute.BaseHypervisor import BaseHypervisorcls
from ext_cloud.OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls

class OpenStackHypervisorcls(OpenStackBaseCloudcls, BaseHypervisorcls):
	
	__openstack_hypervisor = None

	def __init__(self, *arg, **kwargs):
                self.__openstack_hypervisor = arg[0]
                super(OpenStackHypervisorcls, self).__init__(id=self.__openstack_hypervisor.id, name=self.__openstack_hypervisor.hypervisor_hostname,credentials=kwargs['credentials'])

        @property
        def state(self): return self.__openstack_hypervisor.state

        @property
        def status(self): return self.__openstack_hypervisor.status

        @property
        def arch(self): 
		cpu_arch = None
		try:
			import ast
                	cpu_dict = ast.literal_eval(self.__openstack_hypervisor.cpu_info)
			cpu_arch = cpu_dict['arch']
            	except:
               		 pass
		return cpu_arch

        @property
        def host_name(self): return self.__openstack_hypervisor.hypervisor_hostname 

        @property
        def short_host_name(self): 
                return self.host_name.split('.', 1)[0]

        @property
        def cpus(self): return self.__openstack_hypervisor.vcpus

        @property
        def vcpus_used(self): return self.__openstack_hypervisor.vcpus_used

        @property
        def disk_gb(self): return self.__openstack_hypervisor.local_gb

        @property
        def disk_used_gb(self): return self.__openstack_hypervisor.local_gb_used

	@property
        def free_disk_gb(self): return self.__openstack_hypervisor.free_disk_gb

        @property
        def memory_mb(self): return self.__openstack_hypervisor.memory_mb

        @property
        def memory_used_mb(self): return self.__openstack_hypervisor.memory_mb_used

        @property
        def memory_free_mb(self): return self.__openstack_hypervisor.free_ram_mb

        @property
        def running_vms(self): return self.__openstack_hypervisor.running_vms

	@property
	def host_ip(self): return self.__openstack_hypervisor.host_ip

	def list_metrics(self):
		from ext_cloud.BaseCloud.BaseStats.BaseMetrics import BaseMetricscls
		metrics = []
		metric_property = ( 'cpus','vcpus_used','disk_gb', 'disk_used_gb', 'free_disk_gb', 'memory_mb', 'memory_used_mb', 'memory_free_mb', 'running_vms')

		metric_str = 'openstack.hypervisors.' + self.short_host_name + '.'
            	for metric in metric_property:
               		full_metric_str = metric_str + metric
			new_metric = BaseMetricscls(full_metric_str, getattr(self, metric))
			metrics.append(new_metric)
            	# state metric
           	full_metric_str = metric_str + 'statedown'
		value =  1 if self.state == 'down' else 0
		new_metric = BaseMetricscls(full_metric_str, value)
		metrics.append(new_metric)
		# status
           	full_metric_str = metric_str + 'statusdisabled'
		value =  1 if self.status == 'disabled' else 0
		new_metric = BaseMetricscls(full_metric_str, value)
		metrics.append(new_metric)
		# arch metric
		if not self.arch is None:
	           	full_metric_str = metric_str + 'arch.' + self.arch
			new_metric = BaseMetricscls(full_metric_str, 1)
			metrics.append(new_metric)

		return metrics

