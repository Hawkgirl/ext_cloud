from ext_cloud.BaseCloud.BaseCompute.BaseSecurityGroup import BaseSecurityGroupcls
from ext_cloud.OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls
from OpenStackSecurityGroupRule import OpenStackSecurityGroupRulecls


class OpenStackSecurityGroupcls(OpenStackBaseCloudcls, BaseSecurityGroupcls):

	__openstack_securitygroup = None
	__novaclient = None

	def __init__(self, *arg, **kwargs):
                self.__openstack_securitygroup = arg[0]

                super(OpenStackSecurityGroupcls, self).__init__(id=self.__openstack_securitygroup.id, name=self.__openstack_securitygroup.name, credentials=kwargs['credentials'])


	@property
        def __NovaClient(self):
                return self.__novaclient

        @__NovaClient.getter
        def __NovaClient(self):
                if self.__novaclient is None:
                        if self._credentials.has_key('token'):
                                self.__novaclient = NovaClient('2', self._credentials['username'], self._credentials['token'], self._credentials['tenant_name'], self._credentials['auth_url'], 'compute', auth_token=self._credentials['token'], region_name=self._credentials['region_name'])
                        else:
                                self.__novaclient = NovaClient('2', self._credentials['username'], self._credentials['password'], self._credentials['tenant_name'], self._credentials['auth_url'], 'compute', region_name=self._credentials['region_name'])

                return self.__novaclient

        @property
        def description(self):
		return self.__openstack_securitygroup.description

	@property
        def rules(self):
		rules = []
		for rule in self.__openstack_securitygroup.rules:
			openstack_rule = OpenStackSecurityGroupRulecls(ip_protocol = rule['ip_protocol'], from_port = rule['from_port'], to_port = rule['to_port'], cidr_block=rule['ip_range'],id=rule['id'])
                        rules.append(openstack_rule)

		return rules

        def delete(self):
                self.__openstack_securitygroup.delete()

        def add_rule(self, ip_protocol='tcp', from_port=None, to_port=None, cidr_block=None):
		self.__NovaClient.security_group_rules.create(self.__openstack_securitygroup.id, ip_protocol=ip_protocol, from_port=from_port, to_port=to_port, cidr=cidr_block)

        def delete_rule(self, ip_protocol='tcp', from_port=None, to_port=None, cidr_block=None):
		pass

