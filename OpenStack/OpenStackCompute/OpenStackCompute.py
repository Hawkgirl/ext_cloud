from BaseCloud.BaseCompute.BaseCompute import BaseComputecls 
from OpenStack.OpenStackCompute.OpenStackInstance import OpenStackInstancecls
from OpenStack.OpenStackCompute.OpenStackHypervisor import OpenStackHypervisorcls
from OpenStack.OpenStackCompute.OpenStackInstanceType import OpenStackInstanceTypecls
from OpenStack.OpenStackCompute.OpenStackSecurityGroup import OpenStackSecurityGroupcls
from OpenStack.OpenStackCompute.OpenStackKeypair import OpenStackKeypaircls
from OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls

class OpenStackComputecls(OpenStackBaseCloudcls, BaseComputecls):

	def __init__(self, *args, **kwargs):
		self._credentials = kwargs

	def list_metrics(self):
		metrics = []
		from BaseCloud.BaseStats.BaseMetrics import BaseMetricscls

		from toolz import countby
		instances = self.list_instances()
		group_by_state = countby(lambda x: x.state, instances)
		metrics.append(BaseMetricscls('openstack.instances.total', len(instances)))
		metrics.append(BaseMetricscls('openstack.instances.running', group_by_state['RUNNING'] if 'RUNNING' in group_by_state else 0))
		metrics.append(BaseMetricscls('openstack.instances.stopped', group_by_state['STOPPED'] if 'STOPPED' in group_by_state else 0))
		metrics.append(BaseMetricscls('openstack.instances.error', group_by_state['ERROR'] if 'ERROR' in group_by_state else 0))
		return metrics

	@property
	def Childrens(self):
		hypervisors = self.list_hypervisors()
		return hypervisors


        def list_instances(self):
                openstack_instances =  self._NovaClient.servers.list(search_opts = {'all_tenants': 1})
                instances = []
	
               	for openstack_instance in openstack_instances:
                	instance = OpenStackInstancecls(openstack_instance, credentials=self._credentials)
                       	instances.append(instance)

                return instances

	def get_instance_by_id(self, instance_id):
		instances = self.list_instances()
		for instance in instances:
			if instance.id == instance_id:
				return instance
		return None	

        def get_instances_by_name(self, instance_name): pass
        def get_instances_by_tag(self, tag_name, tag_value): pass
	def create_instance(self, image_id=None, key_name=None, security_groups=None, security_group_ids=None, instancetype_id = None, name = None, subnet_id=None): 

		nics = []
		if subnet_id is not None:
			neutron_client = OpenStackClientsCls().get_neutron_client(self._credentials)
			from OpenStack.OpenStackNetworks.OpenStackNetworks import OpenStackNetworkscls
			subnet = OpenStackNetworkscls(**self._credentials).get_subnet_by_id(subnet_id)
			nic = subnet.attach_nic(name=name)
			nics = [{"port-id": nic.id}]
			

                openstack_instance =  self.__NovaClient.servers.create(name, image_id, instancetype_id, nics=nics, security_groups=security_groups, key_name=key_name)
               	instance = OpenStackInstancecls(openstack_instance, credentials=self._credentials)
                return instance
	def create_instances(self, count=1,image_id=None, key_name=None, security_groups=None, instancetype_id = None, names = None): pass

	# ---------- Hypervisor operations -----------------
	def list_hypervisors(self):
		openstack_hypervisors = self.__NovaClient.hypervisors.list()
		hypervisors = []
		for openstack_hypervisor in openstack_hypervisors:
			hypervisor = OpenStackHypervisorcls(openstack_hypervisor, credentials = self._credentials)
			hypervisors.append(hypervisor)

		return hypervisors

	# ------ Key pair opertations ----------------------------------------
        def list_keypairs(self): 
		openstack_keypairs = self.__NovaClient.keypairs.list()
                keypairs = []
                for openstack_keypair in openstack_keypairs:
                        keypair = OpenStackKeypaircls(openstack_keypair, credentials = self._credentials)
                        keypairs.append(keypair)
                return keypairs
        def create_keypair(self, name=None):
		openstack_keypair = self.__NovaClient.keypairs.create(name)
		keypair = OpenStackKeypaircls(openstack_keypair, credentials = self._credentials)
                return keypair
	def import_keypair(self, name=None, public_key=None): pass
	def get_key_pair_by_name(self, keyname): pass

	#--------------  Security group operations ----------------------------------------
	def list_security_groups(self):
		openstack_security_groups = self.__NovaClient.security_groups.list()
		security_groups = []
		for openstack_security_group in openstack_security_groups:
			security_group = OpenStackSecurityGroupcls(openstack_security_group, credentials=self._credentials)
			security_groups.append(security_group)

		return security_groups

	def get_security_group_by_id(self, sg_id):
                openstack_security_group = self.__NovaClient.security_groups.get(sg_id)
                security_group =  OpenStackSecurityGroupcls(openstack_security_group, credentials=self._credentials)
                return security_group

        def create_security_group(self, name=None, description=None, network_id=None):
                openstack_security_group = self.__NovaClient.security_groups.create(name,description)
                security_group = OpenStackSecurityGroupcls(openstack_security_group, credentials=self._credentials)
                return security_group


	# ------ Instance Type opertations ----------------------------------------
	def list_instancetypes(self):
		openstack_instancetypes = self.__NovaClient.flavors.list()
		instancetypes = []
		for openstack_instancetype in openstack_instancetypes:
			instancetype = OpenStackInstanceTypecls(openstack_instancetype, credentials=self._credentials)
			instancetypes.append(instancetype)

		return instancetypes

	def create_instancetype(self, name=None, ram=100, vcpus=1, disk=5):
		openstack_instancetype = self.__NovaClient.flavors.create(name=name, ram=ram, vcpus=vcpus,disk=disk)

		instancetype = OpenStackInstanceTypecls(openstack_instancetype, credentials=self._credentials)
		return instancetype

	def get_matching_instancetype(self, cpus=1, memory=0.5, disk=2):
                instance_types = self.list_instancetypes()
                if len(instance_types) == 0:
                        return None
                best_match = None
                for instance_type in instance_types:
                        if instance_type.cpus >= cpus and instance_type.memory >= memory  and instance_type.disk >= disk:
                                best_match = instance_type

                if best_match is None:
                        return None
                for instance_type in instance_types:
                        if instance_type.cpus >= cpus and instance_type.memory >= memory and instance_type.disk >= disk:
                                if instance_type.cpus < best_match.cpus:
                                        best_match = instance_type
                                elif instance_type.cpus == best_match.cpus:
                                        if instance_type.memory < best_match.cpus:
                                                best_match = instance_type
                                        elif instance_type.memory == best_match.memory:
                                                if instance_type.disk < best_match.disk:
                                                        best_match = instance_type
                return best_match

