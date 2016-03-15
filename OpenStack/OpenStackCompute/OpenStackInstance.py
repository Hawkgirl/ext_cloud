from ext_cloud.BaseCloud.BaseCompute.BaseInstance import BaseInstancecls
from ext_cloud.BaseCloud.BaseCompute.BaseInstance import STATE
from ext_cloud.OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls

import collections
STATE_MAP = collections.defaultdict(lambda: STATE.UNKNOWN)
STATE_MAP['ACTIVE'] = STATE.RUNNING
STATE_MAP['PAUSED'] = STATE.PAUSED
STATE_MAP['SHUTOFF'] = STATE.STOPPED
STATE_MAP['ERROR'] = STATE.ERROR
STATE_MAP['BUILD'] = STATE.STARTING

class OpenStackInstancecls(OpenStackBaseCloudcls, BaseInstancecls):
	
	__openstack_instance = None


	def __init__(self, *arg, **kwargs):
                self.__openstack_instance = arg[0]
                super(OpenStackInstancecls, self).__init__(id=self.__openstack_instance.id, name=self.__openstack_instance.name, credentials=kwargs['credentials'])


        @property
        def size(self): return self.__openstack_instance.flavor['id']

        @property
        def state(self): return str(STATE_MAP[self.__openstack_instance.status])

	def start(self): 
		return self.__openstack_instance.start_instance()

	def stop(self):
		return self.__openstack_instance.stop_instance()

	def reboot(self):
		return self.__openstack_instance.reboot_instance()

	def delete(self):pass
	
	def setname(self, name): pass

	def attach_nic(self, port_id=None, net_id=None, ip_address=None):
		self.__openstack_instance.interface_attach(port_id, net_id,ip_address)

	def detach_nic(self, port_id=None):
		self.__openstack_instance.interface_attach(port_id)

	def add_security_group(self, security_group):
		self.__openstack_instance.add_security_group(security_group)

	@property
        def keypair_name(self): return self.__openstack_instance.key_name
	
	@property
        def image_id(self): 
		if isinstance(self.__openstack_instance.image, dict):
			return self.__openstack_instance.image['id']

		return None
	
	@property
	def tenant_id(self): return self.__openstack_instance.tenant_id

	@property
	def user_id(self): return self.__openstack_instance.user_id

	@property
        def image_name(self): pass

	@property
        def arch(self): pass

	@property
        def network_id(self): pass

	@property
        def subnet_id(self): pass

	@property
        def private_ip(self):
		for key in self.__openstack_instance.addresses:
			nics = self.__openstack_instance.addresses[key]
			for nic in nics:
				if nic['OS-EXT-IPS:type'] == 'fixed':
					return nic['addr']

	@property
        def public_ip(self): 
		for key in self.__openstack_instance.addresses:
			nics = self.__openstack_instance.addresses[key]
			for nic in nics:
				if nic['OS-EXT-IPS:type'] == 'floating':
					return nic['addr']

	@property
        def keypair_name(self): pass

	@property
        def dns_name(self): pass

	@property
        def creation_time(self): pass

	@property
        def os_type(self): pass

	def attach_floatingip(self):
		from OpenStack.OpenStackNetworks.OpenStackNetworks import OpenStackNetworkscls
		nics = OpenStackNetworkscls(**self._credentials).get_all_nics()
		nic_id = None
		for nic in nics:
			if nic.ip_address == self.private_ip:
				nic_id = nic.id
				break;
		floatingips_dict = self._NeutronClient.list_floatingips()
		floatingips_list = floatingips_dict['floatingips']
		floatingip_id = None
		for floatingip in floatingips_list:
			if floatingip['fixed_ip_address'] is None:
				floatingip_id = floatingip['id']
				break

		#empty floating ip not found, create?
		if floatingip_id is None:
			return
		self._NeutronClient.update_floatingip(floatingip_id, 
					{'floatingip': { 'port_id' : nic_id }})

        def addtag(self): pass

	def gettags(self): pass

	@property
	def is_zombie(self):
		from ext_cloud.OpenStack.OpenStackIdentity.OpenStackIdentity import OpenStackIdentitycls
		tenant = OpenStackIdentitycls(**self._credentials).get_tenant_by_id(self.tenant_id)
		if tenant is None:
			return True
	
		user = OpenStackIdentitycls(**self._credentials).get_user_by_id(self.user_id)
		if user is None:
			return True

		return False
