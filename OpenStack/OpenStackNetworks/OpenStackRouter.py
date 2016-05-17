from ext_cloud.BaseCloud.BaseNetworks.BaseRouter import BaseRoutercls
from ext_cloud.OpenStack.OpenStackBaseCloud import OpenStackBaseCloudcls


class OpenStackRoutercls(OpenStackBaseCloudcls, BaseRoutercls):

    __openstack_router = None
    __neutronclient = None

    def __init__(self, *arg, **kwargs):
        self.__openstack_router = arg[0]

        super(OpenStackRoutercls, self).__init__(id=self.__openstack_router['id'], name=self.__openstack_router['name'], credentials=kwargs['credentials'])

    @property
    def state(self):
        return self.__openstack_router['status']

    @property
    def tenant_id(self):
        return self.__openstack_router['tenant_id']

    @property
    def is_zombie(self):
        from ext_cloud.OpenStack.OpenStackIdentity.OpenStackIdentity import OpenStackIdentitycls
        tenant = OpenStackIdentitycls(**self._credentials).get_tenant_by_id(self.tenant_id)
        if tenant is None:
            return True
        return False

    def delete(self):
        pass

    def add_route(self, destination_cidr_block=None, gateway_id=None, instance_id=None, interface_id=None):
        pass

    def attach_nic(self, nic_id):
        pass

    def attach_subnet(self, subnet_id):
        self._Clients.neutron.add_interface_router(self.id, {'subnet_id': subnet_id})

    @property
    def port_ips(self):
	dic = {}
	dic['device_id'] = self.id
	lst = []
	ports = self._Clients.neutron.list_ports(**dic)['ports']
	for port in ports:
		lst.append(port['fixed_ips'][0]['ip_address'])
	return lst
